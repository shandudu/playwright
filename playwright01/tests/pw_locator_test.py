import pytest
from playwright.sync_api import Page, expect


def test_get_by_role(page: Page, hello_world):
    """

    :param page:
    :return:
    """
    page.goto("/demo/dialog", wait_until="networkidle")
    page.get_by_text(text="点我开启一个dialog").click()
    expect(page.get_by_role(role="dialog")).to_be_visible()
    page.goto("/demo/checkbox", wait_until="networkidle")
    page.get_by_role(role="checkbox", name="开发",checked=False).set_checked(True)
    page.get_by_role(role="checkbox", name="开发",checked=True).set_checked(False)
    page.goto("/demo/table", wait_until="networkidle")
    expect(page.get_by_role(role="table")).to_be_visible()
    expect(page.get_by_role(role="cell")).to_have_count(count=13)
    expect(page.get_by_role(role="img", include_hidden=True)).to_have_count(count=4)
    page.goto("/demo/grid", wait_until="networkidle")
    expect(page.get_by_role("treegrid")).to_be_visible()
    expect(page.get_by_role("row").filter(has_text="溜达王").locator("div").nth(1)).to_have_text("44")


@pytest.fixture()
def hello_world():
    print("hello")
    yield
    print("world")