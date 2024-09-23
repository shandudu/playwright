from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/demo/wx_demo/svg.html")
    page.wait_for_timeout(1000)
    # svg元素定位
    circle = page.locator('//*[name()="svg"]/*[name()="circle"]')
    print(circle.bounding_box())
    box = circle.bounding_box()
    # svg元素拖拽
    page.mouse.move(x=box['x'] + box['width'] / 2, y=box['y'] + box['height'] / 2)
    page.mouse.down()
    page.mouse.move(x=box['x'] + box['width'] / 2 + 100, y=box['y'] + box['height'] / 2)
    page.mouse.up()
    page.wait_for_timeout(5000)
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)