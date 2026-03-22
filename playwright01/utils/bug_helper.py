from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from playwright01.data_module import globalconfig
from playwright01.utils.http_util import HttpClient
from playwright01.utils.logger import logger


class BugHelper:
    _cached_token: Optional[str] = None

    @staticmethod
    def get_bug_temp_dir() -> str:
        """获取缺陷相关的临时目录。"""
        project_dir = Path(__file__).resolve().parents[1]
        temp_dir = project_dir / ".temp" / "bug_files"
        temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"创建缺陷临时目录: {temp_dir}")
        return str(temp_dir)

    @staticmethod
    def _extract_module_key(test_identifier: str) -> Optional[str]:
        if not test_identifier:
            return None
        return Path(test_identifier.split("::")[0]).name or None

    @classmethod
    def get_assignee_from_test_case(cls, failed_test: Dict[str, Any]) -> str:
        """根据失败用例匹配负责人。"""
        module_key = cls._extract_module_key(failed_test.get("nodeid", "")) or cls._extract_module_key(
            failed_test.get("name", "")
        )
        if module_key:
            assignee = getattr(globalconfig, "BUG_ASSIGNMENT_RULES", {}).get(module_key)
            if assignee:
                return assignee
        return getattr(globalconfig, "DEFAULT_ASSIGNEE", "fallback_id")

    @staticmethod
    def normalize_failed_tests(failed_tests: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按 nodeid 去重，避免同一用例重复建单。"""
        unique_failed_tests: Dict[str, Dict[str, Any]] = {}
        for failed_test in failed_tests or []:
            if not isinstance(failed_test, dict):
                continue
            nodeid = failed_test.get("nodeid") or failed_test.get("name")
            if not nodeid:
                continue
            current_error = failed_test.get("error_message") or ""
            existing = unique_failed_tests.get(nodeid)
            if not existing or len(current_error) > len(existing.get("error_message") or ""):
                unique_failed_tests[nodeid] = failed_test
        return list(unique_failed_tests.values())

    @staticmethod
    def _get_api_base_url() -> str:
        return getattr(globalconfig, "BASE_URL", "https://www.cat2bug.com:8022/prod-api").rstrip("/")

    @staticmethod
    def _get_bug_host() -> str:
        return getattr(globalconfig, "BUG_URL", "https://www.cat2bug.com:8022").rstrip("/")

    @classmethod
    def login_and_get_token(cls, force_refresh: bool = False) -> Optional[str]:
        """登录缺陷系统并获取 token。"""
        if cls._cached_token and not force_refresh:
            return cls._cached_token

        configured_token = getattr(globalconfig, "ZENTAO_TOKEN", "")
        if configured_token and not force_refresh:
            cls._cached_token = configured_token
            return configured_token

        username = getattr(globalconfig, "USER", "")
        password = getattr(globalconfig, "PWD", "")
        if not username or not password:
            logger.warning("未配置 BUG 登录账号或密码，跳过缺陷创建")
            return None

        try:
            with HttpClient(
                base_url=cls._get_api_base_url(),
                verify_ssl=False,
                retry_times=3,
            ) as client:
                login_result = client.post(
                    "/login",
                    json_data={
                        "username": username,
                        "password": password,
                    },
                )
        except Exception as exc:
            logger.exception(f"登录缺陷系统失败: {exc}")
            return None

        if not login_result.get("success"):
            logger.warning(f"登录缺陷系统失败: {login_result.get('error')}")
            return None

        response_data = login_result.get("data") or {}
        token = response_data.get("token", "")
        if not token and isinstance(response_data.get("data"), dict):
            token = response_data["data"].get("token", "")

        if not token:
            logger.warning(f"登录成功但未获取到 token: {response_data}")
            return None

        cls._cached_token = token
        logger.info("缺陷系统登录成功，已获取 token")
        return token

    @classmethod
    def construct_bug_data(cls, failed_test: Dict[str, Any], **overrides: Any) -> Dict[str, Any]:
        """构造单条缺陷数据。"""
        test_name = failed_test.get("name") or failed_test.get("nodeid") or "unknown"
        error_message = failed_test.get("error_message") or "N/A"
        handle_by = overrides.get("handleBy")
        if not handle_by:
            assignee = cls.get_assignee_from_test_case(failed_test)
            handle_by = [assignee] if assignee else []

        return {
            "defectId": None,
            "defectType": overrides.get("defectType", "BUG"),
            "defectName": overrides.get("defectName", f"【自动测试】{test_name}"),
            "defectDescribe": overrides.get(
                "defectDescribe",
                f"测试用例执行失败\n用例: {test_name}\n错误信息:\n{error_message}",
            ),
            "annexUrls": overrides.get("annexUrls"),
            "imgUrls": overrides.get("imgUrls"),
            "projectId": overrides.get("projectId", 259),
            "testPlanId": overrides.get("testPlanId"),
            "caseId": overrides.get("caseId"),
            "dataSources": overrides.get("dataSources"),
            "dataSourcesParams": overrides.get("dataSourcesParams"),
            "moduleId": overrides.get("moduleId"),
            "moduleVersion": overrides.get("moduleVersion"),
            "createBy": overrides.get("createBy"),
            "updateTime": overrides.get("updateTime"),
            "createTime": overrides.get("createTime"),
            "updateBy": overrides.get("updateBy"),
            "defectState": overrides.get("defectState"),
            "caseStepId": overrides.get("caseStepId", 0),
            "handleBy": handle_by,
            "handleTime": overrides.get("handleTime"),
            "defectLevel": overrides.get("defectLevel", "middle"),
            "srcHost": overrides.get("srcHost", cls._get_bug_host()),
        }

    @classmethod
    def create_bug(cls, **payload: Any) -> Optional[Dict[str, Any]]:
        """创建单条缺陷。"""
        if getattr(globalconfig, "DEBUG_MODE", False):
            logger.info(f"DEBUG_MODE 已开启，模拟创建缺陷: {payload.get('defectName')}")
            return {"code": 200, "msg": "模拟成功", "data": payload}

        token = cls.login_and_get_token()
        if not token:
            return None

        try:
            with HttpClient(
                base_url=cls._get_api_base_url(),
                verify_ssl=False,
                retry_times=3,
            ) as client:
                result = client.post(
                    "/system/defect",
                    json_data=payload,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json;charset=UTF-8",
                    },
                )
        except Exception as exc:
            logger.exception(f"创建缺陷请求失败: {exc}")
            return None

        if result.get("success"):
            logger.info(f"创建缺陷成功: {payload.get('defectName')}")
        else:
            logger.warning(f"创建缺陷失败: {payload.get('defectName')} - {result.get('error')}")
        return result

    @classmethod
    def create_bugs_for_failed_tests(
        cls,
        failed_tests: Iterable[Dict[str, Any]],
        **defaults: Any,
    ) -> List[Dict[str, Any]]:
        """批量为失败用例创建缺陷。"""
        creation_results: List[Dict[str, Any]] = []
        for failed_test in cls.normalize_failed_tests(failed_tests):
            payload = cls.construct_bug_data(failed_test, **defaults)
            response = cls.create_bug(**payload)
            creation_results.append(
                {
                    "nodeid": failed_test.get("nodeid"),
                    "payload": payload,
                    "response": response,
                    "success": bool(response and response.get("success")),
                }
            )
        return creation_results
