import hashlib
import shutil
import os
import sys
import time
from pathlib import Path

from data_module import globalconfig
from data_module.globalconfig import *
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    cast,
)
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Error,
    Page,
    Playwright,
    expect,
)
from pytest_playwright.pytest_playwright import CreateContextCallback
from slugify import slugify
import tempfile
import allure
import re
from playwright01.utils.globalMap import GlobalMap
from playwright._impl._locator import Locator as LocatorImpl
from playwright._impl._sync_base import mapping
from playwright.sync_api._generated import Locator as _Locator
import json
from allure import step

from utils.http_util import HttpClient

# 在全局变量区域添加
_test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'failed_tests': []
}
time_out = 30000

# 调试模式开关
DEBUG_MODE = True  # 设为False时跳过实际API调用
# @pytest.fixture()
# def hello_world():
#     print("hello")
#     yield
#     print("world")
#
#
# @pytest.fixture
# def page(context: BrowserContext) -> Page:
#     print("this is my page")
#     return context.new_page()


@pytest.fixture(scope="session", autouse=True)
def test_init(base_url):
    global_map = GlobalMap()
    global_map.set("baseurl", base_url)
    env = re.search("(https://)(.*)(.ezone.work)", base_url).group(2)
    global_map.set("env", env)


@pytest.fixture(scope="session")
def browser_context_args(
        pytestconfig: Any,
        playwright: Playwright,
        device: Optional[str],
        base_url: Optional[str],
        # _pw_artifacts_folder: tempfile.TemporaryDirectory,
) -> Dict:
    width, height = pytestconfig.getoption("--viewport")
    context_args = {}
    if device:
        context_args.update(playwright.devices[device])
    if base_url:
        context_args["base_url"] = base_url
    # video_option = pytestconfig.getoption("--video")
    # capture_video = video_option in ["on", "retain-on-failure"]
    # if capture_video:
    #     context_args["record_video_dir"] = _pw_artifacts_folder.name

    return {
        **context_args,
        "viewport": {
            "width": width,
            "height": height,
        },
        "record_video_size": {
            "width": width,
            "height": height,
        },
    }


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--viewport",
        action="store",
        default=[1440, 900],
        help="viewport size set",
        type=int,
        nargs=2,
    )
    group.addoption(
        "--ui_timeout",
        default=30_000,
        help="locator timeout and expect timeout",
    )
    group.addoption(
        "--rerun_strategy",
        action="store",
        default=None,
        #  这里不使用nargs="*"是因为无限个args对参数的位置有要求,或者测试目标需要用参数指定
        help="testcase rerun strategy set, eg: screenshot=retain-on-failure,video=retain-on-failure,tracing=retain-on-failure",
    )
    group.addoption(
        "--allure_report_auto_open",
        action="store",
        default="off",
        help="if finish test, allure report auto open, eg: /Users/liuyunlong/Desktop/pw-allure",
    )


@pytest.fixture(scope="session")
def ui_timeout(pytestconfig):
    timeout = float(pytestconfig.getoption("--ui_timeout"))
    expect.set_options(timeout=timeout)
    return timeout


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        try:
            for context in item.funcargs['browser'].contexts:
                for page in context.pages:
                    if page.is_closed():
                        continue
                    bytes_png = page.screenshot(timeout=5000, full_page=True)
                    allure.attach(bytes_png, f"失败截图---{page.title()}")
        except:
            ...


@pytest.fixture()
def _artifacts_recorder(
        request: pytest.FixtureRequest,
        playwright: Playwright,
        pytestconfig: Any,
        _pw_artifacts_folder: tempfile.TemporaryDirectory,
) -> Generator["ArtifactsRecorder", None, None]:
    artifacts_recorder = ArtifactsRecorder(
        pytestconfig, request, playwright, _pw_artifacts_folder
    )
    yield artifacts_recorder
    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True
    artifacts_recorder.did_finish_test(failed)


def truncate_file_name(file_name: str) -> str:
    if len(file_name) < 256:
        return file_name
    return f"{file_name[:100]}-{hashlib.sha256(file_name.encode()).hexdigest()[:7]}-{file_name[-100:]}"


def _build_artifact_test_folder(
        pytestconfig: Any, request: pytest.FixtureRequest, folder_or_file_name: str
) -> str:
    output_dir = pytestconfig.getoption("--output")
    return os.path.join(
        output_dir,
        #  修改为request.node.name,以便支持中文用例名称,所有的request.node.name都是这个目的
        truncate_file_name(request.node.name),
        truncate_file_name(folder_or_file_name),
    )


