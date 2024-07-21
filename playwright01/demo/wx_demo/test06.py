from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    # context = browser.new_context(no_viewport=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.pause()
    context.close()
    browser.close()
    print("关闭")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    # context = browser.new_context(no_viewport=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    context2 = browser.new_context()
    page = context.new_page()
    page2 = context2.new_page()
    page.goto("https://www.baidu.com")
    page2.goto("https://www.bilibili.com")
    page.pause()
    page2.pause()
    context.close()
    browser.close()
    print("关闭")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    # context = browser.new_context(no_viewport=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1000})
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.pause()
    with context.expect_page() as new_page_info:
        page.click('text=hao123')
    new_page = new_page_info.value
    new_page.click("text=hao123推荐")
    context.close()
    browser.close()
    print("关闭")