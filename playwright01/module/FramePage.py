from playwright01.module import *

class FramePage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.url = "http://www.自动化测试.com/demo/upload"


    def xxx(self):
        self.navigate()
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件路径
        file_path = os.path.join(current_dir, '..', 'data_module', 'xxx.xlsx')
        # 使用路径
        FileUploadUtils.upload_file(self.page, '//input[@type="file"]', 'data_module/xxx.xlsx')
        self.page.locator('//input[@type="file"]').set_input_files(file_path)
        # self.page.locator('//input[@type="file"]').set_input_files('data_module/xxx.xlsx')


    def frame_add(self):
        frmae_baidu = self.page.frame(url='https://www.baidu.com/')
        # https://www.baidu.com/
        if not frmae_baidu:
            raise ValueError("未能找到指定的 frame: https://www.baidu.com")
        frmae_baidu.fill('#kw', '百度一下')
        xxx = PageIns(frmae_baidu.page[0])
        # frmae_baidu.page[0].click_button('百度一下')
        xxx.page.click_button('百度一下')

@classmethod
def click_button(self, button_name, timeout=30_000):
    button_loc = self.page.locator("button")
    for _ in button_name:
        button_loc = button_loc.filter(has_text=_)
    button_loc.click(timeout=timeout)