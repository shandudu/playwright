from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/duty/")
    page.wait_for_timeout(1000)
    # page.locator("#draggable").drag_to(page.locator("#droppable"))
    # page.drag_and_drop('#draggable', '#droppable')
    page.locator("//*/p").drag_to(page.locator('//*/ul[@class="privacy-ul-gap"]/li[1]'))
    page.wait_for_timeout(3000)
    # page.pause()
    # page.drag_and_drop('#dragger', 'text=Item 2')
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/html.html")
    page.wait_for_timeout(2000)
    #获取拖动按钮位置并拖动  //*[@id="slider"]/div[1]/div[2]
    dropbutton=page.locator("//*[@id='drag']/div[3]")
    box=dropbutton.bounding_box()
    page.mouse.move(box['x']+box['width']/2,box['y']+box[ 'height']/2)
    page.mouse.down()
    mov_x=box['x']+box['width']/2+390
    page.mouse.move(mov_x,box['y']+box[ 'height']/2)
    page.mouse.up()
    page.wait_for_timeout(3000)
    # page.pause()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run2(playwright)