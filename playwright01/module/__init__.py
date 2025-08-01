import pytest
import time
import os
import sys
import re
from playwright.sync_api import Page, expect, BrowserContext, Locator
from filelock import FileLock
from playwright01.utils.GetPath import get_path
from playwright01.utils.globalMap import GlobalMap
from playwright01.data_module.auth_Data import MyData
from playwright01.module.BasePage import PageObject
from playwright01.module.BaiduPage import Baidu
from playwright01.module.LoginPage import LoginPage
from playwright01.module.OrderPage import OrderPage
from playwright01.module.ProjectPage import ProjectPage
from playwright01.module.FramePage import FramePage




class PageIns:
    def __init__(self, page: Page):
        self.page = page
        self.baidu_page = Baidu(self.page)
        self.login_page = LoginPage(self.page)
        self.order_page = OrderPage(self.page)
        self.project_page = ProjectPage(self.page)
        self.frame_page = FramePage(self.page)

    @staticmethod
    def new_context_return_page(new_context, user):
        # user : 用户别名
        # env : 被测环境
        # from playwright01.module.PageInstance import PageIns
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
                    my_page.login_page.login(username, password)
                    # 注释掉，因为storage_state有的系统使用会有问题
                    # my_page.page.context.storage_state(path=get_path(f".temp/{env}--{user}.json"))
            else:
                context: BrowserContext = new_context()
                page = context.new_page()
                my_page = PageIns(page)
                my_page.login_page.login(username, password)
                # 注释掉，因为storage_state有的系统使用会有问题
                # my_page.page.context.storage_state(path=get_path(f".temp/{env}--{user}.json"))
        return my_page