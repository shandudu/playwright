from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080},)
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.fill("input[name=wd]", "xxx")
    page.click('text=百度一下')
    page.wait_for_timeout(1_000)
    page.reload()
    page.wait_for_timeout(1_000)
    page.go_back()
    page.wait_for_timeout(1_000)
    page.go_forward()
    page.wait_for_timeout(1_000)
    context.close()
    browser.close()