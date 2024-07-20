# context()设置 ignore_https_errors 参数忽略 SSL 错误
#
# ignore_https_errors=True   访问https地址解决安全证书
# viewport={"width": 1920, "height": 1080}  最大化打开浏览器，参数可设置。
# eg：
# context = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
#
# page()设置 ignore_https_errors 参数忽略 SSL 错误，语法如下：
#
# ignore_https_errors=True   访问https地址解决安全证书
# viewport={"width": 1920, "height": 1080}  最大化打开浏览器，参数可设置。
# eg：
# page = browser.new_page(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.wait_for_timeout(3000)
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)


# 除了上一篇中提到的这种方法：playwright 设置 ignore_https_errors 参数忽略 SSL 错误 。后来随着学习和了解还有一种方法：结合 pytest-playwright 用例插件。
"""

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }
    codegen录制用例
    playwright codegen --ignore-https-errors https://example.com
"""

def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_context(
            ignore_https_errors=True,
            viewport={
                "width": 1920,
                "height": 1040,
            }
        )
        page = page.new_page()
        page.goto("https://www.baidu.com")
        assert page.title() == "百度一下，你就知道"
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == '__main__':
    pytest.main(["-v", "test_example.py"])