str = 'shanyingxuanxdfghjk'

print(str[0:3:2])
print(str[:8])
print(str[8:])
print(str[-1:])
print(str[:-1])
print(str[::-1])

import re

# 原始字符串
original_string = "abc123你好456def789"

# 替换非数字的字符
result = re.sub(r"[^\d]+", "", original_string)

print(result)  # 输出：123456789

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.sogou.com")
    page.locator("#query").fill("playwright")
    page.locator("#stb").click()
    page.wait_for_timeout(1000)
    # 定位 搜狗为您找到相关结果约xxxx个 这个元素
    result = page.locator("//*[@id='main']/div[1]/p")
    # 获取该字段值  "搜索工具 搜狗为您找到相关结果约xxxxx个"
    result_string = result.inner_text()
    print(result_string)
    # # 根据约这个词切片，取第二片字符串，应该得到“xxxx个”
    # st1 = result_string.split("约")[1]
    # print(st1)
    # # 再切一次，去除条，得到我们想要的数字结果数
    # search_number = st1.split("条")[0]
    # # 去掉字符串中的逗号，方便转换成int
    # search_number1 = search_number.replace(",", "")
    search_number1 = result = re.sub(r"[^\d]+", "", result_string)
    print(search_number1)

    page.goto("https://cn.bing.com")
    new_page = None
    page.locator("#sb_form_q").fill("playwright")
    page.locator("#search_icon").click()
    page.wait_for_timeout(1000)

    # context.on("page", handle_new_page)

# 点击按钮，这个操作会打开一个新页面
#     page.click('button#open-new-page')

    # 等待新页面加载完成
    # if new_page:
    #     new_page.wait_for_load_state()
    #     print(new_page.title())
    #
    # # 在新页面上执行操作
    # new_page.goto('')



    # 定位 必应为xxxx条结果 这个元素
    result1 = page.locator("//*[@id='b_tween_searchResults']/span")
    # 获取该字段值  "约 xxx 个结果"
    result_string1 = result1.inner_text()
    print(result_string1)
    # st2 = result_string1.split("约")[1]
    # print(st2)
    # # 再切一次，去除个，得到我们想要的数字结果，根据个这个词切片，取第一片字符串，应该得到“273,000 ”
    # st2 = st2.split("个")[0]
    # # 去掉字符串中的逗号和空格，方便转换成int
    # st3 = st2.strip().replace(",", "")
    # print(st3)
    st3 = re.sub(r"[^\d]+", "", result_string1)
    # 首先将两个数都转换为int 数据
    a_N = int(search_number1)
    b_N = int(st3)
    # 搜狗和必应的搜索结果对比
    if (a_N > b_N):
        print("搜狗牛逼，搜狗威武！！！")
    else:
        print("必应牛逼，必应威武！！！");
    page.wait_for_timeout(20000)
    page.close()
    context.close()
    browser.close()


    # def handle_new_page(page):
    #     nonlocal new_page
    #     new_page = page


with sync_playwright() as playwright:
    run(playwright)
