# run.py
import pytest
import os
import subprocess
import sys
import time
import threading
from utils.feishu_robot import send_feishu_report

# 配置常量 - 与pytest.ini保持一致
ALLURE_RESULTS_DIR = "D:/pythonProject/playwright/playwright01/.allure_report"
ALLURE_REPORT_DIR = "./allure-report"
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/3886da75-cf80-4b53-80f5-f9ca829be053"
ALLURE_SERVER_PORT = 13156  # 固定端口


class ReportPlugin:
    """自定义pytest插件用于报告生成和发送"""

    def pytest_sessionfinish(self, session, exitstatus):
        """测试会话结束后执行"""
        print("\n" + "=" * 50)
        print("测试执行完成，开始生成和发送报告...")
        print("=" * 50)

        if self.generate_allure_report():
            # 发送报告链接到飞书
            self.send_report_to_feishu()

    def generate_allure_report(self):
        """生成Allure报告"""
        print("正在生成Allure报告...")

        # 检查allure结果目录是否存在
        if not os.path.exists(ALLURE_RESULTS_DIR):
            print(f"警告：Allure结果目录 {ALLURE_RESULTS_DIR} 不存在")
            return False

        # 检查目录是否为空
        if not os.listdir(ALLURE_RESULTS_DIR):
            print(f"警告：Allure结果目录 {ALLURE_RESULTS_DIR} 为空")
            return False

        # 确保输出目录存在
        if not os.path.exists(ALLURE_REPORT_DIR):
            os.makedirs(ALLURE_REPORT_DIR)

        cmd = [
            "allure", "generate",
            ALLURE_RESULTS_DIR,
            "-o", ALLURE_REPORT_DIR,
            "--clean"
        ]

        try:
            print(f"执行命令: {' '.join(cmd)}")

            # 使用shell=True避免编码问题
            result = subprocess.run(
                ' '.join(cmd),
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ Allure报告生成成功")
                return True
            else:
                print("❌ Allure报告生成失败")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False

        except FileNotFoundError:
            print("错误：未找到allure命令，请确保已安装allure-commandline")
            return False
        except Exception as e:
            print(f"生成报告时出错: {e}")
            return False

    def start_allure_server_and_get_url(self):
        """启动Allure服务器并返回实际的服务器地址"""
        try:
            # 使用固定端口启动allure serve
            allure_command = f'allure serve {ALLURE_RESULTS_DIR} -p {ALLURE_SERVER_PORT}'
            print(f"Starting new Allure server: {allure_command}")

            # 启动Allure服务器
            process = subprocess.Popen(
                allure_command,
                shell=True,
                stdout=subprocess.DEVNULL,  # 隐藏输出
                stderr=subprocess.DEVNULL,  # 隐藏输出
            )

            # 等待服务器启动
            time.sleep(2)

            # 返回固定端口的URL
            url = f"http://localhost:{ALLURE_SERVER_PORT}/"
            print(f"✅ Allure服务器启动成功: {url}")
            return url

        except Exception as e:
            print(f"启动Allure服务器时出错: {e}")
            return None

    def send_report_to_feishu(self):
        """发送报告到飞书"""
        print("正在发送报告到飞书...")

        try:
            # 获取测试摘要信息
            summary_info = self.get_test_summary()

            # 启动Allure服务器并获取实际URL
            server_url = self.start_allure_server_and_get_url()

            # 构造消息
            message = "🎉 Allure测试报告已生成\n"
            if summary_info:
                message += f"📊 用例总数: {summary_info['total']}\n"
                message += f"✅ 通过: {summary_info['passed']}\n"
                message += f"❌ 失败: {summary_info['failed']}\n"
                message += f"⏭️ 跳过: {summary_info['skipped']}\n"

            if server_url:
                message += f"🔗 报告链接: {server_url}\n"
                message += "💡 Allure服务器已启动，请点击链接查看详细报告\n"
                message += "⚠️  请保持程序运行以维持服务器在线"
            else:
                message += "❌ Allure服务器启动失败\n"
                # 备用方案：提供本地文件路径
                index_path = os.path.abspath(os.path.join(ALLURE_REPORT_DIR, "index.html"))
                message += f"📁 本地报告路径: file:///{index_path.replace(os.sep, '/')}"

            # 发送带链接的消息
            from utils.feishu_robot import send_report_link
            send_report_link(FEISHU_WEBHOOK_URL, server_url, message)
            print("✅ 报告发送完成")
        except Exception as e:
            print(f"❌ 发送报告到飞书时出错: {e}")

    def get_test_summary(self):
        """从Allure报告中提取测试摘要"""
        try:
            summary_file = os.path.join(ALLURE_REPORT_DIR, "widgets", "summary.json")
            if os.path.exists(summary_file):
                import json
                with open(summary_file, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                    stat = summary.get('statistic', {})
                    return {
                        'total': stat.get('total', 0),
                        'passed': stat.get('passed', 0),
                        'failed': stat.get('failed', 0),
                        'skipped': stat.get('skipped', 0)
                    }
        except Exception as e:
            print(f"读取测试摘要时出错: {e}")
        return None


def main():
    """主函数"""
    print("🚀 开始执行测试流程...")

    # 创建插件实例
    report_plugin = ReportPlugin()

    # 调用pytest，传入插件
    exit_code = pytest.main(plugins=[report_plugin])

    print(f"🏁 测试执行完成，退出码: {exit_code}")
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
    print('执行完成')
