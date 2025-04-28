import os

class FileUploadUtils:
    @staticmethod
    def upload_file(page, locator, file_path):
        """
        上传文件到指定的页面元素。

        :param page: Playwright 页面对象
        :param locator: 文件输入框的定位器
        :param file_path: 文件路径
        """
        # 动态构建文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, '..', file_path)

        # 确保文件存在
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"文件未找到: {full_path}")

        # 上传文件
        page.locator(locator).set_input_files(full_path)
