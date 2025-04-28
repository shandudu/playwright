import time

from playwright01.testcases import *



def test_retry_while_try(new_context):
    with 测试步骤("初始化和登录测试员"):
        my_page_project = PageIns.new_context_return_page(new_context, "测试员")
        my_page_project.project_page.navigate()
        # my_page_project.project_page.click_button("新建")
    # with 测试步骤("普通hover操作"):
        # my_page_project.page.locator(".ant-dropdown-trigger").hover()
        # my_page_project.page.wait_for_timeout(3_000)
        # my_page_project.page.get_by_text("个人主页").click(timeout=3_000)
    with 测试步骤("普通hover操作"):
        my_page_project.project_page.hover_retry(my_page_project.page.locator(".ant-dropdown-trigger"), my_page_project.page.get_by_title("公共项目集"), "hover", "click")

    # with 测试步骤("使用for和try来重试下拉"):
    #     for _ in range(4):
    #         if _ == 3:
    #             pytest.fail("重试3次，仍然失败")
    #         try:
    #             my_page_project.page.locator("#parent").blur()
    #             my_page_project.page.locator("#parent").click()
    #             my_page_project.page.wait_for_timeout(3_000)
    #             my_page_project.page.get_by_title("公共项目集").click(timeout=3_000)
    #             break
    #         except:
    #             pass
    # with 测试步骤("使用for和try来重试下拉"):
    #     start_time = time.time()
    #     while True:
    #         if time.time() - start_time > 30:
    #             pytest.fail("重试30秒，仍然失败")
    #         try:
    #             my_page_project.page.locator("#parent").blur()
    #             my_page_project.page.locator("#parent").click()
    #             my_page_project.page.wait_for_timeout(3_000)
    #             my_page_project.page.get_by_title("公共项目集").click(timeout=3_000)
    #             break
    #         except:
    #             pass