@pytest.fixture
def new_context(
        browser: Browser,
        browser_context_args: Dict,
        _artifacts_recorder: "ArtifactsRecorder",
        request: pytest.FixtureRequest,
        ui_timeout: float,
        pytestconfig: Any,
        _pw_artifacts_folder: tempfile.TemporaryDirectory,
) -> Generator[CreateContextCallback, None, None]:
    browser_context_args = browser_context_args.copy()
    context_args_marker = next(request.node.iter_markers("browser_context_args"), None)
    additional_context_args = context_args_marker.kwargs if context_args_marker else {}
    browser_context_args.update(additional_context_args)
    contexts: List[BrowserContext] = []

    def _new_context(**kwargs: Any) -> BrowserContext:
        #  获取重试的log策略并转成列表
        _rerun_strategy = pytestconfig.getoption("--rerun_strategy").split(",")
        #  获取重试次数,此处为2则为重试2次,加上第1次,一共跑3次
        _reruns = pytestconfig.getoption("--reruns")
        video_option = pytestconfig.getoption("--video")
        #  重试log策略(默认None)和重试次数(默认0)参数必须都有值
        if _rerun_strategy and _reruns:
            #  使用空字符串去补足轮次和策略的对应关系:
            if _reruns + 1 > len(_rerun_strategy):
                _init_rerun_strategy = [""] * (1 + _reruns - len(_rerun_strategy)) + _rerun_strategy
            #  使用切片来处理多余的策略(如果相等,则切片是本身),可根据自身设计改成从后往前切
            else:
                _init_rerun_strategy = _rerun_strategy[:_reruns + 1]
            #  这里减1是因为request.node.execution_count从1开始,我们取列表下标从0开始
            rerun_round = request.node.execution_count - 1
            _round_rerun_strategy = _init_rerun_strategy[rerun_round]

            #  这里先判断是否有log策略
            if _round_rerun_strategy:
                if "video" in _round_rerun_strategy:
                    video_option = _round_rerun_strategy.split("=")[-1]
                else:
                    video_option = "off"
            else:
                video_option = "off"
        #  这里只判断了video,是因为创建context时必须设置record_video_dir后才开始主动录屏
        capture_video = video_option in ["on", "retain-on-failure"]
        browser_context_args.update(kwargs)
        if capture_video:
            video_option_dict = {"record_video_dir": _pw_artifacts_folder.name}
            #  字典的update可以直接传字典,也可以解包,解包相当于kwargs
            browser_context_args.update(video_option_dict)
        my_context = browser.new_context(**browser_context_args)
        my_context.set_default_timeout(ui_timeout)
        my_context.set_default_navigation_timeout(ui_timeout * 2)
        original_close = my_context.close

        def _close_wrapper(*args: Any, **my_kwargs: Any) -> None:
            contexts.remove(context)
            _artifacts_recorder.on_will_close_browser_context(my_context)
            original_close(*args, **my_kwargs)

        my_context.close = _close_wrapper
        contexts.append(my_context)
        _artifacts_recorder.on_did_create_browser_context(my_context)
        return my_context

    yield cast(CreateContextCallback, _new_context)
    for context in contexts.copy():
        context.close()


