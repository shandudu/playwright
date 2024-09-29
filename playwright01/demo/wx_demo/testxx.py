from playwright.sync_api import Playwright,sync_playwright,expect

def run(playwright:Playwright)->None:

    browser=playwright.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://vxetable.cn/v4/#/component/grid/checkbox/highlight", wait_until='networkidle')
    # page.goto("https://www.baidu.com", wait_until='networkidle')
    # page.locator('//span[@title="全选/取消"]').click()
    # 获取某个元素的HTML
    blog=page.locator('//span[@title="全选/取消"]').get_attribute(name='class')
    print(blog)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)