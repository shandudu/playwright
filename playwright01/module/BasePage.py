from playwright01.module import *
from playwright01.module.table import Table
from playwright01.module.locators import Locators

class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.locators = Locators(self.page)

    def navigate(self):
        self.page.goto(self.url)

    def table(self, value, index: int = -1):
        return Table(self.page, value, index=-1)

    def click_button(self, button_name, timeout=30_000):
        button_loc = self.page.locator("button")
        for _ in button_name:
            button_loc = button_loc.filter(has_text=_)
        button_loc.click(timeout=timeout)

        # self.page.get_by_role("button").filter(has_text=button_name).click(timeout=timeout)

    def search(self, placeholder: str = None, value: str = None):
        if placeholder:
            # self.page.locator(".ant-input-affix-wrapper input").filter(has=self.page.get_by_placeholder(placeholder)).fill(value)
            self.page.locator(
                f"//span[@class='ant-input-affix-wrapper']//input[contains(@placeholder, '{placeholder}')]").fill(value)
        else:
            self.page.locator(".ant-input-affix-wrapper input").fill(value)
        self.page.wait_for_load_state("networkidle")

    def el_input(self, label_name: str, value: str, header_div: Locator = None, timeout: float = None):
        if header_div:
            header_div.locator(self.locators.get_header_div(label_name)).locator("input, textarea").locator("visible=true").last.fill(value, timeout=timeout)

        else:
            self.locators.get_header_div(label_name).locator("input, textarea").locator("visible=true").last.fill(value, timeout=timeout)


    def el_select(self, label_name: str, value: str, header_div: Locator = None, timeout: float = None):
        if header_div:
            header_div.locator(self.locators.get_header_div(label_name)).locator("visible=true").click(timeout=timeout)
            if header_div.locator(self.locators.get_header_div(label_name)).locator('//input[@type="search"]').count():
                header_div.locator(self.locators.get_header_div(label_name)).locator('//input[@type="search"]').fill(value, timeout=timeout)
            self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(value).click(timeout=timeout)
            # 点击label_name 隐藏选项的下拉框
            self.page.locator('//label[@class="ant-form-item-no-colon" and @title="{label_name}"]'.format(label_name=label_name)).click()
        else:
            self.locators.get_header_div(label_name).locator("visible=true").click(timeout=timeout)
            if self.locators.get_header_div(label_name).locator('//input[@type="search"]').count():
                self.locators.get_header_div(label_name).locator('//input[@type="search"]').fill(value, timeout=timeout)
            self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(value).click(timeout=timeout)
            # 点击label_name 隐藏选项的下拉框
            self.page.locator('//label[@class="ant-form-item-no-colon" and @title="{label_name}"]'.format(label_name=label_name)).click()
        expect(self.page.locator(".ant-select-dropdown")).to_be_hidden(timeout=timeout)


    def el_radio(self, label_name: str, value: str, header_div: Locator = None, timeout: float = None):
        if header_div:
            header_div.locator(self.locators.get_header_div(label_name)).locator("label").locator("visible=true").filter(has_text=value).locator("input").check(timeout=timeout)
        else:
            self.locators.get_header_div(label_name).locator("label").locator("visible=true").filter(has_text=value).locator("input").check(timeout=timeout)

    def el_switch(self, label_name: str, switch_status: str, header_div: Locator = None, timeout: float = None):
        if "开" in switch_status or "是" in switch_status:
            switch_status = True
        else:
            switch_status = False
        if header_div:
            header_div.locator(self.locators.get_header_div(label_name)).get_by_role("switch").set_checked(switch_status, timeout=timeout)
        else:
            self.locators.get_header_div(label_name).get_by_role("switch").set_checked(switch_status, timeout=timeout)