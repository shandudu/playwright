from playwright.sync_api import Page, expect, BrowserContext, Browser
from pytest import mark
import pytest
from filelock import FileLock
from playwright01.utils.GetPath import get_path
from playwright01.utils.globalMap import GlobalMap
from playwright01.module import PageIns
from playwright01.data_module.project_Data import *

from allure import severity as 用例级别, step as 测试步骤, title as 用例名称, description as 用例描述

from allure_commons.types import Severity
阻塞 = Severity.BLOCKER
严重 = Severity.CRITICAL
普通 = Severity.NORMAL
不重要 = Severity.TRIVIAL
轻微 = Severity.MINOR


