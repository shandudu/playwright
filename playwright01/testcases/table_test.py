from playwright01.data_module.project_Data import project_data_createProject
from playwright01.testcases import *


def test_new_context(new_context):
    my_page_tester = PageIns.new_context_return_page(new_context, "测试员")  # 确认这里的函数名与定义处一致
    my_page_tester.project_page.navigate()
    my_page_tester.project_page.click_button(button_name="新建")
    print('**************')
    # 数据类的使用
    test_dict = project_data_createProject(项目集名称="table_test", 项目集周期="1, 1", 父项目集="公共项目集")
    my_page_tester.project_page.form_card_add(**test_dict.as_dict())
    # my_page_tester.project_page.form_card_add_only(**test_dict.as_dict())
    # my_page_tester.project_page.create_project(**test_dict.as_dict())

    # my_page_tester.project_page.form_card_add(项目集名称="table_test", 项目集周期="1, 1", 父项目集="公共项目集")

    # my_page_tester.project_page.el_datetime(label="项目集周期", days="1, 1")
    # my_page_tester.project_page.el_input(label="项目集名称", value="xxx")


    # index = my_page_tester.project_page.get_table.get_header_index(column_name="开始时间")
    # loc = my_page_tester.project_page.get_table.get_row_locator(my_page_tester.page.get_by_text('table_test'))
    # my_page_tester.project_page.get_table.get_cell("开始时间", my_page_tester.page.get_by_text('table_test'))
    # print(my_page_tester.project_page.get_table.get_cell("开始时间",
    #                                                      my_page_tester.page.get_by_text('table_test')).text_content())
    #
    # print(my_page_tester.project_page.get_table.get_cell(2, 6).text_content())
    # my_page_tester.project_page.get_table.get_row_dict()
    # print(my_page_tester.project_page.get_table.get_col_list('开始时间'))
    # my_page_tester.project_page.el_input("项目集名称", '12322222455', my_page_tester.page.locator('//*[@class="ant-form ant-form-horizontal"]')) #最上层元素定位
    # my_page_tester.project_page.el_input("项目集名称", '12322222455') # 无最上层元素定位
    # my_page_tester.project_page.el_select("项目集", 'table_test') # 无最上层元素定位
    # my_page_tester.project_page.el_radio("权限类型", '企业内公开') # 无最上层元素定位
    # my_page_tester.project_page.el_radio("工作流设置规则", '引用项目模板') # 无最上层元素定位
    # # my_page_tester.project_page.el_radio("工作流设置规则", '基于已有项目') # 无最上层元素定位
    # my_page_tester.project_page.el_switch("创建文档空间", '开') # 无最上层元素定位
