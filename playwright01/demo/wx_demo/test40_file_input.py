from playwright.sync_api import Playwright, sync_playwright, expect
# 非input控件

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.jq22.com/demo/preview201801282117/")
    page.wait_for_timeout(100)

    with page.expect_file_chooser() as fc_info:
        page.locator("//html/body/div/div/div[1]/img[1]").click()  # 点击上传附件按钮
    # page.pause()
    file_chooser = fc_info.value
    file_chooser.set_files('D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png') # 上传文件
    # 为了清楚看到上传后的图片，宏哥加大了等待时间
    page.wait_for_timeout(10000)
    print("browser will be close");
    page.close()
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)