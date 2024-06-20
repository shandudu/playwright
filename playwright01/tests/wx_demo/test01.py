import time

from playwright.sync_api import Page, expect, sync_playwright

"""
"""
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.click("input[name='wd']")
    page.fill("input[name='wd']", "chromium")
    time.sleep(1)
    page.screenshot(path=f'example-{p.chromium.name}.png')
    browser.close()


with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.click("input[name='wd']")
    page.fill("input[name='wd']", "chromium")
    time.sleep(1)
    page.screenshot(path=f'example-{p.chromium.name}.png')
    browser.close()


with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print(page.title())
    page.click("input[id='kw']")
    page.fill("input[name='wd']", "chromium")
    time.sleep(1)
    page.screenshot(path=f'example-{p.chromium.name}.png')
    browser.close()