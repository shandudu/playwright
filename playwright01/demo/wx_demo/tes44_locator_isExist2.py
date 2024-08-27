from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:\\pythonProject\\playwright\\playwright01\\demo\\wx_demo\\test44.html")
    loginButton = page.locator("#bjhg")
    # loginButton.click()

    # 操作隐藏元素
    js = "document.getElementById('bjhg').click()"
    page.wait_for_timeout(10000)
    page.evaluate(js)

    print(loginButton.get_attribute("class"))
    # 通过id定位隐藏元素,然后进行判断(上一篇两种方法)
    print(page.is_visible("#bjhg"))
    print(page.locator("#bjhg").is_visible())
    page.wait_for_timeout(1000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)