class ArtifactsRecorder:
    def __init__(
            self,
            pytestconfig: Any,
            request: pytest.FixtureRequest,
            playwright: Playwright,
            pw_artifacts_folder: tempfile.TemporaryDirectory,
    ) -> None:
        """
        初始化 ArtifactsRecorder 类。

        Args:
            pytestconfig: pytest 配置对象
            request: pytest 测试请求对象
            playwright: Playwright 对象
            pw_artifacts_folder: 用于存储测试过程中生成的工件的临时目录

        """

        self._request = request
        self._pytestconfig = pytestconfig
        self._playwright = playwright
        self._pw_artifacts_folder = pw_artifacts_folder

        self._all_pages: List[Page] = []
        self._screenshots: List[str] = []
        self._traces: List[str] = []
        self._rerun_strategy = pytestconfig.getoption("--rerun_strategy").split(",")
        self._reruns = pytestconfig.getoption("--reruns")
        #  这里逻辑了上面的一致,不赘述了
        if self._rerun_strategy and self._reruns:
            if self._reruns + 1 >= len(self._rerun_strategy):
                self._init_rerun_strategy = [""] * (1 + self._reruns - len(self._rerun_strategy)) + self._rerun_strategy
            else:
                self._init_rerun_strategy = self._rerun_strategy[:self._reruns + 1]

            rerun_round = request.node.execution_count - 1
            self._round_rerun_strategy = self._init_rerun_strategy[rerun_round]

            #  以下为判断log策略内容和参数的方法,注意,如果没有则设置为off
            if "screenshot" in self._round_rerun_strategy:
                self._screenshot_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._screenshot_option = "off"
            if "video" in self._round_rerun_strategy:
                self._video_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._video_option = "off"
            if "tracing" in self._round_rerun_strategy:
                self._tracing_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._tracing_option = "off"
            self._capture_trace = self._tracing_option in ["on", "retain-on-failure"]
        else:
            #  没有重试log策略和重试次数,自然取原始的log策略
            self._screenshot_option = self._pytestconfig.getoption("--screenshot")
            self._video_option = self._pytestconfig.getoption("--video")
            self._tracing_option = pytestconfig.getoption("--tracing")
            self._capture_trace = self._tracing_option in ["on", "retain-on-failure"]

    def did_finish_test(self, failed: bool) -> None:
        """
        在测试完成时执行的方法。

        根据测试是否失败以及配置的日志策略,保存截图、录制的跟踪信息和视频。

        Args:
            failed: 测试是否失败
        """
        #  获取当前轮次并初始化一个字符串,给保存文件做前缀
        round_prefix = f"round{self._request.node.execution_count}-"
        #  这里可以学习一下组合的布尔逻辑
        capture_screenshot = self._screenshot_option == "on" or (
                failed and self._screenshot_option == "only-on-failure"
        )
        if capture_screenshot:
            for index, screenshot in enumerate(self._screenshots):
                human_readable_status = "failed" if failed else "finished"
                screenshot_path = _build_artifact_test_folder(
                    self._pytestconfig,
                    self._request,
                    #  原始为 f"test-{human_readable_status}-{index + 1}.png",
                    f"{round_prefix}{index + 1}-{human_readable_status}-{screenshot.split(os.sep)[-1]}.png",
                )
                #  这里这种写法注意下,如果自己需要放log,用这个方式创建很好
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                shutil.move(screenshot, screenshot_path)
                # shutil.copy(screenshot, screenshot_path)
                # allure附加图片文件的方法
                allure.attach.file(screenshot_path, f"{round_prefix}{index + 1}-{human_readable_status}-{screenshot.split(os.sep)[-1]}.png")
        else:
            for screenshot in self._screenshots:
                os.remove(screenshot)

        if self._tracing_option == "on" or (
                failed and self._tracing_option == "retain-on-failure"
        ):
            for index, trace in enumerate(self._traces):
                trace_file_name = (
                    f"{round_prefix}trace.zip" if len(self._traces) == 1 else f"{round_prefix}trace-{index + 1}.zip"
                )
                trace_path = _build_artifact_test_folder(
                    self._pytestconfig, self._request, trace_file_name
                )
                os.makedirs(os.path.dirname(trace_path), exist_ok=True)
                shutil.move(trace, trace_path)
                # allure附加zip文件的方法
                allure.attach.file(trace_path, "trace.playwright.dev", extension="zip")
        else:
            for trace in self._traces:
                os.remove(trace)

        preserve_video = self._video_option == "on" or (
                failed and self._video_option == "retain-on-failure"
        )
        if preserve_video:
            for index, page in enumerate(self._all_pages):
                video = page.video
                if not video:
                    continue
                try:
                    # 获取页面标题并处理非法字符
                    page_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', page.title())[:30]
                    video_file_name = (
                        f"{round_prefix}video.webm"
                        if len(self._all_pages) == 1
                        else f"{round_prefix}video-{index + 1}-{page_title}.webm"
                    )
                    video.save_as(
                        path=_build_artifact_test_folder(
                            self._pytestconfig, self._request, video_file_name
                        )
                    )

                    # 自定义 allure 附件名称
                    custom_video_title = f"过程录像_{page_title}_{round_prefix}video{index + 1}"
                    allure.attach.file(
                        _build_artifact_test_folder(self._pytestconfig, self._request, video_file_name),
                        custom_video_title,
                        allure.attachment_type.WEBM
                    )
                except Error:
                    # Silent catch empty videos.
                    pass

    def on_did_create_browser_context(self, context: BrowserContext) -> None:
        """
        在即将关闭浏览器上下文时执行的方法。

        停止录制跟踪信息,并根据配置保存截图。

        Args:
            context: 即将关闭的浏览器上下文
        """

        #  上下文里监听,有新的page就添加到列表中
        context.on("page", lambda page: self._all_pages.append(page))
        #  判断是否需要trace,如果需要,就开始录制
        if self._request and self._capture_trace:
            context.tracing.start(
                title=slugify(self._request.node.name),
                screenshots=True,
                snapshots=True,
                sources=True,
            )

    def on_will_close_browser_context(self, context: BrowserContext) -> None:
        #  判断是否需要trace,如果需要,就结束录制
        if self._capture_trace:
            trace_path = Path(self._pw_artifacts_folder.name) / create_guid()
            context.tracing.stop(path=trace_path)
            self._traces.append(str(trace_path))
        else:
            context.tracing.stop()

        #  如果需要截图,就在关闭page前,获取截图
        if self._screenshot_option in ["on", "only-on-failure"]:
            for page in context.pages:
                #  这里用try是因为有可能page已经关闭了
                try:
                    screenshot_path = (
                        # Path(self._pw_artifacts_folder.name) / create_guid()
                        # Path(self._pw_artifacts_folder.name) / page.title()
                        Path(self._pw_artifacts_folder.name) / "".join([page.title()[:10], str(time.time_ns())])
                    )
                    page.screenshot(
                        timeout=5000,
                        path=screenshot_path,
                        full_page=self._pytestconfig.getoption(
                            "--full-page-screenshot"
                        ),
                    )
                    self._screenshots.append(str(screenshot_path))
                except Error:
                    pass


