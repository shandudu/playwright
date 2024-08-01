from playwright.sync_api import sync_playwright, Route


def intercept_request(route, request):
    if request.url.startswith("https://dog.ceo/"):
        print(f"Intercepted request to: {request.url}")
        route.continue_() # 继续请求

def intercept_request(route: Route, request):
    if request.url.startswith("http://www.baidu.com/api"):
        print(f"拦截请求: {request.url}")
        route.continue_()  # 中止请求
    else:
        print(f"Fallback: {request.url}")
        route.fallback()

def intercept_request(route, request):
    if request.url.startswith("https://dog.ceo/api/breeds/list/all"):
        print(f"Intercepted request to: {request.url}")
        route.fulfill(status=200, body='{"message": "Hello, World!"}', headers={'Content-Type': 'application/json'})
        print(route.request)
    else:
        route.continue_()

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 监听请求并拦截
    page.route("**/*", lambda route, request: intercept_request(route, request))

    page.goto("https://dog.ceo/api/breeds/list/all")
    page.wait_for_timeout(3000)
    # page.pause()
    page.wait_for_timeout(3000)
    print('Test Complete')  # Add break point here
    browser.close()

def run2(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 监听请求并拦截
    page.route("**/**", lambda route, request: intercept_request(route, request))
    page.goto("http://www.baidu.com")
    print('Test Complete')  # Add break point here
    browser.close()

def run3(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 监听请求并拦截
    page.route("**/*", lambda route, request: intercept_request(route, request))

    page.goto("https://dog.ceo/api/breeds/list/all")
    page.pause()

    browser.close()
with sync_playwright() as playwright:
    run3(playwright)

