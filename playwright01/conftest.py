import pytest
from playwright.sync_api import BrowserContext, Page


@pytest.fixture()
def hello_world():
    print("hello")
    yield
    print("world")

@pytest.fixture
def page(context: BrowserContext) -> Page:
    print("this my page")
    return context.new_page()