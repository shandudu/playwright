from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.w3cschool.cn/")
    page.wait_for_timeout(2000)
    # 点击的时候会自动滚动
    page.locator('[alt="软件测试教程"]').click()
    page.wait_for_timeout(5000)
    # #page.pause()
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.douban.com/")
    page.wait_for_timeout(2000)
    # 点击的时候会自动滚动
    # 让元素出现到窗口的可视范围
    page.get_by_text('选电影').scroll_into_view_if_needed()
    page.wait_for_timeout(5000)
    page.get_by_text('选电影').hover()
    page.wait_for_timeout(5000)
    # #page.pause()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run2(playwright)