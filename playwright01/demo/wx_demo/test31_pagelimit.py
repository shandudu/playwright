# 分页测试
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.jq22.com/demo/jqueryPager202102221221/")
    # 获得所有分页的数量
    # -4是因为要去掉首页、上一个（«）和下一个（»）'[name="radio"]'
    # total_pages = page.locator('//*[@id="page"]/ul/li').count()-4
    # print("Total page is", total_pages)
    # for li in page.locator('//*[@id="page"]/ul/li').all():
    #     page.locator("//div[@id='page']/ul/li[8]").click()
    #     page.wait_for_timeout(300)
    # # 当前页面是第几页
    # current_page = page.locator("#page>> ul >> li.active")
    # print("Current page is", current_page.text_content())
    ###############
    page.get_by_text('末页').click()
    text_num = page.locator('//li[@class="active"]').inner_text()
    print(text_num)
    page.get_by_text('首页').click()
    first_num = page.locator('//li[@class="active"]').inner_text()
    for i in range(3, int(text_num) + 3 ):
        # page.locator('//li[{i}]'.format(i=i)).click()
        # num = page.locator('//li[{i}]'.format(i=i)).inner_text()
        page.locator("//div[@id='page']/ul/li[8]").click()
        num = page.locator("//div[@id='page']/ul/li[8]").inner_text()
        print('下标——', i)
        print('实际值', num)
        page.wait_for_timeout(1000)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)