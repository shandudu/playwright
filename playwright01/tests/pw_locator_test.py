from playwright.sync_api import Page, expect,  Playwright


def test_get_by_role(page: Page, hello_world):
    """

    :param page:
    :return:
    """
    page.goto("/demo/dialog", wait_until="networkidle")
    page.get_by_text(text="点我开启一个dialog").click()
    expect(page.get_by_role(role="dialog")).to_be_visible()
    page.goto("/demo/checkbox", wait_until="networkidle")
    page.get_by_role(role="checkbox", name="开发", checked=False).set_checked(True)
    page.get_by_role(role="checkbox", name="开发", checked=True).set_checked(False)
    page.goto("/demo/table", wait_until="networkidle")
    expect(page.get_by_role(role="table")).to_be_visible()
    expect(page.get_by_role(role="cell")).to_have_count(count=13)
    expect(page.get_by_role(role="img", include_hidden=True)).to_have_count(count=4)
    page.goto("/demo/grid", wait_until="networkidle")
    expect(page.get_by_role("treegrid")).to_be_visible()
    expect(page.get_by_role("row").filter(has_text="溜达王").locator("div").nth(1)).to_have_text("44")



def test_get_by_text(page: Page):
    page.goto("/demo/getbytext", wait_until="networkidle")
    expect(page.get_by_text(text="确定")).to_have_count(3)
    expect(page.get_by_text("确定", exact=True)).to_have_count(2)
    expect(page.get_by_text("确定 确认 肯定")).to_have_count(1)


def test_get_by_label(page: Page):
    page.goto("/demo/input", wait_until="networkidle")
    page.get_by_label("输入你想输入的任何文字").fill("1234567")


def test_get_by_placeholder(page: Page):
    page.goto("/demo/input", wait_until="networkidle")
    page.get_by_placeholder("超过10位小数会被截取").fill("12345627")


def test_get_by_title(page: Page):
    page.goto("/demo/image", wait_until="networkidle")
    expect(page.get_by_title("这是一个title")).to_be_visible()


def test_get_by_alt_text(page: Page):
    page.goto("/demo/image", wait_until="networkidle")
    expect(page.get_by_alt_text("这是图片占位符")).to_be_visible()
    expect(page.get_by_alt_text("图片占位符")).to_be_visible()


def test_get_by_test_id(page: Page, playwright: Playwright):
    page.goto("/demo/image", wait_until="networkidle")
    playwright.selectors.set_test_id_attribute("my_test_id")
    expect(page.get_by_test_id("Howls Moving Castle")).to_be_visible()


def test_and_or(page: Page)


def test_nth_all(page: Page):
    page.goto("https://www.taobao.com", wait_until="load")
    expect(page.locator("[aria-label='查看更多']").last).to_contain_text("图书")
    expect(page.locator("[aria-label='查看更多']").first).to_contain_text("办公")
    expect(page.locator("[aria-label='查看更多']").nth(0)).to_contain_text("办公")
    expect(page.locator("[aria-label='查看更多']").nth(-1)).to_contain_text("图书")
    for _ in page.locator("[aria-label='查看更多']").all():
        print(_.text_content())
    print('完成')
    print('完成')


def test_frame_locator(page: Page):
    page.goto("/demo/iframe", wait_until="load")
    baidu = page.frame(url="https://www.baidu.com/")
    baidu.fill('#kw', '百度一下')
    page.frame_locator("//iframe[@src='http://www.自动化测试.com']").locator("//div[@id='c8']").click()
    print('完成')
