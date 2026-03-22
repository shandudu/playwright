class MyData:
    def __init__(self, local=True, execl=None, yaml=None, feishu=None):
        self.local = local
        self.execl = execl
        self.yaml = yaml
        self.feishu = feishu

    def userinfo(self, env, username):
        user = ""
        if self.execl:
            pass
            # todo 把execl转换成字典的方法
        elif self.yaml:
            pass
            # todo 把yaml转换成字典的方法
        elif self.feishu:
            pass
            # todo 把feishu转换成字典的方法
        elif self.local:
            user = {"playwright":
                        {"测试员":
                             {"username": "winni", "password": "playwright001"},
                             # {"username": "xxx_98", "password": "syx201314"},
                         "测试经理":
                             {"username": "xxx_98", "password": "syx201314"},
                         },
                    "cat2bug":
                        {"测试员":
                             {"username": "xxx", "password": "xxx123456"},
                         },
                    "macrozheng":
                        {"测试员":
                             {"username": "admin", "password": "macro123"},

                         },
                    }

        return user[env][username]
