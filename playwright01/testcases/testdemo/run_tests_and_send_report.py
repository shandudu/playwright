# run_tests_and_send_report.py
import subprocess
import sys
import os
import time
from utils.feishu_robot import send_feishu_report


def run_tests():
    """执行测试用例"""
    print("开始执行测试用例...")

    # 执行pytest命令，生成allure结果
    cmd = [
        sys.executable, "-m", "pytest",
        "--alluredir=./allure-results",
        "--clean-alluredir"
    ]

    # 如果需要指定测试目录或文件，可以添加
    # cmd.extend(["tests/"])  # 指定测试目录

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("测试执行完成")
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行测试时出错: {e}")
        return False


def generate_allure_report():
    """生成Allure报告"""
    print("生成Allure报告...")

    cmd = [
        "allure", "generate",
        "./allure-results",
        "-o", "./allure-report",
        "--clean"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Allure报告生成成功")
            return True
        else:
            print("Allure报告生成失败")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except FileNotFoundError:
        print("错误：未找到allure命令，请确保已安装allure-commandline")
        return False
    except Exception as e:
        print(f"生成报告时出错: {e}")
        return False


def main():
    """主函数"""
    # 配置参数
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/3886da75-cf80-4b53-80f5-f9ca829be053"  # 替换为你的webhook
    report_dir = "./allure-report"
    report_url = "http://your-server.com/reports/allure-report"  # 可选，报告访问地址

    # 执行测试
    test_success = run_tests()

    if not test_success:
        print("测试执行失败")
        # 也可以选择发送失败通知
        # send_feishu_report(webhook_url, "", "测试执行失败")
        return

    # 生成报告
    report_success = generate_allure_report()

    if not report_success:
        print("报告生成失败")
        return

    # 发送报告到飞书
    print("发送报告到飞书...")
    send_feishu_report(webhook_url, report_dir, report_url)
    print("报告发送完成")


if __name__ == "__main__":
    main()
