# 《最新出炉》系列初窥篇-Python+Playwright自动化测试-11-playwright操作iframe-中篇


from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mail.qq.com/")
    page.wait_for_timeout(2000)
    # 点击qq登录
    # page.locator("#QQMailSdkTool_login_loginBox_tab_item_qq").click()
    page.locator("xpath=//div[@id='QQMailSdkTool_login_loginBox_tab_item_qq']").click()
    # 操作iframe上的元素
    # frame = page.frame_locator('[class="QQMailSdkTool_login_loginBox_qq_iframe"]').frame_locator("#ptlogin_iframe")
    frame = page.frame_locator('xpath=//iframe[@class="QQMailSdkTool_login_loginBox_qq_iframe"]').frame_locator('xpath=//iframe[@name="ptlogin_iframe"]')
    #点击密码登录
    frame.locator("#switcher_plogin").click()
    frame.locator('input#u').fill('北京-宏哥')
    frame.locator('input#p').fill("123456")
    frame.locator('input#login_button').click()
    print("运行成功")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