def create_guid() -> str:
    return hashlib.sha256(os.urandom(16)).hexdigest()



class Locator(_Locator):
    __last_step = None

    @property
    def selector(self):
        _repr = self.__repr__()
        if "selector" in _repr:
            __selector = []
            for _ in _repr.split("selector=")[1][1:-2].split(" >> "):
                if r"\\u" not in _:
                    __selector.append(_)
                    continue
                __selector.append(
                    _.encode("utf8")
                    .decode("unicode_escape")
                    .encode("utf8")
                    .decode("unicode_escape")
                )
            return " >> ".join(__selector)

    def __getattribute__(self, attr):
        global api_Count
        global time_out
        try:
            orig_attr = super().__getattribute__(attr)
            if callable(orig_attr):

                def wrapped(*args, **kwargs):
                    step_title = None
                    if attr == "_sync" and self.__last_step:
                        step_title = self.__last_step
                    else:
                        self.__last_step = attr
                    start_time = time.time()
                    global 最后操作的page
                    最后操作的page = self.page
                    while True:
                        self.page.wait_for_load_state()
                        if time.time() - start_time < int(time_out / 1333):
                            try:
                                if attr in ["click", "fill", "hover", "check", "blur", "focus"]:
                                    self.page.wait_for_timeout(100)
                                    api_length = len(api_Count)
                                    if api_Count:
                                        self.page.wait_for_timeout(200)
                                        self.page.evaluate('''() => {
                                               const spanToRemove = document.getElementById('ainotestgogogo');
                                               if (spanToRemove) {
                                                   spanToRemove.remove();
                                               }
                                           }''')
                                        self.page.evaluate(f'''() => {{
                                                const span = document.createElement('span');
                                                span.textContent = '{attr}:{api_length}';
                                                span.style.position = 'absolute';
                                                span.style.top = '0';
                                                span.style.left = '50%';
                                                span.style.transform = 'translateX(-50%)';
                                                span.style.backgroundColor = 'yellow'; // 设置背景色以便更容易看到
                                                span.style.zIndex = '9999';
                                                span.id = 'ainotestgogogo';
                                                document.body.appendChild(span);
                                            }}''')
                                    else:
                                        # 在这里可以添加自己需要等待或者处理的动作,比如等待转圈,关闭弹窗等等(当然,弹窗最好单独做个监听)
                                        self.page.locator("//*[contains(@class, 'spin-dot-spin')]").locator("visible=true").last.wait_for(state="hidden", timeout=30_000)
                                        if self.page.locator('//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]').locator("visible=true").or_(self.page.locator(".driver-close-btn").filter(has_text="关闭").locator("visible-true")).count():
                                            self.page.locator('//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]').locator("visible=true").or_(self.page.locator(".driver-close-btn").filter(has_text="关闭").locator("visible-true")).last.evaluate("node => node.click()")
                                        self.page.evaluate('''() => {
                                                const spanToRemove = document.getElementById('ainotestgogogo');
                                                if (spanToRemove) {
                                                    spanToRemove.remove();
                                                }
                                            }''')
                                        self.page.evaluate(f'''() => {{
                                                const span = document.createElement('span');
                                                span.textContent = '{attr}:{api_length}';
                                                span.style.position = 'absolute';
                                                span.style.top = '0';
                                                span.style.left = '50%';
                                                span.style.transform = 'translateX(-50%)';
                                                span.style.backgroundColor = 'green'; // 设置背景色以便更容易看到
                                                span.style.zIndex = '9999';
                                                span.id = 'ainotestgogogo';
                                                document.body.appendChild(span);
                                            }}''')
                                        break
                                else:
                                    break
                            except:
                                self.page.evaluate('''() => {
                                        const spanToRemove = document.getElementById('ainotestgogogo');
                                        if (spanToRemove) {
                                            spanToRemove.remove();
                                        }
                                    }''')
                                self.page.evaluate(f'''() => {{
                                        const span = document.createElement('span');
                                        span.textContent = '操作等待中.....';
                                        span.style.position = 'absolute';
                                        span.style.top = '0';
                                        span.style.left = '50%';
                                        span.style.transform = 'translateX(-50%)';
                                        span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                        span.style.zIndex = '9999';
                                        span.id = 'ainotestgogogo';
                                        document.body.appendChild(span);
                                    }}''')
                                break
                        else:
                            self.page.evaluate('''() => {
                                    const spanToRemove = document.getElementById('ainotestgogogo');
                                    if (spanToRemove) {
                                        spanToRemove.remove();
                                    }
                                }''')
                            escaped_api_count = json.dumps(api_Count)
                            self.page.evaluate(f'''() => {{
                                    const span = document.createElement('span');
                                    span.textContent = `当前列表内容为: {escaped_api_count}`;
                                    span.style.position = 'absolute';
                                    span.style.top = '0';
                                    span.style.left = '50%';
                                    span.style.transform = 'translateX(-50%)';
                                    span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                    span.style.zIndex = '9999';
                                    span.id = 'ainotestgogogo';
                                    document.body.appendChild(span);
                                }}''')
                            if sys.platform != "linux":
                                print("接口卡超时了,暂时放行,需要查看超时接口或调整接口监听范围:")
                                print(escaped_api_count)
                                pass
                            api_Count.clear()
                            break

                    if step_title:
                        with step(f"{step_title}: {self.selector}"):
                            return orig_attr(*args, **kwargs)
                    return orig_attr(*args, **kwargs)

                return wrapped
            return orig_attr
        except AttributeError:
            ...


