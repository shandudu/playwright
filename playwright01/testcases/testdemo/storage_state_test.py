
from playwright01.testcases import *


def test_storage_state(page: Page, browser: Browser):
    my_page = PageIns(page)
    my_page.baidu.baidu_srarch(search_keyword="playwright", search_result="https://github.com/microsoft/playwright")
    my_page.login.login(user="xxx_98", pwd="syx201314")
    my_page.page.context.storage_state(path="xxx_98.json")
    context = browser.new_context(storage_state="xxx_98.json")
    page = context.new_page()
    page.goto("https://xxxdd.ezone.work/workbench/myapproval")
    page