from playwright.sync_api import sync_playwright

def baidu_t():
    playwright = sync_playwright()
    browser = playwright.start().chromium.launch(headless=False)
    context = browser.new_context(

            viewport= {
              "width": 1920,
              "height": 1080
            }

    )
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.screenshot(path="baidu.png")
    print('baidu')


def test_taobao(page):
    page.goto("https://www.taobao.com/")
    page.screenshot(path="taobao.png")
    print('taobao')


if __name__ == "__main__":
    baidu_t()