mapping.register(LocatorImpl, Locator)





# """
# 在文件顶部导入部分添加requests
# import requests
# from typing import Dict, List
#
#
# @pytest.hookimpl(trylast=True)
# def pytest_sessionfinish(session, exitstatus):
#     """增强的测试结束处理"""
#     global _test_results
#
#     # 1. 打印美观的统计结果
#     print("\n" + "="*50)
#     print("测试执行统计".center(50))
#     print("-"*50)
#     print(f"总用例数: {_test_results['total']}")
#     print(f"通过数: \033[32m{_test_results['passed']}\033[0m")
#     print(f"失败数: \033[31m{_test_results['failed']}\033[0m")
#     print(f"跳过数: {_test_results['skipped']}")
#     print("="*50 + "\n")
#
#     # 2. 调试模式下保存失败用例到文件
#     if DEBUG_MODE and _test_results['failed'] > 0:
#         failed_file = Path(".failed_tests.json")
#         with open(failed_file, 'w', encoding='utf-8') as f:
#             json.dump(_test_results['failed_tests'], f, indent=2, ensure_ascii=False)
#         print(f"[调试模式] 已保存失败用例信息到: {failed_file.absolute()}")
#
#     # 3. 实际创建禅道bug
#     if not DEBUG_MODE and _test_results['failed'] > 0:
#         print("\n开始为失败用例创建禅道bug...")
#         for failed_test in _test_results['failed_tests']:
#             _create_zentaobug(failed_test)
#
#     # 保留原有的allure报告处理逻辑
#     allure_report_auto_open_config = session.config.getoption("--allure_report_auto_open")
#     if allure_report_auto_open_config != "off":
#         if sys.platform != "linux":
#             import subprocess
#             import psutil
#             import time
#             def kill_existing_allure_processes():
#                 '''关闭所有运行中的 allure serve 进程'''
#                 killed = False
#                 for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#                     try:
#                         cmdline = proc.info['cmdline']
#                         # 确保是 allure serve 进程
#                         if cmdline and 'allure' in ' '.join(cmdline) and 'serve' in ' '.join(cmdline):
#                             print(f"\nFound existing Allure process (PID: {proc.info['pid']}), terminating...")
#                             psutil.Process(proc.info['pid']).terminate()
#                             killed = True
#                     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#                         continue
#
#                 if killed:
#                     # 给进程一点时间来完全终止
#                     time.sleep(1)
#                 return killed
#
#             try:
#                 # 先尝试关闭已存在的 allure 进程
#                 kill_existing_allure_processes()
#
#                 # 启动新的 allure 服务
#                 allure_command = f'allure serve {allure_report_auto_open_config}'
#                 print(f"Starting new Allure server: {allure_command}")
#                 subprocess.Popen(allure_command, shell=True)
#
#             except Exception as e:
#                 print(f"Error managing Allure process: {str(e)}")
#
# # """
#
#
# def _create_zentaobug(failed_test: Dict) -> None:
#     """创建禅道bug的调试友好版本"""
#     try:
#         bug_data = {
#             "product": "自动化测试",
#             "module": "Playwright测试",
#             "title": f"自动化测试失败: {failed_test['name']}",
#             "steps": f"测试用例 {failed_test['nodeid']} 执行失败\n\n"
#                     f"错误信息:\n{failed_test.get('error', '无详细错误信息')}",
#             "severity": 3,
#             "pri": 2,
#             "openedBuild": "trunk"
#         }
#
#         if DEBUG_MODE:
#             # 调试模式下只打印不实际调用
#             print("\n[调试模式] 模拟创建禅道bug:")
#             print(json.dumps(bug_data, indent=2, ensure_ascii=False))
#             return
#
#         # 实际调用代码
#         response = requests.post(
#             "http://your-zentao-api/bug-create",
#             json=bug_data,
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": "Bearer your_token"
#             }
#         )
#         response.raise_for_status()
#         print(f"成功创建禅道bug: {response.json()}")
#     except Exception as e:
#         print(f"创建禅道bug失败: {str(e)}")
#

