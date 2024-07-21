import base64

from playwright.sync_api import Playwright, sync_playwright, expect

"""
screenshot方法可以进行截图，参数如下:

timeout:以毫秒为单位的超时时间，0为禁用超时

path:设置截图的路径

type：图片类型，默认jpg

quality：像素，不适用于jpg

omit_background: 隐藏默认白色背景，并允许捕获具有透明度的屏幕截图。不适用于“jpeg”图像。

full_page：如果为true，则获取完整可滚动页面的屏幕截图，而不是当前可见的视口。默认为

`假`。

clip：指定结果图像剪裁的对象clip={'x': 10 , 'y': 10, 'width': 10, 'height': 10}
"""


def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.screenshot(path='a.png', full_page=True)  # 截图
    print(page.title())
    page.wait_for_timeout(1000)
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    element_handle = page.query_selector("#form")  # 按照元素截图
    element_handle.screenshot(path="screenshot.png")
    print(page.title())
    page.wait_for_timeout(1000)
    context.close()
    browser.close()

def run3(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    screenshot_bytes = page.screenshot()
    print(base64.b64encode(screenshot_bytes).decode())
    page.wait_for_timeout(1000)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run3(playwright)