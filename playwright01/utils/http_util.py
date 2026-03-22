"""
HTTP 客户端工具类 - 优化版

基于 httpx 库，支持：
- SSL 证书验证跳过（适用于内网环境）
- 自动重试机制
- 请求/响应日志记录
- Cookie 会话管理
- 代理支持
- 同步和异步请求

Author: MiniMax Agent
"""

import httpx
from typing import Optional, Dict, Any, Union, List
import json
import asyncio
from playwright01.utils.logger import *
import time
from contextlib import asynccontextmanager




class HttpClient:
    """
    基于 httpx 库的 HTTP 客户端工具类
    支持同步和异步请求，自动处理 SSL 证书问题
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = False,  # SSL 证书验证，默认跳过
        retry_times: int = 3,  # 重试次数
        retry_delay: float = 1.0,  # 重试延迟（秒）
        proxies: Optional[Dict[str, str]] = None,  # 代理配置
        enable_log: bool = True  # 是否启用日志
    ):
        """
        初始化 HTTP 客户端

        Args:
            base_url: 基础 URL
            timeout: 超时时间（秒）
            headers: 默认请求头
            verify_ssl: 是否验证 SSL 证书，默认 False（跳过验证）
            retry_times: 重试次数，默认 3 次
            retry_delay: 重试延迟，默认 1 秒
            proxies: 代理配置，如 {"http": "http://proxy:8080"}
            enable_log: 是否启用日志记录
        """
        self.base_url = base_url.rstrip('/') if base_url else ""
        self.timeout = timeout
        self.default_headers = headers or {}
        self.verify_ssl = verify_ssl
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.proxies = proxies
        self.enable_log = enable_log

        # 配置 httpx 客户端参数
        client_kwargs = {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "headers": self.default_headers,
            "verify": self.verify_ssl,  # SSL 验证控制
            "follow_redirects": True,
            "cookies": httpx.Cookies()
        }

        if proxies:
            client_kwargs["proxies"] = proxies

        # 同步客户端
        self.client = httpx.Client(**client_kwargs)

        # 异步客户端配置
        async_kwargs = {
            "base_url": self.base_url,
            "timeout": self.timeout,
            "headers": self.default_headers,
            "verify": self.verify_ssl,
            "follow_redirects": True,
            "cookies": httpx.Cookies()
        }

        if proxies:
            async_kwargs["proxies"] = proxies

        self.async_client = httpx.AsyncClient(**async_kwargs)

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        if self.enable_log:
            logger.info(f"📤 [{method}] {url}")
            if kwargs.get('json'):
                logger.debug(f"📤 请求数据: {json.dumps(kwargs['json'], ensure_ascii=False)[:500]}")
            if kwargs.get('params'):
                logger.debug(f"📤 查询参数: {kwargs['params']}")

    def _log_response(self, method: str, url: str, status_code: int, response_data: Any, error: str = None):
        """记录响应日志"""
        if self.enable_log:
            if error:
                logger.error(f"📥 [{method}] {url} - ❌ 错误: {error}")
            else:
                status_icon = "✅" if status_code < 400 else "⚠️" if status_code < 500 else "❌"
                logger.info(f"📥 [{method}] {url} - {status_icon} {status_code}")
                if isinstance(response_data, dict):
                    logger.debug(f"📥 响应数据: {json.dumps(response_data, ensure_ascii=False)[:500]}")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        处理响应结果

        Args:
            response: httpx 响应对象

        Returns:
            统一格式的响应数据
        """
        try:
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")

            if content_type.startswith("application/json"):
                data = response.json()
            else:
                # 尝试解析为 JSON，失败则返回文本
                try:
                    data = response.json()
                except Exception:
                    data = response.text

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": data,
                "success": True,
                "error": None
            }
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {str(e)}"
            return {
                "status_code": e.response.status_code,
                "error": error_msg,
                "data": None,
                "success": False
            }
        except httpx.RequestError as e:
            error_msg = f"请求错误: {str(e)}"
            return {
                "status_code": None,
                "error": error_msg,
                "data": None,
                "success": False
            }
        except Exception as e:
            return {
                "status_code": None,
                "error": f"未知错误: {str(e)}",
                "data": None,
                "success": False
            }

    def _request_with_retry(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        带重试机制的请求

        Args:
            method: HTTP 方法
            url: 请求地址
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        last_error = None

        for attempt in range(self.retry_times):
            try:
                if method.upper() == "GET":
                    response = self.client.get(url, **kwargs)
                elif method.upper() == "POST":
                    response = self.client.post(url, **kwargs)
                elif method.upper() == "PUT":
                    response = self.client.put(url, **kwargs)
                elif method.upper() == "DELETE":
                    response = self.client.delete(url, **kwargs)
                elif method.upper() == "PATCH":
                    response = self.client.patch(url, **kwargs)
                else:
                    response = self.client.request(method, url, **kwargs)

                return self._handle_response(response)

            except Exception as e:
                last_error = str(e)
                if attempt < self.retry_times - 1:
                    logger.warning(f"请求失败，{self.retry_delay}秒后重试... ({attempt + 1}/{self.retry_times})")
                    time.sleep(self.retry_delay)
                    self.retry_delay *= 2  # 指数退避

        return {
            "status_code": None,
            "error": f"重试{self.retry_times}次后仍失败: {last_error}",
            "data": None,
            "success": False
        }

    # ==================== 同步方法 ====================

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送 GET 请求

        Args:
            url: 请求地址
            params: 查询参数
            headers: 请求头
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        self._log_request("GET", url, params=params)
        result = self._request_with_retry("GET", url, params=params, headers=headers, **kwargs)
        self._log_response("GET", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    def post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
             headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送 POST 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        self._log_request("POST", url, json=json_data, data=data)
        result = self._request_with_retry("POST", url, data=data, json=json_data, headers=headers, **kwargs)
        self._log_response("POST", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    def put(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
            headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送 PUT 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        self._log_request("PUT", url, json=json_data, data=data)
        result = self._request_with_retry("PUT", url, data=data, json=json_data, headers=headers, **kwargs)
        self._log_response("PUT", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送 DELETE 请求

        Args:
            url: 请求地址
            headers: 请求头
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        self._log_request("DELETE", url)
        result = self._request_with_retry("DELETE", url, headers=headers, **kwargs)
        self._log_response("DELETE", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    def patch(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
              headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        发送 PATCH 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        self._log_request("PATCH", url, json=json_data, data=data)
        result = self._request_with_retry("PATCH", url, data=data, json=json_data, headers=headers, **kwargs)
        self._log_response("PATCH", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    # ==================== 异步方法 ====================

    async def _async_request_with_retry(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        异步带重试机制的请求

        Args:
            method: HTTP 方法
            url: 请求地址
            **kwargs: 其他参数

        Returns:
            响应数据
        """
        last_error = None

        for attempt in range(self.retry_times):
            try:
                if method.upper() == "GET":
                    response = await self.async_client.get(url, **kwargs)
                elif method.upper() == "POST":
                    response = await self.async_client.post(url, **kwargs)
                elif method.upper() == "PUT":
                    response = await self.async_client.put(url, **kwargs)
                elif method.upper() == "DELETE":
                    response = await self.async_client.delete(url, **kwargs)
                elif method.upper() == "PATCH":
                    response = await self.async_client.patch(url, **kwargs)
                else:
                    response = await self.async_client.request(method, url, **kwargs)

                return self._handle_response(response)

            except Exception as e:
                last_error = str(e)
                if attempt < self.retry_times - 1:
                    logger.warning(f"异步请求失败，{self.retry_delay}秒后重试... ({attempt + 1}/{self.retry_times})")
                    await asyncio.sleep(self.retry_delay)
                    self.retry_delay *= 2

        return {
            "status_code": None,
            "error": f"重试{self.retry_times}次后仍失败: {last_error}",
            "data": None,
            "success": False
        }

    async def async_get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """异步发送 GET 请求"""
        self._log_request("ASYNC_GET", url, params=params)
        result = await self._async_request_with_retry("GET", url, params=params, headers=headers, **kwargs)
        self._log_response("ASYNC_GET", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    async def async_post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                         headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """异步发送 POST 请求"""
        self._log_request("ASYNC_POST", url, json=json_data, data=data)
        result = await self._async_request_with_retry("POST", url, data=data, json=json_data, headers=headers, **kwargs)
        self._log_response("ASYNC_POST", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    async def async_put(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                        headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """异步发送 PUT 请求"""
        self._log_request("ASYNC_PUT", url, json=json_data, data=data)
        result = await self._async_request_with_retry("PUT", url, data=data, json=json_data, headers=headers, **kwargs)
        self._log_response("ASYNC_PUT", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    async def async_delete(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """异步发送 DELETE 请求"""
        self._log_request("ASYNC_DELETE", url)
        result = await self._async_request_with_retry("DELETE", url, headers=headers, **kwargs)
        self._log_response("ASYNC_DELETE", url, result.get("status_code"), result.get("data"), result.get("error"))
        return result

    # ==================== 会话管理 ====================

    def set_cookie(self, key: str, value: str, **kwargs):
        """设置 Cookie"""
        self.client.cookies.set(key, value, **kwargs)

    def get_cookie(self, key: str) -> Optional[str]:
        """获取 Cookie"""
        return self.client.cookies.get(key)

    def clear_cookies(self):
        """清除所有 Cookie"""
        self.client.cookies.clear()

    def set_header(self, key: str, value: str):
        """设置默认请求头"""
        self.client.headers[key] = value
        self.default_headers[key] = value

    def remove_header(self, key: str):
        """移除默认请求头"""
        if key in self.client.headers:
            del self.client.headers[key]
        if key in self.default_headers:
            del self.default_headers[key]

    # ==================== 生命周期管理 ====================

    def close(self):
        """关闭客户端连接"""
        try:
            self.client.close()
            # 异步客户端关闭需要在事件循环中执行
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(self.async_client.aclose())
            else:
                try:
                    asyncio.run(self.async_client.aclose())
                except RuntimeError:
                    # 事件循环已在运行但没有asyncio.run可用
                    pass
            logger.debug("HTTP 客户端已关闭")
        except Exception as e:
            logger.error(f"关闭客户端时出错: {e}")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        self.close()


# ==================== 便捷函数 ====================

def create_client(
    base_url: str = "",
    verify_ssl: bool = False,
    **kwargs
) -> HttpClient:
    """
    便捷函数：创建 HttpClient 实例

    Args:
        base_url: 基础 URL
        verify_ssl: 是否验证 SSL 证书
        **kwargs: 其他参数

    Returns:
        HttpClient 实例
    """
    return HttpClient(base_url=base_url, verify_ssl=verify_ssl, **kwargs)


@asynccontextmanager
async def async_client_context(base_url: str = "", verify_ssl: bool = False, **kwargs):
    """
    异步上下文管理器便捷函数

    Args:
        base_url: 基础 URL
        verify_ssl: 是否验证 SSL 证书
        **kwargs: 其他参数

    Yields:
        HttpClient 实例
    """
    client = HttpClient(base_url=base_url, verify_ssl=verify_ssl, **kwargs)
    try:
        yield client
    finally:
        await client.async_client.aclose()