# import pytest
#
# def pytest_collection_modifyitems(config, items):
#     """根据标记重新排序测试项"""
#     # 分离并行和串行用例
#     parallel = []
#     serial = []
#
#     for item in items:
#         if item.get_closest_marker("parallel"):
#             parallel.append(item)
#         else:
#             serial.append(item)
#
#     # 先执行并行用例，后执行串行用例
#     items[:] = parallel + serial


# 替换原有的 pytest_sessionfinish 函数

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """增强的错误信息收集"""
    global _test_results

    if report.when == 'call':
        _test_results['total'] += 1

        if report.passed:
            _test_results['passed'] += 1
        elif report.failed:
            error_msg = str(report.longrepr) if hasattr(report, 'longrepr') else None
            # 提取更详细的错误信息
            if error_msg and 'AssertionError' in error_msg:
                error_msg = error_msg.split('AssertionError:')[-1].strip()

            _test_results['failed'] += 1
            _test_results['failed_tests'].append({
                'name': report.nodeid.split('::')[-1],
                'nodeid': report.nodeid,
                'error': error_msg,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            })
        elif report.skipped:
            _test_results['skipped'] += 1



@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    # 只在主进程中打开报告
    if not hasattr(session.config, 'workerinput'):
        if ENABLE_ALLURE_REPORT:
            # 自动打开allure报告
            allure_report_auto_open_config = session.config.getoption("--allure_report_auto_open")
            if allure_report_auto_open_config not in ["off", None, ""]:
                if sys.platform != "linux":
                    import subprocess
                    import psutil
                    import time

                    def kill_existing_allure_processes():
                        '''关闭所有运行中的 allure serve 进程'''
                        killed = False
                        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                            try:
                                cmdline = proc.info['cmdline']
                                # 确保是 allure serve 进程
                                if cmdline and 'allure' in ' '.join(cmdline) and 'serve' in ' '.join(cmdline):
                                    print(f"\nFound existing Allure process (PID: {proc.info['pid']}), terminating...")
                                    psutil.Process(proc.info['pid']).terminate()
                                    killed = True
                            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                continue

                        if killed:
                            # 给进程一点时间来完全终止
                            time.sleep(3)
                        return killed

                    try:
                        # 先尝试关闭已经存在的 allure 进程
                        kill_existing_allure_processes()

                        # 启动新的 allure 服务
                        allure_report_dir = allure_report_auto_open_config
                        allure_command = f'allure serve {allure_report_dir}'
                        print(f"Starting new Allure server: {allure_command}")
                        subprocess.Popen(allure_command, shell=True)

                    except Exception as e:
                        print(f"Error managing Allure process: {str(e)}")

        # 创建cat2bug BUG
        if ENABLE_CAT2BUG_CREATION:
            for failed_test in _test_results['failed_tests']:
                print("\n开始为失败用例创建cat2bug...")
                print(f"正在为用例 {failed_test['name']} 创建bug...")
                # 调用构造函数，该函数会完成登录和创建bug的全过程
                bug_result = construct_bug_data(failed_test)
                if bug_result.get('status') == 'success':
                    print(f"成功创建bug，编号: {bug_result.get('bug_id')}")
                else:
                    print("创建bug失败")

