from playwright01.testcases import *


def test_login(page: Page):
    login = LoginPage(page)

    login.login(user="xxx_98", pwd="syx201314")