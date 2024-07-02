# 《最新出炉》系列初窥篇-Python+Playwright自动化测试-11-playwright操作iframe-上篇

# locator = page.frame_locator("frame").get_by_text("登录")

# locator = page.frame_locator("my-frame").get_by_text("Submit")
# locator.click()

from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/html.html")
    page.wait_for_timeout(2000)
    # 操作非iframe上的元素
    page.locator('[id="maininput"]').fill("xxx I am a index page's div!")
    # 操作iframe上的元素
    frame = page.frame_locator("iframe[id=frameA]")
    # xpath 匹配
    frame.locator('[id="iframeinput"]').fill('This is a iframe input!')
    page.wait_for_timeout(3000)
    # page.pause()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

