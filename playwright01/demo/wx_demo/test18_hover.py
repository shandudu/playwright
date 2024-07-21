
from playwright.sync_api import Page, expect, sync_playwright


# def test_pw_hover(page: Page) -> None:
#     page.goto("https://www.baidu.com/", wait_until="networkidle")
#     page.locator("a[name='tj_briicon']").hover()
#     page.locator('xpath=//div[text()="百科"]').click()
#     page.wait_for_timeout(9000)


def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, slow_mo=3000)
    page = browser.new_page()
    page.goto("https://wwww.baidu.com")
    page.wait_for_timeout(3000)
    page.fill("input[name=\"wd\"]", "selenium ap")
    page.wait_for_timeout(3000)
    #自动补全其中一个选择项
    auto_text = page.locator("//*[@id='form']/div/ul/li[@data-key='selenium app自动化']").click()
    page.wait_for_timeout(3000)
    page.click("text=百度一下")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)