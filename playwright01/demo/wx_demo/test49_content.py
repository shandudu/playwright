from playwright.sync_api import Playwright,sync_playwright,expect

def run(playwright:Playwright)->None:

    browser=playwright.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()
    page.goto("https://www.cnblogs.com/du-hong", wait_until='networkidle')
    # page.goto("https://www.baidu.com", wait_until='networkidle')

    #获取某个元素的HTML
    blog=page.locator('#blogTitle')
    print(blog.inner_html())
    print('-------------北京-宏哥----------------------')
    print(blog.inner_text())
    page.wait_for_timeout(5000)#强制等待5秒
    print('*********************')
    print(blog.all_inner_texts())
    print('*********************')
    print(blog.all_text_contents())
    page.wait_for_timeout(5000)#强制等待5秒
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)