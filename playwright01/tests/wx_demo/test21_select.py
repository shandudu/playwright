from playwright.sync_api import Playwright, sync_playwright, expect

# # Single selection matching the value
# page.get_by_label('Choose a color').select_option('blue')
#
# # Single selection matching the label
# page.get_by_label('Choose a color').select_option(label='Blue')
#
# # Multiple selected items
# page.get_by_label('Choose multiple colors').select_option(['red', 'green', 'blue'])


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/select.html", wait_until="load")
    page.wait_for_timeout(1000)
    # page.select_option("#select_id", "河北")
    select = page.get_by_label("快递邮寄地址：")
    # option = select.select_option(value="四川")
    # option = select.select_option(index=1)
    # option = select.select_option(label="第五")
    page.select_option("#select_id", "3")
    page.wait_for_timeout(3000)
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.12306.cn/index/", wait_until="networkidle")
    page.locator("#fromStationText").click()

    page.locator('//li[text()="北京"]').click()
    page.wait_for_timeout(1000)
    # page.locator("toStationText").click()
    page.locator('//li[text()="上海"]').click()
    page.wait_for_timeout(1000)
    page.locator('#search_one').click()
    page.wait_for_timeout(1000)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run2(playwright)
