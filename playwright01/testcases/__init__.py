from playwright.sync_api import Page, expect, BrowserContext, Browser
from pytest import mark
import pytest
from filelock import FileLock
from playwright01.utils.GetPath import get_path
from playwright01.utils.globalMap import GlobalMap
from playwright01.module import PageIns