from playwright01.module import *



class PageIns:
    def __init__(self, page: Page):
        self.page = page
        self.baidu = Baidu(self.page)
        self.login = LoginPage(self.page)


