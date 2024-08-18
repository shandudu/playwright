import time
from playwright01.module import *

class ProjectPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = '/portfolio'
        self.input_name = self.page.get_by_placeholder("1-32个字符")
        self.search_name = self.page.get_by_placeholder("请输入项目集名称")
        self.system_button = self.page.locator('//span[@aria-label="setting"]').locator("xpath=/..")
        self.ops = self.page.get_by_text("运维操作")
        self.no_data = self.page.get_by_text("暂无数据")

    def create_project(self, project_name="自动化创建项目集", is_time=True):
        self.navigate()
        self.click_button("新建")
        if is_time:
            project_name = f"{project_name}_{time.time_ns()}"
        self.input_name.fill(project_name)
        self.click_button("确定")
        self.search_name.fill(project_name)
        expect(self.page.locator("a").filter(has_text=project_name)).to_be_visible()
        return project_name


    def del_project(self, project_name):
        while True:
            self.navigate()
            # self.input_name.fill(project_name)
            self.search('请输入项目集名称', project_name)
            if self.no_data.count():
                break
            else:
                self.system_button.last.click()
                self.ops.click()
                self.click_button("删除项目集")
                self.click_button("确定")