def construct_bug_data(failed_test: Dict, **kwargs) -> Dict:
    """构造cat2bug系统 bug 数据"""
    # 登录获取token
    with HttpClient(base_url=f"{BASE_URL}") as client:
        login_data = {
            "username": f"{USER}",
            "password": f"{PWD}"
        }

        login_result = client.post("/login", json_data=login_data)
        token = login_result.get('data', {}).get('token') if login_result.get('status_code') == 200 else None

        if not token:
            print("获取token失败")
            return {}

        # 构造bug数据
        bug_data = {
            "defectId": None,
            "defectType": "BUG",
            "defectName": f"自动化测试失败:{failed_test.get('name', '未知用例')}",
            "defectDescribe": f"测试用例执行失败\n错误信息:\n{failed_test.get('error_message', '无错误信息')}\n\n测试节点:{failed_test.get('nodeid', '未知节点')}",
            "annexUrls": None,
            "imgUrls": None,
            "projectId": 124,  # 可根据需要配置
            "testPlanId": None,
            "caseId": None,
            "dataSources": None,
            "dataSourcesParams": None,
            "moduleId": None,
            "moduleVersion": None,
            "createBy": None,
            "updateTime": None,
            "createTime": None,
            "updateBy": None,
            "defectState": None,
            "caseStepId": 0,
            "handleBy": [213],  # 可根据需要配置处理人
            "handleTime": None,
            "defectLevel": "middle",
            "srcHost": "https://www.cat2bug.com:8022"
        }

        # 请求头配置
        headers = {
            'authorization': f'Bearer {token}',
            'Accept': "*/*",
            'Content-Type': "application/json; charset=UTF-8"
        }

        # 提交bug
        result = client.post("/system/defect", json_data=bug_data, headers=headers)

        if result.get('status_code') == 200:
            project_num = result.get('data', {}).get('data', {}).get('projectNum')
            print(f"成功创建bug，bug编号: {project_num}")
            return {
                'bug_id': project_num,
                'status': 'success',
                'details': result
            }
        else:
            print(f"创建bug失败: {result}")
            return {
                'bug_id': None,
                'status': 'failed',
                'details': result
            }

def get_assignee_from_test_case(failed_test: dict) -> str:
    """
    根据失败用例的文件名提取模块关键字，并查找配置中的负责人ID
    :param failed_test: 失败的测试用例信息字典
    :return: 负责人ID（字符串）
    """

    def extract_module_key(name: str):
        """
        从测试名称中提取 test_xxx.py 文件名中的完整模块关键字（含 .py）
        示例输入：
            'testcases/test_询报价流程_无PN申请转询价.py::test_询报价流程_申请转询价_无PN申请[chromium]'
        输出：
            'test_询报价流程_无PN申请转询价.py'
        """
        # 提取 :: 左边的部分（即文件路径部分）
        file_part = name.split("::")[0] if "::" in name else name
        # 获取文件名（不含路径）
        filename = Path(file_part).name  # 如 test_询报价流程_无PN申请转询价.py

        # 匹配 test_xxx.py 格式的文件名
        match = re.search(r"(test_.+?\.py)", filename, re.UNICODE)
        if match:
            return match.group(1)  # 返回完整文件名如 test_xxx.py
        return None

    # 尝试从 'name' 中提取模块关键字
    test_name = failed_test.get('name', '')
    module_key = extract_module_key(test_name)

    # 如果没找到，尝试从 'nodeid' 中提取（更可靠）
    if not module_key:
        nodeid = failed_test.get('nodeid', '')
        module_key = extract_module_key(nodeid)

    # 查找配置中的指派人
    if module_key:
        assignee = getattr(globalconfig, "BUG_ASSIGNMENT_RULES", {}).get(module_key)
        if assignee:
            return assignee

    # 返回默认负责人
    return getattr(globalconfig, "DEFAULT_ASSIGNEE", "fallback_id")

