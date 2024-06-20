"""
playwright通过slow_mo （单位是毫秒）减慢执行速度，它的作用范围是全局的，从启动浏览器到操作元素每个动作都会有等待间隔，方便在出现问题的时候看到页面操作情况
"""
from playwright.async_api import Page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1_000)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.fill('#kw', "xxxtenction")
    page.click('#su')
    page.wait_for_timeout(1_000)
    browser.close()



    # # 固定等待1秒
    # page.wait_for_timeout(1_000)
    # # 等待事件
    # page.wait_for_timeout(event)
    # # 等待加载状态
    # page.get_by_role("button").click()
    # page.wait_for_load_state()
"""
定位方式
    page.locator("xpath=//h2")
    page.locator("text=文本输入")
    page.locator("#s-usersetting-top")
    page.locator("input[name='wd']").click()
    page.get_by_role("button", name="百度一下").click()
    page.get_by_placeholder("搜索").click()
    page.get_by_text("搜索").click()  建议使用文本定位器来查找非交互式元素，如div, span, p 等。对于交互式元素，如请button, a, input, 使用角色定位器。
    page.get_by_label("Password").fill("secret")
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1_000)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    page.locator('input[name="wd"]').fill("xxx")
    page.get_by_role("button", name="百度一下").click()