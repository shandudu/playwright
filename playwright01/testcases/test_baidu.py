from playwright01.testcases import *


def test_baidu(page: Page):
    baidu = Baidu(page)
    # baidu.navigate()
    # baidu.searh_input.fill("playwright")
    # baidu.click_button("百度一下")
    # expect(page.get_by_text("https://github.com/microsoft/playwright")).to_be_visible()
    baidu.baidu_srarch(search_keyword="playwright", search_result="https://github.com/microsoft/playwright")