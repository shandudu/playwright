from playwright.sync_api import Playwright, sync_playwright, expect




def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://sahitest.com/demo/saveAs.htm")
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.get_by_text("testsaveas.zip").click()
    download = download_info.value
    download.save_as("D:/pythonProject/playwright/playwright01/demo/wx_demo/file" + download.suggested_filename)
    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)