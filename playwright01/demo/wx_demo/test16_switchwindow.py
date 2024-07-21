import time

from playwright.sync_api import sync_playwright



def switch_to_page(context, title=None, url=None):
    """切换到指定title 名称的标签页"""
    for item_page in context.pages:
        if title:
            if title in item_page.title():
                # 激活当前选项卡
                item_page.bring_to_front()
                return item_page
        if url:
            if url in item_page.url:
                # 激活当前选项卡
                item_page.bring_to_front()
                return item_page
    else:
        print("not found title")
    return context.pages[0]


with sync_playwright() as playwright:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.baidu.com')
    # 点开多个标签页
    for link in page.locator('#s-top-left>a').all():
        link.click()
    # 遍历page对象
    # print(context.pages)
    # for i in context.pages:
    #     print(i.title())
    page.wait_for_timeout(30_000)
    # page1 = switch_to_page(context, title='百度文库 - 一站式AI内容获取和创作平台')
    page1 = switch_to_page(context, url='https://image.baidu.com/')

    print(page1.title())
    browser.close()

