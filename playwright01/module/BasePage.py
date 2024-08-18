from playwright01.module import *


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""

    def navigate(self):
        self.page.goto(self.url)

    def click_button(self, button_name, timeout=30_000):
        button_loc = self.page.locator("button")
        for _ in button_name:
            button_loc = button_loc.filter(has_text=_)
        button_loc.click(timeout=timeout)

        # self.page.get_by_role("button").filter(has_text=button_name).click(timeout=timeout)

    def search(self, placeholder: str = None, value: str =None):
        if placeholder:
            # self.page.locator(".ant-input-affix-wrapper input").filter(has=self.page.get_by_placeholder(placeholder)).fill(value)
            self.page.locator(f"//span[@class='ant-input-affix-wrapper']//input[contains(@placeholder, '{placeholder}')]").fill(value)
        else:
            self.page.locator(".ant-input-affix-wrapper input").fill(value)
        self.page.wait_for_load_state("networkidle")

