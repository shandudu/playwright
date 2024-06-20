from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.click("input[name='wd']")
    page.fill("input[name='wd']", "chrome1")
    page.screenshot(path=f'example-chromium.png')
    browser.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.click("input[name='wd']")
    page.fill("input[name='wd']", "chrome1")
    page.screenshot(path=f'example-chromium.png')
    browser.close()