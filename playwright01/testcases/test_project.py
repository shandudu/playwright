
# import os
# os.environ['PYTHONPATH'] = 'D:\\ythonProject\\playwright\\playwright01'
# a = os.environ['PYTHONPATH']
# # 添加项目根目录到系统路径
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
#
# print(a)
import sys
import os

import pytest

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
@pytest.mark.parallel
def test_createProject(new_context, del_project):
    try:
        with 测试步骤("初始化和登录测试员"):
            my_page_project = PageIns.new_context_return_page(new_context, "测试员")
        with 测试步骤("创建项目集"):
            item = {
                '项目名': '自动化创建项目集'
            }
            aaa = my_page_project.project_page.create_project2(**item)

    except Exception as e:

        raise

@pytest.fixture
def del_project(new_context):
    try:
        print('前置')
        yield
        with 测试步骤("初始化和登录测试员"):
            my_page_project = PageIns.new_context_return_page(new_context, "测试员")
        with 测试步骤("删除项目集"):
            my_page_project.project_page.del_project("自动化创建项目集")
    except Exception as e:
        pass

# if __name__ == '__main__':
#     # import pytest
#     pytest.main(['-s', 'test_baidu.py'])