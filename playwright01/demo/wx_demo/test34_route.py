from playwright.sync_api import sync_playwright

def intercept_request(route, request):
    if request.url.startswith("https://www.baidu.com/"):
        print(f"Intercepted request to: {request.url}")
        route.abort()  # 中止请求

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 监听请求并拦截
    page.route("https://www.baidu.com/img/*", lambda route, request: intercept_request(route, request))
    page.wait_for_timeout(3000)
    page.goto("https://www.baidu.com/")
    #page.pause()
    page.wait_for_timeout(3000)
    # page.pause()
    print('Test Complete')  # Add break point here
    browser.close()

# Route类的fulfill()方法用于模拟完成请求，即手动提供响应数据并结束请求
def intercept_request(route, request):
    if request.url.startswith("https://dog.ceo/api/breeds/list/all"):
        print(f"Intercepted request to: {request.url}")
        route.fulfill(status=200, body='{"message": "Hello, World!"}', headers={'Content-Type': 'application/json'})
    else:
        route.continue_()


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 监听请求并拦截
    page.route("**/*", lambda route, request: intercept_request(route, request))

    page.goto("https://dog.ceo/api/breeds/list/all")
    page.wait_for_timeout(3000)
    page.pause()
    print('Test Complete')  # Add break point here
    browser.close()


def handle(route):
    response = route.fetch()
    json = response.json()
    json["message"]["beijing-hongge"] = ["beijing-hongge"]
    route.fulfill(response=response, json=json)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.route("https://dog.ceo/api/breeds/list/all", handle)
    page.goto("https://dog.ceo/api/breeds/list/all")
    page.wait_for_timeout(3000)
    page.pause()
    print('Test Complete')  # Add break point here
    browser.close()