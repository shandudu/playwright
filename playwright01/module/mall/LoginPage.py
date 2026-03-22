from playwright01.module import *


class MallLoginPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "/admin/index.html#/login"
        self.user = self.page.get_by_placeholder("请输入用户名")
        self.pwd = self.page.get_by_placeholder("请输入密码")
        self.state = self.page.locator('//span[@class="el-breadcrumb__item"]').first
        self.state2 = self.page.locator('//span[@class="el-breadcrumb__item2"]').first


    def login(self, user, pwd):
        self.navigate()
        self.user.fill(user)
        self.pwd.fill(pwd)
        self.click_button("登录")
        expect(self.state2).to_be_visible(timeout=2_000)