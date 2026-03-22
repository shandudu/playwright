

from playwright01.testcases import *


def test_filelock1(page: Page):
    my_page = PageIns(page)
    with FileLock(get_path("/.temp/lock.loc")):
        my_page.baidu.baidu_srarch(search_keyword="playwright", search_result="https://github.com/microsoft/playwright")
        # page.wait_for_timeout(10_000)
        global_map = GlobalMap()
        global_map.set("a", "123")
