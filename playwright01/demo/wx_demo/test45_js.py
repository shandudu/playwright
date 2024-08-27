from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.wait_for_timeout(1000)
    searchInputBox = page.locator("#kw")
    if searchInputBox.is_enabled():
        print("百度首页的搜索输入框可以输入内容！")
    # 给搜索输入框通过JavaScript添加disable属性
    js = "document.getElementById('kw').setAttribute('disabled', '')";
    page.evaluate(js)
    searchInputBox1 = page.locator("//*[@id='kw']")
    # 再次判断搜索输入框是否可以操作（输入搜索内容）
    if ~searchInputBox1.is_enabled():
        print("百度首页的搜索输入框不可以输入内容！")

    # searchInputBox1.fill('1111')

    page.wait_for_timeout(1000)
    print("browser will be close")
    page.close()
    context.close()
    browser.close()

# 自定义方法来判断页面元素是否存在
def is_element_present(page, selector):
    """
    判断指定选择器的元素是否存在于页面上
    :param page: Playwright的Page对象
    :param selector: 用于选择元素的CSS选择器
    :return: 如果元素存在返回True，否则返回False
    """
    try:
        # 尝试获取元素
        page.wait_for_selector(selector, timeout=5000)  # 等待元素出现，超时时间为5秒
        return True
    except Exception as e:
        # 如果在等待元素或获取元素时发生异常，说明元素不存在
        return False

def run2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com/")
    page.wait_for_timeout(1000)
    if is_element_present(page,"input#kw"):
        searchInputBox = page.locator("#kw")
        '''判断searchInputBox变量对象是否处于可用状态。如果处于可用状态，则输入“百度首页的搜索输入框被成功找到！” '''
        if searchInputBox.is_enabled():
            searchInputBox.type("百度首页的搜索输入框被成功找到！")
    else:
        print("页面上的输入框元素未被找到！")
    page.wait_for_timeout(1000)
    print("browser will be close")
    page.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)