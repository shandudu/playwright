import os.path
from playwright01.utils.globalMap import GlobalMap
from playwright01.module import *
from playwright01.data_module.my_Data import MyData


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""

    def navigate(self):
        self.page.goto(self.url)

    def click_button(self, button_name, timeout=30_000):
        button_loc = self.page.locator("button")
        for _ in button_name:
            button_loc = button_loc.filter(has_text=_)
        button_loc.click(timeout=timeout)

        # self.page.get_by_role("button").filter(has_text=button_name).click(timeout=timeout)

def new_context_return_page(new_context, user):
    # user : 用户别名
    # env : 被测环境
    from playwright01.module.PageInstance import PageIns
    global_map = GlobalMap()
    env = global_map.get("env")
    username = MyData().userinfo(env, user)["username"]
    password = MyData().userinfo(env, user)["password"]
    with FileLock(get_path(f".temp/{env}--{user}.lock")):
        if os.path.exists(get_path(f".temp/{env}--{user}.json")):
            context: BrowserContext = new_context(storage_state=get_path(f".temp/{env}--{user}.json"))
            page = context.new_page()
            my_page = PageIns(page)
            my_page.order_page.navigate()
            expect(my_page.login_page.user.or_(my_page.login_page.state)).to_be_visible()
            if my_page.login_page.user.count():
                my_page.login_page.login(username=username, password=password)
                my_page.page.context.storage_state(path=get_path(f".temp/{env}--{user}.json"))
        else:
            context: BrowserContext = new_context()
            page = context.new_page()
            my_page = PageIns(page)
            my_page.login_page.login(username, password)
            my_page.page.context.storage_state(path=get_path(f".temp/{env}--{user}.json"))
    return my_page