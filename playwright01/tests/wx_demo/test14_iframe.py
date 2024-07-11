from playwright.sync_api import sync_playwright


def handler(dialog):
    print("监听dialog 事件")
    print(dialog.message)
    # dialog.accept()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://sahitest.com/")

    page.on("dialog", handler)

    # 执行JavaScript
    page.evaluate("alert('hello world')")

    #page.pause()
    browser.close()