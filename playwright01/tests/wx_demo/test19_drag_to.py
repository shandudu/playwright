from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://jqueryui.com/resources/demos/droppable/default.html")
    page.wait_for_timeout(1000)
    # page.locator("#draggable").drag_to(page.locator("#droppable"))
    # page.drag_and_drop('#draggable', '#droppable')
    page.locator('#draggable').hover()
    page.mouse.down()
    page.locator('#droppable').hover()
    page.mouse.up()
    page.wait_for_timeout(3000)
    # page.pause()
    # page.drag_and_drop('#dragger', 'text=Item 2')
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)