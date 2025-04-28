import os
import shutil

import pytest
from multiprocessing import Process

def run_parallel():
    """ 并行域：2个worker执行标记用例 """
    pytest.main([
        "-m", "parallel", 
        "-n", "2", 
        "-v", 
        "--junitxml=parallel.xml",
        "--alluredir=./.allure_parallel"  # 为并行测试创建独立目录
    ])

def run_serial():
    """ 串行域：主进程执行未标记用例 """
    pytest.main([
        "-m", "not parallel", 
        "-v", 
        "--junitxml=serial.xml",
        "--alluredir=./.allure_serial"  # 为串行测试创建独立目录
    ])

if __name__ == '__main__':
    # 清空历史报告目录（新增allure-results清理）
    for dir in ['.allure_parallel', '.allure_serial', 'allure-results']:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    # 启动并行域进程
    p = Process(target=run_parallel)
    p.start()

    # 主进程执行串行用例
    run_serial()

    # 等待并行完成
    p.join()

    # 合并到Jenkins默认读取的allure-results目录
    os.system("allure generate --clean .allure_parallel .allure_serial -o allure-results")
    os.system("allure open allure-results")  # 本地调试用
    # time.sleep(3)
    # os.system("allure generate ./.allure_report -o ./.allure-results --clean")
