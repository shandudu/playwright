from playwright.sync_api import Playwright, sync_playwright, expect
# 非input控件

# # Select one file    选择一个文件
# page.get_by_label("Upload file").set_input_files('myfile.pdf')
#
# # Select multiple files   选择多个文件
# page.get_by_label("Upload files").set_input_files(['file1.txt', 'file2.txt'])
#
# # Remove all the selected files  移除所有文件
# page.get_by_label("Upload file").set_input_files([])
#
# # Upload buffer from memory  从缓存中上传
# page.get_by_label("Upload file").set_input_files(
#     files=[
#         {"name": "test.txt", "mimeType": "text/plain", "buffer": b"this is a test"}
#     ],
# )

from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.jq22.com/demo/jstpsc202005191001")
    # 定位选择文件按钮
    page.locator('#upload-input').set_input_files(['D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png','D:/pythonProject/playwright/playwright01/demo/wx_demo/file/user.jpg'])
    #file_input_element.input_file('C:/Users/DELL/Desktop/bjhg.png')
    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()

def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.jq22.com/demo/easyUpload201801161800")
    with page.expect_file_chooser() as fc_info:
        page.locator('//*[@id="easy1"]/div[2]/div[1]').click()  # 点击选择文件按钮
    # page.pause()
    file_chooser = fc_info.value
    file_chooser.set_files(['D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png','D:/pythonProject/playwright/playwright01/demo/wx_demo/file/user.jpg']) # 上传文件
    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()

def run3(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://graph.baidu.com/pcpage/index?tpl_from=pc")
    page.locator('//span[@class="graph-d20-search-wrapper-camera"]').click()
    with page.expect_file_chooser() as fc_info:
        page.locator('//input[@type="file"]').click()  # 点击选择文件按钮
    # page.pause()
    file_chooser = fc_info.value
    file_chooser.set_files('D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png')
    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()


def run4(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://graph.baidu.com/pcpage/index?tpl_from=pc")
    page.locator('//span[@class="graph-d20-search-wrapper-camera"]').click()

    page.locator('//input[@type="file"]').set_input_files('D:/pythonProject/playwright/playwright01/demo/wx_demo/file/xxx.png')
    # page.pause()
    page.wait_for_timeout(10000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run4(playwright)