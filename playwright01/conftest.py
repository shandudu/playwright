import re

import pytest
from playwright.sync_api import BrowserContext, Page
from playwright01.utils.globalMap import GlobalMap
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Union,
    Pattern,
    cast,
)


# @pytest.fixture()
# def hello_world():
#     print("hello")
#     yield
#     print("world")
#
# @pytest.fixture
# def page(context: BrowserContext) -> Page:
#     print("this my page")
#     return context.new_page()

@pytest.fixture(scope="session", autouse=True)
def test_init(base_url):
    global_map = GlobalMap()
    global_map.set('baseurl', base_url)
    env = re.search("(https://)(.*)(.ezone.work)", base_url).group(2)
    global_map.set('env', env)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig: Any):
    width, height = pytestconfig.getoption("--viewport")
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {
            "width": width,
            "height": height,
        },
        "record_video_size": {
            "width": width,
            "height": height,
        }
    }


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright", "Playwright")
    group.addoption(
        "--viewport",
        action="store",
        default=[1440, 1000],
        help="Viewport size",
        type=int,
        nargs=2,
    )
