# 页面滚动条，滚动直到此出现元素
# page.locator("//div[contains(@class, 'react-grid-item')][last()]").scroll_into_view_if_needed()
# 元素说明：找到class里包含‘react-grid-item’属性最后一个属性

# # 光标移动至滚动条所在框中
# page.click("div.content-main")
# # 滚动鼠标 , 参数给一个较大值，以保证直接移动至最后
# page.mouse.wheel(0,10000)

# page.evaluate("var q=document.documentElement.scrollTop=滚动条的位置")

from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.163.com/")
    page.locator('//*[@id="lazy_subfoot_js"]/div/div/div[2]/div[2]/p[5]/a').click()
    page.locator('//*[@id="lazy_subfoot_js"]/div/div/div[1]/div/div[1]/div[3]/a[5]').scroll_into_view_if_needed()
    page.wait_for_timeout(2000)
    page.close()
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.163.com/")
    # 光标移动至滚动条所在框中
    page.click("#ne_wrap")
    # 滚动鼠标 , 参数给一个较大值，以保证直接移动至最后
    page.mouse.wheel(0, 10000)
    page.wait_for_timeout(2000)
    page.close()
    context.close()
    browser.close()

def run3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.163.com/")
    page.evaluate("var q=document.documentElement.scrollTop=50000")
    page.mouse.wheel(0,7000)
    page.wait_for_timeout(2000)
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run3(playwright)