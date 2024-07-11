from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/html.html")

    iframe = page.frame(name='frameA')
    # 执行js 给输入框输入内容
    js = "document.getElementById('iframeinput').value='北京-宏哥';"
    iframe.evaluate(js)

    page.pause()
    browser.close()