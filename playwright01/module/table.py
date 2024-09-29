import random

from playwright01.module import *


class Table:
    # column : 列
    # row:  行

    def __init__(self, page: Page, value: str = None, index: int = -1):
        self.page = page
        self.page.wait_for_load_state("networkidle")
        # self.table_div = self.page.locator('.ant-table-wrapper ezone-resizeTable stdScrollBar ezone-resizeTable-hidden _workbenchList_18rqg_1 ant-table-middle _table_mxss1_1')
        self.table_div = self.page.locator('.ant-table-wrapper').filter(has_text=value).nth(index)
        self.table_header_tr = self.table_div.locator('//thead/tr')

    def get_header_index(self, column_name: str) -> int:
        return self.table_header_tr.locator("th").all_text_contents().index(column_name)

    def get_row_locator(self, row_locator: Locator) -> Locator:
        return self.table_div.locator("tr").filter(has=row_locator)

    def get_cell(self, columnr_nameorcolumn_index: str | int,
                 row_locatororrow_indexorrow_value: Locator | int | str) -> Locator:
        """
        :param columnr_nameorcolumn_index: 列名或者列索引
        :param row_locatororrow_indexorrow_value: 行定位器或者行索引或者行值
        :return:
        """
        if isinstance(columnr_nameorcolumn_index, str):
            # 判断是否为字符串类型, 为字符串类型，则是columnr_name
            column_index = self.get_header_index(columnr_nameorcolumn_index)
        else:
            # 不是 则是column_index
            column_index = columnr_nameorcolumn_index

        if isinstance(row_locatororrow_indexorrow_value, Locator):
            row_index = self.get_row_locator(row_locatororrow_indexorrow_value)
        elif isinstance(row_locatororrow_indexorrow_value, str):
            row_index = self.table_div.locator("tr").filter(has_text=row_locatororrow_indexorrow_value)
        else:
            row_index = self.table_div.locator("tbody").locator('//tr[not(@aria-hidden="true")]').nth(
                row_locatororrow_indexorrow_value)

        return row_index.locator("td").nth(column_index)

    def get_row_dict(self, row_locatororrow_index: Locator | int = "random") -> dict:
        if isinstance(row_locatororrow_index, int):
            tr = self.table_div.locator("tbody").locator('tr').locator('visible=true').nth(row_locatororrow_index)
        elif isinstance(row_locatororrow_index, Locator):
            tr = self.table_div.locator("tr").filter(has=row_locatororrow_index)
        else:
            all_tr = self.table_div.locator('tbody').locator('tr').locator('visible=true').all()
            tr = random.choice(all_tr)

        td_text_list = tr.locator('td').all_text_contents()
        header_text_list = self.table_header_tr.locator('th').all_text_contents()
        row_dict = dict(zip(header_text_list, td_text_list))
        return row_dict

    def get_col_list(self, column_name: str) -> list:
        index = self.get_header_index(column_name)
        all_tr = self.table_div.locator('tbody').locator('tr').locator('visible=true').all()
        col_list = []
        for tr in all_tr:
            col_list.append(tr.locator('td').nth(index).text_content())
        return col_list

        def check_table_box(self, *args, unchecked:bool = False):
            """
            勾选checkbox的方法
            :param args:如果是int,则主要为至上而下选中的checkbox个数（只能传一个）,
            如果是str，则为str能标识的某行的checkbox（可传多个）
            如果是Locator，则为locator为某行的checkbox(可传多个)
            :param unchecked:是否清楚之前勾选，是否先设置为全部不勾选的状态
            :return:
            """
        if unchecked:
            for check_box in self.table_div.locaotr('//input[@type="checkbox"]').all(): check_box.set_checked(False)
        for arg in args:
            if isinstance(arg, int):
                for i in range(arg):
                    for check_box in self.table_div.locator('//tbody/input[@type="checkbox"]').all()[:arg]: check_box.set_checked(True)
                    break
            if isinstance(arg, str):
                self.table_div.locator('//tr').filter(has_text=arg).locator('//input[@type="checkbox"]').set_checked(True)
            if isinstance(arg, Locator):
                self.table_div.locator('//tr').filter(has=arg).locator('//input[@type="checkbox"]').set_checked(True)