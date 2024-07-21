from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/radio.html", wait_until="networkidle")
    page.get_by_role(role="checkbox", name="李白", checked=False).set_checked(True)
    page.locator('[name="checkbox2"]').click()
    page.locator('[name="checkbox4"]').set_checked(True)

    # page.get_by_text('孙尚香 ').last.click()
    page.get_by_text('孙尚香 ').check()
    page.wait_for_timeout(1000)
    context.close()
    browser.close()


def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/radio.html", wait_until="networkidle")
    page.wait_for_timeout(3000)
    # 选择点击 韩信
    page.locator('[value="李白"]').click()
    state = page.locator('[value="李白"]').is_checked()
    print(state)
    page.wait_for_timeout(2000)
    page.locator('[value="李白"]').check()
    page.wait_for_timeout(2000)
    state = page.locator('[value="李白"]').uncheck()
    page.wait_for_timeout(2000)
    print(state)
    # page.pause()
    browser.close()


def run3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/radio.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    for radio in page.locator('[type="radio"]').all():
        if not (radio.is_checked()):
            radio.click()

    page.wait_for_timeout(1000)
    # page.pause()
    browser.close()


def run4(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/radio.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    for radio in page.locator('[type="checkbox"]').all():
        if not (radio.is_checked()):
            radio.click()

    page.wait_for_timeout(1000)
    # page.pause()
    browser.close()


def run5(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.jq22.com/demo/inputStyle201703310052", wait_until="networkidle")
    page.wait_for_timeout(1000)
    for radio in page.locator('[type="radio"]').all():
        if not (radio.is_checked()):
            radio.click()

    page.wait_for_timeout(1000)
    # page.pause()
    browser.close()


def run6(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.jq22.com/demo/inputStyle201703310052", wait_until="networkidle")
    page.wait_for_timeout(1000)
    for radio in page.locator('[type="checkbox"]').all():
        if not (radio.is_checked()):
            radio.click()

    page.wait_for_timeout(1000)
    # page.pause()
    browser.close()


def run7(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.wjx.cn/m/2792226.aspx/")
    page.wait_for_timeout(5000)
    page.locator('//input[@id="q1_1"]/following-sibling::a').click()
    page.locator('//input[@id="q2_2"]/following-sibling::a').click()
    page.locator('//input[@id="q3_4"]/following-sibling::a').click()
    page.locator('//input[@id="q4_2"]/following-sibling::a').click()

    for radio in page.locator('//input[@type="checkbox" and @name="q5"]//following-sibling::a').all():
        radio.click()
    page.locator('//input[@id="q6_2"]/following-sibling::a').click()
    page.locator('//input[@id="q7_4"]/following-sibling::a').click()
    page.locator('//input[@id="q8_3"]/following-sibling::a').click()
    page.locator('//input[@id="q9_3"]/following-sibling::a').click()
    page.wait_for_timeout(10000)
    # page.pause()
    browser.close()


with sync_playwright() as playwright:
    run7(playwright)
