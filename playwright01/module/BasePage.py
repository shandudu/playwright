from playwright01.module import *
from playwright01.module.table import Table
from playwright01.module.locators import Locators
from playwright01.utils.my_date import *

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

    def hover_retry(self, hover对象: Locator, 下一步点击对象: Locator, 第一步动作="hover", 第二步动作="click", timeout=30_000):
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout / 1000:
                pytest.fail(f"hover重试{hover对象.__str__()}在{timeout/1000}秒内未成功")
            try:
                self.page.mouse.move(x=1, y=1)
                self.page.wait_for_timeout(1_000)
                if 第一步动作 == "hover":
                    hover对象.last.hover()
                else:
                    hover对象.last.click()
                self.page.wait_for_timeout(3_000)
                if 第二步动作 == "click":
                    下一步点击对象.last.click(timeout=3000)
                else:
                    下一步点击对象.last.wait_for(state="visible", timeout=3000)
                break
            except:
                continue



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

    def el_datetime(self, label: str, days: str, header_div: Locator = None, timeout: float = None):
        """
        :param label:
        :param days:
        :param header_div:
        :param timeout:
        date_locator :日期控件定位
        :return:
        """
        if header_div:
            date_locator = header_div.locator(self.locators.get_header_div(label))
        else:
            date_locator = self.locators.get_header_div(label)
        days_list = days.split(",")
        for index, day in enumerate(days_list):
            try:
                int(day)
                # date_formatted 格式化后的日期
                date_formatted  = return_time_add_days(int(day))
            except:
                date_formatted = day
            date_locator.locator("input").nth(index).click(timeout=timeout)
            date_locator.locator("input").nth(index).fill(date_formatted, timeout=timeout)
            # 失焦方法
            date_locator.locator("input").nth(index).blur(timeout=timeout)


    def form_card_add(self,header_div: Locator = None, timeout=None, **kwargs):
        for label, value in kwargs.items():
            if not value:
                continue
            elif self.locators.get_header_div(label).locator(".ant-input").count():
                self.el_input(label_name=label, value=value,header_div=header_div, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-select-selector").count():
                self.el_select(label_name=label, value=value,header_div=header_div, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-radio-group").count():
                self.el_radio(label_name=label, value=value,header_div=header_div, timeout=timeout)
            elif self.locators.get_header_div(label).get_by_role("switch").count():
                self.el_switch(label_name=label, switch_status=value,header_div=header_div, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-picker").count():
                self.el_datetime(label=label, days=value,header_div=header_div, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{label}:{value}")


    def form_card_add_only(self, header_div: Locator = None, timeout=None, **kwargs):
        # 页面上已有的表单项列表 = []
        # 已经有唯一表单项 = False
        exist_list = []
        already_unique_form_item = False
        if header_div:
            header_div_locator = header_div
        else:
            for index, label in enumerate(kwargs.keys()):
                if index == 0:
                    try:
                        self.locators.get_header_div(label).last.wait_for(timeout=timeout)
                    except:
                        pass

                if self.locators.get_header_div(label).count() == 0:
                    continue
                else:
                    if self.locators.get_header_div(label).count() == 1:
                        already_unique_form_item = True
                    exist_list.append(self.locators.get_header_div(label))
                if already_unique_form_item and len(exist_list) >= 2:
                    break

            # 包含可见表单项的loc = self.page.locator("*")
            exist_loc = self.page.locator("*")
            for exist_list_loc in exist_list:
                exist_loc = exist_loc.filter(has=exist_list_loc)
            if already_unique_form_item:
                header_div_locator = exist_loc.last
            else:
                header_div_locator = min(exist_loc.all(), key=lambda loc: len(loc.text_content()))

        for label, value in kwargs.items():
            if not value:
                continue
            if self.locators.get_header_div(label).locator(".ant-input").count():
                self.el_input(label_name=label, value=value, header_div=header_div_locator, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-select-selector").count():
                self.el_input(label_name=label, value=value, header_div=header_div_locator, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-radio-group").count():
                self.el_radio(label_name=label, value=value, header_div=header_div_locator, timeout=timeout)
            elif self.locators.get_header_div(label).get_by_role("switch").count():
                self.el_switch(label_name=label, switch_status=value, header_div=header_div_locator, timeout=timeout)
            elif self.locators.get_header_div(label).locator(".ant-picker").count():
                self.el_datetime(label=label, days=value, header_div=header_div_locator, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{label}:{value}")

    # def check_table_box(self, *args, unchecked:bool = False):
    #     """
    #     勾选checkbox的方法
    #     :param args:如果是int,则主要为至上而下选中的checkbox个数（只能传一个）,
    #     如果是str，则为str能标识的某行的checkbox（可传多个）
    #     如果是Locator，则为locator为某行的checkbox(可传多个)
    #     :param unchecked:是否清楚之前勾选，是否先设置为全部不勾选的状态
    #     :return:
    #     """
    #     if unchecked:
    #         for check_box in self.table_div.locaotr('//input[@type="checkbox"]').all(): check_box.set_checked(False)
    #     for arg in args:
    #         if isinstance(arg, int):
    #             for i in range(arg):
    #                 for check_box in self.table_div.locator('//tbody/input[@type="checkbox"]').all()[:arg]: check_box.set_checked(True)
    #                 break
    #         if isinstance(arg, str):
    #             self.table_div.locator('//tr').filter(has_text=arg).locator('//input[@type="checkbox"]').set_checked(True)
    #         if isinstance(arg, Locator):
    #             self.table_div.locator('//tr').filter(has=arg).locator('//input[@type="checkbox"]').set_checked(True)