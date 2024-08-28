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
                             {"username": "zhang20121104", "password": "playwright123"},
                         },
                    "playwright0":
                        {"测试员":
                             {"username": "winni1", "password": "playwright001"},
                         "测试经理":
                             {"username": "tracy2012", "password": "playwright123"},
                         },
                    }

        return user[env][username]
