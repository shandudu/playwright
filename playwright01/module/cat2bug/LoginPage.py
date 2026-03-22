from playwright01.module import *


class CatLoginPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "/index#/login?redirect=%2Findex"
        self.user = self.page.get_by_placeholder("账号")
        self.pwd = self.page.get_by_placeholder("密码")
        self.state = self.page.get_by_text('首页').first


    def login(self, user, pwd):
        self.navigate()
        self.user.fill(user)
        self.pwd.fill(pwd)
        self.click_button("登陆")
        expect(self.state).to_be_visible()
