from playwright01.testcases import *


def test_createProject(new_context, del_project):
    my_page_project = PageIns.new_context_return_page(new_context, "测试员")
    aaa = my_page_project.project_page.create_project()
    print(aaa)

@pytest.fixture
def del_project(new_context):
    print('前置')
    yield
    my_page_project = PageIns.new_context_return_page(new_context, "测试员")
    my_page_project.project_page.del_project("自动化创建项目集")
