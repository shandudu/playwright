from playwright01.module import *

class OrderPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "/workbench/mytask"
        self.order_tip = self.page.locator(".anticon-bell")