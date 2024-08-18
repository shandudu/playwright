from playwright01.testcases import *

def test_new_context(new_context):
    my_page_tester = new_context_return_page(new_context, "测试员")  # 确认这里的函数名与定义处一致
    my_page_manager = new_context_return_page(new_context, "测试经理")  # 确认这里的函数名与定义处一致
