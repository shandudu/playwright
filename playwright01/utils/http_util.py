import httpx
from typing import Optional, Dict, Any, Union
import json
import asyncio


class HttpClient:
    """
    基于 httpx 库的 HTTP 客户端工具类
    支持同步和异步请求
    """

    def __init__(self, base_url: str = "", timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """
        初始化 HTTP 客户端

        Args:
            base_url: 基础 URL
            timeout: 超时时间（秒）
            headers: 默认请求头
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.default_headers = headers or {}

        # 同步客户端
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.default_headers
        )

        # 异步客户端
        self.async_client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.default_headers
        )

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        处理响应结果

        Args:
            response: httpx 响应对象

        Returns:
            解析后的响应数据
        """
        try:
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.json() if response.headers.get("content-type", "").startswith(
                    "application/json") else response.text
            }
        except httpx.HTTPStatusError as e:
            return {
                "status_code": e.response.status_code,
                "error": str(e),
                "data": e.response.json() if e.response.headers.get("content-type", "").startswith(
                    "application/json") else e.response.text
            }
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    # 同步方法
    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送 GET 请求

        Args:
            url: 请求地址
            params: 查询参数
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = self.client.get(url, params=params, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    def post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送 POST 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = self.client.post(url, data=data, json=json_data, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    def put(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送 PUT 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = self.client.put(url, data=data, json=json_data, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        发送 DELETE 请求

        Args:
            url: 请求地址
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = self.client.delete(url, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    # 异步方法
    async def async_get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> \
    Dict[str, Any]:
        """
        异步发送 GET 请求

        Args:
            url: 请求地址
            params: 查询参数
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = await self.async_client.get(url, params=params, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    async def async_post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                         headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        异步发送 POST 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = await self.async_client.post(url, data=data, json=json_data, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    async def async_put(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                        headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        异步发送 PUT 请求

        Args:
            url: 请求地址
            data: 表单数据
            json_data: JSON 数据
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = await self.async_client.put(url, data=data, json=json_data, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    async def async_delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        异步发送 DELETE 请求

        Args:
            url: 请求地址
            headers: 请求头

        Returns:
            响应数据
        """
        try:
            response = await self.async_client.delete(url, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            return {
                "status_code": None,
                "error": str(e),
                "data": None
            }

    def close(self):
        """
        关闭客户端连接
        """
        self.client.close()
        if asyncio.get_event_loop().is_running():
            # 在事件循环运行时，安排异步关闭
            asyncio.create_task(self.async_client.aclose())
        else:
            # 如果事件循环未运行，直接关闭
            asyncio.run(self.async_client.aclose())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
