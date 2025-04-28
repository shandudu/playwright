
# import os
# os.environ['PYTHONPATH'] = 'D:\\ythonProject\\playwright\\playwright01'
# a = os.environ['PYTHONPATH']
# # 添加项目根目录到系统路径
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
from playwright01.module import BasePage
# print(a)
import sys
import os
sys.path.append("D:\\pythonProject\\playwright\\playwright01")
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
# print(sys.path)
from playwright01.testcases import *

@用例名称("项目集的新建")
@用例描述("""
1. 项目集的新建
2. 删除项目集
""")
@用例级别(严重)
def test_createProject(new_context):
    try:
        with 测试步骤("初始化和登录测试员"):
            my_page_project = PageIns.new_context_return_page(new_context, "测试员")

            my_page_project.frame_page.xxx()
            # # 检查 frame 是否存在
            # my_page_project.frame_page.frame_add()
            # # mxxx = PageIns(frmae_baidu.page)
            # # # base_page_instance = BasePage(frmae_baidu)
            # # # base_page_instance.click_button('百度一下')
            # # mxxx.page.click_button('百度一下')


    except Exception as e:

        raise


