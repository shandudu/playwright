from playwright01.testcases import *


def test_login_and_baidu(page: Page):
    my_page = PageIns(page)
    my_page.baidu.baidu_srarch(search_keyword="playwright", search_result="https://github.com/microsoft/playwright")
    my_page.login.login(user="xxx_98", pwd="syx201314")