# 《最新出炉》系列初窥篇-Python+Playwright自动化测试-11-playwright操作iframe-中篇


from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mail.163.com/")
    page.wait_for_timeout(2000)
    # 操作iframe上的元素
    # frame = page.frame_locator('xpath=//div[@id="loginDiv"]/iframe')
    # iframe id是动态变化的用正则表达式
    frame = page.frame_locator('[id^="x-URS-iframe"]')
    print(frame)
    # 点击密码登录
    frame.locator("input[name='email']").fill('北京-宏哥')
    frame.locator("input[name='password']").fill("123456")
    frame.locator('a#dologin').click()
    print("运行成功")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
