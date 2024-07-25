from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    # 创建一个浏览器实例
    browser = playwright.chromium.launch()
    # 启动录制
    context = browser.new_context(record_video_dir="videos/recording.mp4",record_video_size={"width": 1980, "height": 960})
    page = context.new_page()
    # 执行需要录制的操作
    page.goto("https://www.baidu.com")
    page.locator("#kw").fill("北京-宏哥")
    page.locator("#su").click()
    # 关闭实例
    context.close()
    browser.close()
    # 保存录像文件
    # 获取视频路径
    recording_path = page.video.path()
    print("录像文件路径：", recording_path)
    # 删除视频
    # video.delete()
    # 视频另存为
    # video.save_as(path)