import os
import shutil
import pytest
import glob
from playwright01.utils.logger import logger

# 控制是否启用多线程
enable_multi_threading = False


def clear_directories():
    dirs_to_clear = ["../.allure_report", "../.test_result"]
    for d in dirs_to_clear:
        if os.path.exists(d):
            shutil.rmtree(d)
            logger.info(f"(run.py文件直接调用) 清理 Allure 报告目录: {d}")
        os.makedirs(d, exist_ok=True)
        logger.info(f"(run.py文件直接调用) 重新生成 Allure 报告目录: {d}")

    # 清理禅道bug相关的临时文件
    temp_bug_dir = os.path.join(os.path.dirname(__file__), ".temp", "bug_files")
    if os.path.exists(temp_bug_dir):
        try:
            shutil.rmtree(temp_bug_dir)
            logger.info(f"(run.py文件直接调用) 清理bug临时目录: {temp_bug_dir}")
        except Exception as e:
            logger.warning(f"清理bug临时目录失败 {temp_bug_dir}: {e}")

    # 重新创建目录
    os.makedirs(temp_bug_dir, exist_ok=True)
    logger.info(f"(run.py文件直接调用) 创建禅道bug临时目录: {temp_bug_dir}")


if __name__ == "__main__":
    # 设置环境变量，告诉 conftest.py "我已经清理过了"
    os.environ["TEST_CLEANUP_DONE"] = "1"  # 关键！

    clear_directories()  # 执行清理

    if enable_multi_threading:
        # 并行执行带 @pytest.mark.parallel 的用例（3个进程）
        pytest.main([
            "-m", "parallel",
            "-n", "3",
            "-v",
            "--alluredir=../.allure_report",
        ])

        # 串行执行带 @pytest.mark.serial 的用例（主进程）
        # pytest.main([
        #     # "-m", "serial",
        #     "-m", "not parallel",  # 执行非parallel表示的用例，除了parallel表示，别的不管什么标识都会执行
        #     "-v",
        #     "--alluredir=../.allure_report",
        # ])
    else:
        # 单线程运行全部用例
        pytest.main([
            "-v",
            "--alluredir=../.allure_report",
        ])