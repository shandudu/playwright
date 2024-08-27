from playwright.sync_api import Playwright, sync_playwright, expect
# input控件


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/demo/wx_demo/upload_file.html", wait_until="load")
    # 定位选择文件按钮
    page.locator('#pic').set_input_files('D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png')
    #file_input_element.input_file('C:/Users/DELL/Desktop/bjhg.png')
    page.wait_for_timeout(3000)
    print("browser will be close");
    page.close()
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)