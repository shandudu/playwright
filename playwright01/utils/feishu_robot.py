# utils/feishu_robot.py
import requests
import json
import os
import zipfile
from typing import Optional


def send_text_message(webhook_url, content):
    """发送文本消息到飞书机器人"""
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    return response.json()


def zip_report(report_dir, zip_path):
    """将报告目录压缩为zip文件"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(report_dir):
            for file in files:
                abs_file = os.path.join(root, file)
                arc_file = os.path.relpath(abs_file, report_dir)
                zipf.write(abs_file, arc_file)


def send_report_link(webhook_url, report_url, message="Allure测试报告已生成"):
    """发送报告链接到飞书"""
    import requests
    import json

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "测试报告",
                    "content": [
                        [{
                            "tag": "text",
                            "text": message + "\n"
                        }, {
                            "tag": "a",
                            "text": "点击查看报告",
                            "href": report_url
                        }]
                    ]
                }
            }
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    return response.json()


def send_feishu_report(webhook_url: str, report_dir: str, report_url: Optional[str] = None):
    """
    发送Allure报告到飞书

    Args:
        webhook_url: 飞书机器人webhook地址
        report_dir: Allure报告目录路径
        report_url: 报告访问URL（可选）
    """
    if not os.path.exists(report_dir):
        send_text_message(webhook_url, f"错误：报告目录 {report_dir} 不存在")
        return

    # 获取报告摘要信息
    summary = get_allure_summary(report_dir)

    if report_url:
        # 发送带链接的消息
        message = f"测试报告已生成\n"
        if summary:
            message += f"用例总数: {summary.get('total', 0)}\n"
            message += f"通过: {summary.get('passed', 0)}\n"
            message += f"失败: {summary.get('failed', 0)}\n"
            message += f"跳过: {summary.get('skipped', 0)}\n"

        send_report_link(webhook_url, report_url, message)
    else:
        # 只发送文本摘要
        message = "Allure测试报告已生成\n"
        if summary:
            message += f"用例总数: {summary.get('total', 0)}, "
            message += f"通过: {summary.get('passed', 0)}, "
            message += f"失败: {summary.get('failed', 0)}, "
            message += f"跳过: {summary.get('skipped', 0)}"

        send_text_message(webhook_url, message)


def get_allure_summary(report_dir):
    """从Allure报告中提取摘要信息"""
    summary_file = os.path.join(report_dir, "widgets", "summary.json")
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
                stat = summary.get('statistic', {})
                return {
                    'total': stat.get('total', 0),
                    'passed': stat.get('passed', 0),
                    'failed': stat.get('failed', 0),
                    'skipped': stat.get('skipped', 0)
                }
        except Exception:
            return None
    return None


if __name__ == '__main__':
    # 测试代码
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url"
    send_text_message(webhook_url, "测试消息")


def main():
    """主函数"""
    # 配置参数
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url"  # 替换为你的webhook
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

# 使用示例
if __name__ == "__main__":
    # 假设已经生成了报告到 allure-report 目录
    report_dir = "allure-report"
    zip_path = "allure-report.zip"

    # 压缩报告
    zip_report(report_dir, zip_path)

    # 发送报告链接（需要先将报告上传到可访问位置）
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/3886da75-cf80-4b53-80f5-f9ca829be053"
    report_url = "http://your-server.com/reports/allure-report"  # 报告访问地址

    result = send_report_link(webhook_url, report_url)
    print(result)

# if __name__ == '__main__':
#     print(send_text_message("https://open.feishu.cn/open-apis/bot/v2/hook/3886da75-cf80-4b53-80f5-f9ca829be053", "测试"))