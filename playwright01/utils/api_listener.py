from playwright.sync_api import TimeoutError

class ApiResponseListener:
    def __init__(self, page, target_url):
        self.page = page
        self.target_url = target_url
        self.response_data = None

    def wait_for_response_and_capture(self, timeout=10000):
        try:
            with self.page.expect_response(lambda res: self.target_url in res.url, timeout=timeout) as response_info:
                # 在这里你可以触发请求（比如点击按钮），或者等待某个异步请求发生
                pass  # 如果你已经在别处触发了请求，这里可以不做任何事

            response = response_info.value
            print("接口 URL:", response.url)
            try:
                self.response_data = response.json()
                print("接口返回值（JSON）:", self.response_data)
            except TimeoutError:
                print("接口响应超时")
            except Exception as e:
                self.response_data = response.text()
                print("接口返回值（非JSON）:", self.response_data)

        except TimeoutError:
            print(f"等待接口响应超时：{self.target_url}")
        except Exception as e:
            print("发生异常:", e)

    def get_response_data(self):
        return self.response_data