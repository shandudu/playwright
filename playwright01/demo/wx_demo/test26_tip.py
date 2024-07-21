import pytest
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/toast.html", wait_until="load")
    # page.get_by_role(role="button", name="点击关注").click()
    page.locator('#hongge').click()
    # expect(page.locator('//div[text()="感谢关注：北京-宏哥"]')).to_have_text('感谢关注：北京-宏哥')
    text = page.locator('//div[text()="感谢关注：北京-宏哥"]').inner_text()
    assert text == '感谢关注：北京-宏哥'
    page.wait_for_timeout(1000)
    context.close()
    browser.close()


def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://login.anjuke.com/login/form?history=aHR0cHM6Ly9iZWlqaW5nLmFuanVrZS5jb20v",
              wait_until="networkidle")
    frame = page.frame_locator('//iframe[@id="iframeLoginIfm"]')
    frame.locator('#phoneIpt').fill('18888888888')
    frame.locator('#smsIpt').fill('234567')
    frame.locator('#checkagree').click()
    frame.locator('#smsSubmitBtn').click()
    toast_text = frame.get_by_text('请获取验证码')
    page.wait_for_timeout(3000)
    #page.pause()
    print("Toast text is", toast_text.inner_text())
    context.close()
    browser.close()


'//div[text()="请获取验证码"]'

with sync_playwright() as playwright:
    run2(playwright)
