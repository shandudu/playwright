from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/demo/wx_demo/breadcrumb.html", wait_until="load")
    page.wait_for_timeout(1000)
    # 获得其父层级 //div[@class="SignFlowInput"] >> //input[@name="password"]
    ancestors = page.locator('//ol[@class="breadcrumb"]/li/a').all()
    for  link in ancestors:
        print(link.inner_text())
    # 获取当前层级
    # 由于页面上可能有很多class为active的元素
    # 所以使用层级定位最为保险
    current = page.locator('//ol[@class="breadcrumb"] >> //li[@class="active"]')
    print(current.inner_text())
    page.wait_for_timeout(1000)
    print("browser will be close");
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
