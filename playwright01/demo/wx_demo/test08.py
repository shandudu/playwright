from playwright.sync_api import sync_playwright
"""# Opens a new tab"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page1 = context.new_page()
    page2 = context.new_page()

    page1.goto("https://www.baidu.com")
    page1.fill('#kw', 'xxxx')
    page1.wait_for_timeout(2_000)

    page2.goto("https://www.baidu.com")
    page2.fill('#kw', 'xxxxtencation')
    page2.wait_for_timeout(1_000)
    browser.close()


# Get page after a specific action (e.g. clicking a link)

# with context.expect_page() as new_page_info:
#     page.get_by_text("open new tab").click() # Opens a new tab
# new_page = new_page_info.value
#
# new_page.wait_for_load_state()
# print(new_page.title())

# Get popup after a specific action (e.g., click)
# with page.expect_popup() as popup_info:
#     page.get_by_text("open the popup").click()
# popup = popup_info.value
#
# popup.wait_for_load_state()
# print(popup.title())

# 如果触发新页面的操作未知，可以使用以下模式

# Get all new pages (including popups) in the context
def handle_page(page):
    page.wait_for_load_state()
    print(page.title())

context.on("page", handle_page)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.baidu.com")
    with context.expect_page() as new_page_info:
        page.click('text=新闻')
    new_page = new_page_info.value
    new_page.wait_for_load_state()  # 等待页面加载到指定状态
    print(new_page.title())
    browser.close()


