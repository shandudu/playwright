from playwright01.module import *



class PageIns:
    def __init__(self, page: Page):
        self.page = page
        self.baidu_page = Baidu(self.page)
        self.login_page = LoginPage(self.page)
        self.order_page = OrderPage(self.page)


