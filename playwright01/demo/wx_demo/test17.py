from playwright.sync_api import sync_playwright

def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, slow_mo=3000)
    page = browser.new_page()
    page.goto("D:/pythonProject/playwright/playwright01/tests/wx_demo/ModalDialogueBox.html")
    # page.on("dialog", lambda dialog: dialog.accept())
    page.on("dialog", lambda dialog: print(dialog.message))

    # def on_dialog(dialog):
    #     print('Dialog message:', dialog.message)
    #     dialog.accept()
    #
    # page.on('dialog', on_dialog)

    # 点击弹出警告框
    page.locator("#input_1").click()
    # 点击弹出警告框
    page.wait_for_timeout(5000)
    page.locator("#input_2").click()
    # 点击弹出警告框
    page.wait_for_timeout(5000)
    page.locator("#input_3").click()
    browser.close()

def run2(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, slow_mo=3000)
    page = browser.new_page()
    page.on("dialog", lambda dialog: dialog.accept())
    page.on("dialog", lambda dialog: print(dialog.message))
    page.goto("http://news.cyol.com/node_60799.html")
    browser.close()




with sync_playwright() as playwright:
    run(playwright)