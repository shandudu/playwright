# 《最新出炉》系列初窥篇-Python+Playwright自动化测试-11-playwright操作iframe-下篇

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://sahitest.com/demo/framesTest.htm")
    # name 属性定位
    frame = page.frame(name="top")
    print(frame)
    browser.close()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://sahitest.com/demo/framesTest.htm")
    # name 属性定位
    frame = page.frame(url="index.htm")
    print(frame)
    browser.close()