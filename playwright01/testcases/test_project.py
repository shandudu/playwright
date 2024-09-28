from playwright01.testcases import *




@用例名称("项目集的新建")
@用例描述("""
1. 项目集的新建
2. 删除项目集
""")
@用例级别(严重)
def test_createProject(new_context, del_project):
    with 测试步骤("初始化和登录测试员"):
        my_page_project = PageIns.new_context_return_page(new_context, "测试员")
    with 测试步骤("创建项目集"):
        aaa = my_page_project.project_page.create_project()
    print(aaa)

@pytest.fixture
def del_project(new_context):
    print('前置')
    yield
    with 测试步骤("初始化和登录测试员"):
        my_page_project = PageIns.new_context_return_page(new_context, "测试员")
    with 测试步骤("创建项目集"):
        my_page_project.project_page.del_project("自动化创建项目集")