# """
# 在文件顶部导入部分添加requests
# import requests
# from typing import Dict, List
#
#
# @pytest.hookimpl(trylast=True)
# def pytest_sessionfinish(session, exitstatus):
#     """增强的测试结束处理"""
#     global _test_results
#
#     # 1. 打印美观的统计结果
#     print("\n" + "="*50)
#     print("测试执行统计".center(50))
#     print("-"*50)
#     print(f"总用例数: {_test_results['total']}")
#     print(f"通过数: \033[32m{_test_results['passed']}\033[0m")
#     print(f"失败数: \033[31m{_test_results['failed']}\033[0m")
#     print(f"跳过数: {_test_results['skipped']}")
#     print("="*50 + "\n")
#
#     # 2. 调试模式下保存失败用例到文件
#     if DEBUG_MODE and _test_results['failed'] > 0:
#         failed_file = Path(".failed_tests.json")
#         with open(failed_file, 'w', encoding='utf-8') as f:
#             json.dump(_test_results['failed_tests'], f, indent=2, ensure_ascii=False)
#         print(f"[调试模式] 已保存失败用例信息到: {failed_file.absolute()}")
#
#     # 3. 实际创建禅道bug
#     if not DEBUG_MODE and _test_results['failed'] > 0:
#         print("\n开始为失败用例创建禅道bug...")
#         for failed_test in _test_results['failed_tests']:
#             _create_zentaobug(failed_test)
#
#     # 保留原有的allure报告处理逻辑
#     allure_report_auto_open_config = session.config.getoption("--allure_report_auto_open")
#     if allure_report_auto_open_config != "off":
#         if sys.platform != "linux":
#             import subprocess
#             import psutil
#             import time
#             def kill_existing_allure_processes():
#                 '''关闭所有运行中的 allure serve 进程'''
#                 killed = False
#                 for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#                     try:
#                         cmdline = proc.info['cmdline']
#                         # 确保是 allure serve 进程
#                         if cmdline and 'allure' in ' '.join(cmdline) and 'serve' in ' '.join(cmdline):
#                             print(f"\nFound existing Allure process (PID: {proc.info['pid']}), terminating...")
#                             psutil.Process(proc.info['pid']).terminate()
#                             killed = True
#                     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#                         continue
#
#                 if killed:
#                     # 给进程一点时间来完全终止
#                     time.sleep(1)
#                 return killed
#
#             try:
#                 # 先尝试关闭已存在的 allure 进程
#                 kill_existing_allure_processes()
#
#                 # 启动新的 allure 服务
#                 allure_command = f'allure serve {allure_report_auto_open_config}'
#                 print(f"Starting new Allure server: {allure_command}")
#                 subprocess.Popen(allure_command, shell=True)
#
#             except Exception as e:
#                 print(f"Error managing Allure process: {str(e)}")
#
# # """
#
#
# def _create_zentaobug(failed_test: Dict) -> None:
#     """创建禅道bug的调试友好版本"""
#     try:
#         bug_data = {
#             "product": "自动化测试",
#             "module": "Playwright测试",
#             "title": f"自动化测试失败: {failed_test['name']}",
#             "steps": f"测试用例 {failed_test['nodeid']} 执行失败\n\n"
#                     f"错误信息:\n{failed_test.get('error', '无详细错误信息')}",
#             "severity": 3,
#             "pri": 2,
#             "openedBuild": "trunk"
#         }
#
#         if DEBUG_MODE:
#             # 调试模式下只打印不实际调用
#             print("\n[调试模式] 模拟创建禅道bug:")
#             print(json.dumps(bug_data, indent=2, ensure_ascii=False))
#             return
#
#         # 实际调用代码
#         response = requests.post(
#             "http://your-zentao-api/bug-create",
#             json=bug_data,
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": "Bearer your_token"
#             }
#         )
#         response.raise_for_status()
#         print(f"成功创建禅道bug: {response.json()}")
#     except Exception as e:
#         print(f"创建禅道bug失败: {str(e)}")
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_logreport(report):
#     """增强的错误信息收集"""
#     global _test_results
#
#     if report.when == 'call':
#         _test_results['total'] += 1
#
#         if report.passed:
#             _test_results['passed'] += 1
#         elif report.failed:
#             error_msg = str(report.longrepr) if hasattr(report, 'longrepr') else None
#             # 提取更详细的错误信息
#             if error_msg and 'AssertionError' in error_msg:
#                 error_msg = error_msg.split('AssertionError:')[-1].strip()
#
#             _test_results['failed'] += 1
#             _test_results['failed_tests'].append({
#                 'name': report.nodeid.split('::')[-1],
#                 'nodeid': report.nodeid,
#                 'error': error_msg,
#                 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
#             })
#         elif report.skipped:
#             _test_results['skipped'] += 1
# import pytest
#
# def pytest_collection_modifyitems(config, items):
#     """根据标记重新排序测试项"""
#     # 分离并行和串行用例
#     parallel = []
#     serial = []
#
#     for item in items:
#         if item.get_closest_marker("parallel"):
#             parallel.append(item)
#         else:
#             serial.append(item)
#
#     # 先执行并行用例，后执行串行用例
#     items[:] = parallel + serial