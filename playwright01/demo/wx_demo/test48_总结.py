from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    """模拟输入
   1.type模拟人工输入:一个字符一个字符地输入字段， 模拟真实的键盘输入。
   page.get_by_placeholder('手机号或邮箱').type('1760123456',delay=1000)  #delay是设置输入延迟时间，不然眼睛会看不到效果
   2.fill输入文字
   fill()#输入文字
   
   2.2查找元素
   page.locator()#元素定位器
   page.get_by_text("文本内容")#查找文本匹配的元素
   page.get_by_role("button")#get_by_role是一个查找页面元素的方法,代表要查找的元素的角色或类型

   2.3模拟点击相关
   #点击
   page.get_by_role("button").click()
   #双击
   page.get_by_text("Item").dblclick()
   #右击
   page.get_by_text("Item").click(button="right")
   #Shift+点击
   page.get_by_text("Item").click(modifiers=["Shift"])
   #鼠标悬停在元素上
   page.get_by_text("Item").hover()
   #点击左上角
   page.get_by_text("Item").click(position={"x":0,"y":0})
   
   2.4获取元素文本
   inner_text()#获取元素的文本内容
   
   2.5等待时间
   page.wait_for_timeout(2000)#强制等待2秒
   
   2.6模拟键盘按钮
   #按Enter键
   page.get_by_text("Submit").press("Enter")
   #在键盘上按$符号
   page.get_by_role("textbox").press("$")
   2.7获取元素属性
   page.locator('#s-top-left>a').get_attribute()#获取元素属性
   2.8获取input 输入框的值
   可以通过input_value() 方法获取输入框的内容。
   #获取输入框的值
   input1=page.locator('#kw')
   input1.fill('北京-宏哥')
   print(input1.input_value())
   """






with sync_playwright() as playwright:
    run(playwright)