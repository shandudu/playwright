from utils.http_util import HttpClient

with HttpClient(base_url="https://www.cat2bug.com:8022/prod-api") as client:
    # 登录获取token
    data =  {
  "username": "demo",
  "password": "123456"
}

    # 注意使用正确的登录路径
    result = client.post("/login", json_data=data)
    print("登录响应:", result)

    # 安全地提取token
    token = result.get('data', {}).get('token') if result.get('status_code') == 200 else None

    if not token:
        print("获取token失败")
        exit()

    print(f"Token: {token}")
    # 提交bug数据
    bug_data = {
    "defectId": None,
    "defectType": "BUG",
    "defectName": "测试",
    "defectDescribe": "aaa",
    "annexUrls": None,
    "imgUrls": None,
    "projectId": 124,
    "testPlanId": None,
    "caseId": None,
    "dataSources": None,
    "dataSourcesParams": None,
    "moduleId": None,
    "moduleVersion": None,
    "createBy": None,
    "updateTime": None,
    "createTime": None,
    "updateBy": None,
    "defectState": None,
    "caseStepId": 0,
    "handleBy": [213],
    "handleTime": None,
    "defectLevel": "middle",
    "srcHost": "https://www.cat2bug.com:8022"
}
    # 正确的请求头配置
    headers = {
        'authorization': token,
        'Accept': "*/*",
        'Content-Type': "application/json; charset=UTF-8"
    }

    # 方法1: 直接使用 json_data 参数 (推荐)
    result = client.post("/system/defect", json_data=bug_data, headers=headers)
    print("方法1提交结果:", result)
    # 安全地提取token
    projectNum = result.get('data', {}).get('data').get('projectNum') if result.get('status_code') == 200 else None
    print("bug编号:", projectNum)
