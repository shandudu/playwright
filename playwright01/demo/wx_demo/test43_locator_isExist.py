from playwright.sync_api import Playwright, sync_playwright, expect
"""
page对象调用的判断方法, 传一个selector 定位参数
page.is_checked(selector: str) # checkbox or radio 是否选中
page.is_disabled(selector: str) # 元素是否可以点击或编辑
page.is_editable(selector: str) # 元素是否可以编辑
page.is_enabled(selector: str) # 是否可以操作
page.is_hidden(selector: str) # 是否隐藏
page.is_visible(selector: str) # 是否可见

locator对象调用的判断方法
locator.is_checked()
locator.is_disabled()
locator.is_editable()
locator.is_enabled()
locator.is_hidden()
locator.is_visible()

元素句柄的判断方法
element_handle.is_checked()
element_handle.is_disabled()
element_handle.is_editable()
element_handle.is_enabled()
element_handle.is_hidden()
element_handle.is_visible()
"""

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator('//a[@id="s-top-loginbtn"]').click()
    page.get_by_placeholder('手机号/用户名/邮箱').fill('2232275482@qq.com')
    page.get_by_placeholder('密码').fill('syx201314')
    page.locator("//input[@id='TANGRAM__PSP_11__isAgree']").click()
    page.locator('//input[@class="pass-button pass-button-submit"]').click()
    page.wait_for_timeout(1000)
    error_message = page.locator("//p[text()='邮箱 22...2@qq.com 是否可用于验证']")
    if error_message.is_visible():
        print("宏哥！元素存在")
    else:
        print("宏哥！元素不存在")

    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)