from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:

    def mouse_operate():
        # https://draw.yunser.com/
        page.mouse.move(350, 200)
        page.mouse.down()
        page.mouse.move(350, 300)
        page.mouse.move(450, 300)
        page.mouse.move(450, 200)
        page.mouse.move(350, 200)
        page.mouse.up()

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://draw.yunser.com/")
    page.wait_for_timeout(1000)
    mouse_operate()
    page.wait_for_timeout(1000)
    # page.pause()
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cps-check.com/cn/mouse-buttons-test", wait_until="load")
    page.wait_for_timeout(1000)
    #将鼠标移到测试框内
    page.mouse.move(650,300)
    #按下左键
    page.mouse.down()
    page.wait_for_timeout(20000)
    #释放
    page.mouse.up()
    page.wait_for_timeout(2000)
    #page.pause()
    context.close()
    browser.close()

def run3(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.runoob.com/")
    page.wait_for_timeout(1000)
    for i in range(50):
        page.mouse.wheel(0, 100)
        page.wait_for_timeout(500)
    #page.pause()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run3(playwright)