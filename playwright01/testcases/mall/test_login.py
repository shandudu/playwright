from playwright01.testcases import *

@用例名称("登录")
@用例描述("""
1. 登录
2. 删除项目集
""")
@用例级别(严重)
@pytest.mark.parallel
def test_createProject(new_context):
    try:
        with 测试步骤("初始化和登录测试员"):
            my_page_project = PageIns.new_context_return_page_mall(new_context, "测试员")
            pass

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
