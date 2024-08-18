from playwright01.module import *
from playwright01.module.BasePage import PageObject

class OrderPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "/workbench/mytask"
        self.order_tip = self.page.locator(".anticon-bell")