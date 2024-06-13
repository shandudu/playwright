from playwright.sync_api import Page, expect


def test_pw_action(page: Page) -> None:
    page.goto("/demo/button")
    page.wait_for_timeout(10000)
    page.get_by_text("点击我试试1").click(modifiers=["Control"])
    page.get_by_text("点击我试试1").click(button="right")
    page.get_by_text("点击我试试1").click(position={"x": 15, "y": 20})
    page.get_by_text("点击我试试1").click(click_count=3, delay=1_000)
    page.get_by_text("点击我试试1").click(timeout=3_000)
    page.get_by_text("点击我试试1").click(force=True)
    page.get_by_text("点击我试试1").click(no_wait_after=True)
    page.get_by_text("点击我试试1").click(trial=True)
    page.get_by_text("点击我试试1").dblclick()


def test_pw_notification_message(page: Page) -> None:
    page.goto("/demo/button")
    # page.wait_for_timeout(2_000)
    page.get_by_text("点击我试试1").click()
    expect(page.get_by_text("点击成功1!")).to_be_visible()


def test_pw_hover(page: Page) -> None:
    page.goto("/demo/hover", wait_until="networkidle")
    page.locator("#c4").hover()
    expect(page.get_by_text("你已经成功悬浮")).to_be_visible()


def test_pw_dropdown(page: Page) -> None:
    page.goto("/demo/dropdown", wait_until="networkidle")
    page.get_by_text("点击选择").click()
    page.get_by_text("playwright").click()
    expect(page.get_by_text("你选择了websocket")).to_be_visible()
    page.get_by_text("点击选择").click()
    page.get_by_text("selenium").click()
    expect(page.get_by_text("你选择了webdriver")).to_be_visible()


def test_pw_input(page: Page) -> None:
    page.goto("/demo/input", wait_until="networkidle")
    page.get_by_placeholder("不用管我,我是placeholder").fill("12345\n")
    assert page.get_by_placeholder("不用管我,我是placeholder").input_value() == "12345"
    page.get_by_label("也许你可以通过label来定位input输入框").fill("label输入")
    assert page.get_by_label("也许你可以通过label来定位input输入框").input_value() == "label输入"
    page.get_by_label("数字输入专用").fill("1.5682345678952130123")
    page.get_by_label("数字输入专用").blur()
    page.wait_for_timeout(1_000)
    assert page.get_by_label("数字输入专用").input_value() == "1.5682345679"


def test_pw_textarea(page: Page) -> None:
    page.goto("/demo/textarea", wait_until="networkidle")
    page.locator("textarea").fill("12345")
    page.locator("textarea").fill("12345\n6")
    page.locator("textarea").fill("""123456""")
    expect(page.locator("textarea")).to_have_value("123\n     456")