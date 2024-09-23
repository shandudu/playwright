from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/demo/wx_demo/canvas.html")
    page.wait_for_timeout(1000)

    # svg元素拖拽
    page.mouse.move(x=40, y=40)
    page.mouse.down()
    page.mouse.move(x=100, y=100)
    page.mouse.up()
    page.wait_for_timeout(5000)
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)