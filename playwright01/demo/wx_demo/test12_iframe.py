# 《最新出炉》系列初窥篇-Python+Playwright自动化测试-11-playwright操作iframe-下篇


from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto("https://mail.qq.com/")
    dump_frame_tree(page.main_frame, "")
    browser.close()

def dump_frame_tree(frame, indent):
    print(indent + frame.name + '@' + frame.url)
    for child in frame.child_frames:
        dump_frame_tree(child, indent + "    ")

with sync_playwright() as playwright:
    run(playwright)

# page.main_frame #获取page对象本身的 frame 对象
# page.frames #获取page对象全部frames 包含page本身的frame对象
# frame.child_frames #获取frame下的全部子 frame 对象
# page.frame_locator('') #返回的对象只能用locator() 方法定位元素然后click()等操作元素
# page.frame(name，url) #方法可以使用frame的name属性或url属性定位到frame对象

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://mail.163.com/")
    print('获取page对象本身的frame对象')
    print(page.main_frame)
    print('获取page对象全部frames 包含page本身的frame对象 ')
    print(page.frames)
    print('获取page对象子frame ')
    print(page.main_frame.child_frames)
    browser.close()
