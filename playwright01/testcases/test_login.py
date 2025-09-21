from playwright01.testcases import *

def test_login(page: Page):
    my_page = PageIns(page)

    my_page.login_page.login(user="xxx_98", pwd="syx201314")