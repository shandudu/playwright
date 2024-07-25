
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator('#kw').highlight()
    # page.get_by_text('新闻').highlight()
    page.get_by_text('新闻').nth(0).highlight()
    page.wait_for_timeout(3000)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)