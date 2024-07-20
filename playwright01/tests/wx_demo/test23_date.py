from playwright.sync_api import Playwright, sync_playwright

# # 原生js，移除元素的readonly属性
# js1 = 'document.getElementById("createTime").removeAttribute("readonly");'
# page.evaluate(js1)
# # 直接给输入框输入日期
# js2 = 'document.getElementById("createTime").value="2023-11-11";'
# page.evaluate(js2)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.12306.cn/index/")
    page.wait_for_timeout(5000)
    page.locator('#train_date').click()
    page.locator('//div[text()="今天"]/parent::div/following-sibling::div[1]').click()

    page.wait_for_timeout(3000)
    browser.close()


def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.jq22.com/demo/jquery-rq-150115222509/")
    page.wait_for_timeout(5000)
    page.locator('#beginTime').fill('2026-08-18')
    page.locator('#endTime').fill('2030-08-18 10:34')
    # page.locator('#beginTime').click()
    # page.locator(data_choice('yearwrapper', '2025年')).click()
    # page.locator(data_choice('monthwrapper', '08月')).click()
    # page.locator(data_choice('daywrapper', '19日')).click()

    page.wait_for_timeout(3000)
    browser.close()


def data_choice(type, value):
    """
    :type type: 时间类型
    :type value: 时间值
    """
    xpath = '//div[@id="datescroll"]//div[@id="{type}"]/ul/li[text()="{value}"]'.format(type=type, value=value)
    return xpath


def run3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/date.html", wait_until="load")
    page.wait_for_timeout(5000)
    # 原生js，移除元素的readonly属性
    js1 = 'document.getElementById("Dateinput").removeAttribute("readonly");'
    page.evaluate(js1)
    # 直接给输入框输入日期
    js2 = 'document.getElementById("Dateinput").value="2023-11-11";'
    page.evaluate(js2)

    page.wait_for_timeout(3000)
    browser.close()

with sync_playwright() as playwright:
    run3(playwright)
