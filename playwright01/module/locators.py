from playwright01.module import *


class Locators:
    def __init__(self, page: Page):
        self.page = page


    def button_locator(self, value, index) -> Locator:
        button = self.page.locator("button")
        for word in value:
            button = button.filter(has_text=word)

        return  button.locator('visible=true').nth(index)

    def below_locator(self, find_locator="*") -> Locator:
        return self.page.locator(f"xpath=/following::{find_locator}[position()=1]")

    def get_header_div(self, value:str) -> Locator:
        div_locator = self.page.locator('label').locator('visible=true').filter(has=self.page.get_by_text(value)).locator(self.below_locator())
        return div_locator