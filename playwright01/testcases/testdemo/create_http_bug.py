from utils.http_util import HttpClient

# 创建客户端（自动跳过 SSL 证书验证）
with HttpClient(
        base_url="https://www.cat2bug.com:8022/prod-api",
        verify_ssl=False,  # 跳过 SSL 验证
        retry_times=3  # 重试 3 次
) as client:
    # 1. 登录获取 Token
    login_result = client.post("/login", json_data={
        "username": "xxx",
        "password": "xxx123456"
    })

    print("登录结果:", login_result)

    # 提取 Token
    token = login_result.get("data", {}).get("token", "")

    # 2. 创建缺陷
    defect_result = client.post(
        "/system/defect",
        json_data={
            "defectId": None,
            "defectType": "BUG",
            "defectName": "【自动化测试】测试BUG",
            "defectDescribe": "测试用例执行失败",
            "defectName": 'xxx',
            "projectId": 259,
            "handleBy": [454],
            "defectLevel": "middle",
            "srcHost": "https://www.cat2bug.com:8022"
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=UTF-8"
        }
    )

    print("创建结果:", defect_result)


    # {
    #     "defectId": null,
    #     "defectType": "BUG",
    #     "defectName": "xxxx",
    #     "defectDescribe": "xxxxxxxxxxxxxxxx",
    #     "annexUrls": null,
    #     "imgUrls": null,
    #     "projectId": 259,
    #     "testPlanId": null,
    #     "caseId": null,
    #     "dataSources": null,
    #     "dataSourcesParams": null,
    #     "moduleId": null,
    #     "moduleVersion": null,
    #     "createBy": null,
    #     "updateTime": null,
    #     "createTime": null,
    #     "updateBy": null,
    #     "defectState": null,
    #     "caseStepId": 0,
    #     "handleBy": [
    #         454
    #     ],
    #     "handleTime": null,
    #     "defectLevel": "middle",
    #     "srcHost": "https://www.cat2bug.com:8022"
    # }