"""
同步
browser = chromium.launch()
context = browser.new_context()

# Start tracing before creating / navigating a page.
context.tracing.start(screenshots=True, snapshots=True, sources=True)

page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
context.tracing.stop(path = "trace.zip")
异步
browser = await chromium.launch()
context = await browser.new_context()

# Start tracing before creating / navigating a page.
await context.tracing.start(screenshots=True, snapshots=True, sources=True)

await page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
await context.tracing.stop(path = "trace.zip")
运行代码后，我们可以看到，在文件夹中会多出一个名为trace.zip，我们可以使用playwright cli或者在浏览器中打开保存的跟踪trace.playwright.dev。命令如下：
1.playwright show-trace trace.zip  2.访问https://trace.playwright.dev/，选择我们录制好的trace.zip文件，将其拖拽到页面中，即可打开
"""

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("北京-宏哥")
    page.locator("#su").click()
    context.tracing.stop(path="trace.zip")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)


"""  
上边宏哥讲解的是创建一个追踪文件。那么如果想使用同一个浏览器上下文创建多个跟踪文件，我们可以先用tracing.start()。然后再使用tracing.start_chunk创建多个跟踪文件。语法示例如下：

context.tracing.start(name="trace", screenshots=True, snapshots=True)
page = context.new_page()
page.goto("https://playwright.dev")

context.tracing.start_chunk()
page.get_by_text("Get Started").click()
# Everything between start_chunk and stop_chunk will be recorded in the trace.
context.tracing.stop_chunk(path = "trace1.zip")

context.tracing.start_chunk()
page.goto("http://example.com")
# Save a second trace file with different actions.
context.tracing.stop_chunk(path = "trace2.zip")
"""