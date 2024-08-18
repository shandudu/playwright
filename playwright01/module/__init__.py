import pytest
from playwright.sync_api import Page, expect, BrowserContext
from filelock import FileLock
from playwright01.utils.GetPath import get_path
from playwright01.module.OrderPage import OrderPage
from playwright01.module.BaiduPage import Baidu
from playwright01.module.LoginPage import LoginPage
from playwright01.utils.globalMap import GlobalMap
