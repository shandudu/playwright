from playwright01.module import *
from playwright01.module.BasePage import PageObject


class Baidu(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.baidu.com/"
        self.searh_input = self.page.locator("input[name=wd]")

    def baidu_srarch(self, search_keyword, search_result):
        self.navigate()
        self.searh_input.fill(search_keyword)
        self.click_button("百度一下")
        expect(self.page.get_by_text(search_result)).to_be_visible()