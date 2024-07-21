# 1.日历时间控件限制手动输入的情况下，**fill()**无法写入数据，需要执行js来移除readonly属性！
# 详细参考博客：日历时间控件（传送门）
# 1.有些页面的内容不是打开页面时直接加载的，需要我们滚动页面，直到页面的位置显示在屏幕上时，才会去请求服务器，加载相关的内容。所以，有时候我们就需要模拟页面向下滚动的操作。而python没有提供操作滚动条的方法，只能借助js来完成！
# 2.使用JS语句模拟向下滚动页面
# 可以使用JS语句，定位滚动条的位置到最下面，从而实现页面的向下滚动。
# js = "var q=document.documentElement.scrollTop=滚动条的位置"
# page.evaluate(js)
# 1.获取浏览器滚动条滚动距离的问题，共有两种方法，
# document.body.scrolltop//当没有DOCTYPE声明时，用它
# document.documentElement.scrollTop//标准网页，用它
# 2.也有人说chrome只能使用document.body.scrollTop方法得到height值，本人试用了一下，得到的结果是
# 以此可见，Chrome依然遵循上面的标准，使用document.documentElement.scrollTop方式，得到height值
# 其实在实际使用中，为确保在各个浏览器中的正常使用，js代码可采用如下方法：
# var height = document.body.scrolltop||document.documentelement.scrolltop


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.cnblogs.com/")
    js = "var q=document.documentElement.scrollTop=50000"
    page.evaluate(js)
    page.wait_for_timeout(3000)
    # page.pause()
    browser.close()

# 高亮操作元素
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com/")
    #定位点击登录
    #page.pause()
    page.locator("#s-top-loginbtn").click()
    page.locator("#TANGRAM__PSP_11__userName").fill("北京-宏哥")
    #设置颜色
    usernamejs ="var u = document.getElementById('TANGRAM__PSP_11__userName').style.background = 'yellow'; var u1=document.getElementById('TANGRAM__PSP_11__userName').style.border = '2px solid red'"
    page.evaluate(usernamejs)
    passwordjs = "var u = document.getElementById('TANGRAM__PSP_11__password').style.background = 'yellow'"
    page.evaluate(passwordjs)
    submitjs = "var u = document.getElementById('TANGRAM__PSP_11__submit').style.background = 'yellow'"
    page.evaluate(submitjs)
    page.wait_for_timeout(3000)
    # page.pause()
    browser.close()