import datetime
from typing import Optional, Literal


def return_time_add_days(days: int, time: Optional[Literal["/", "-", "datetime", "year"]] = "-"):
    """
    :param days: 增加的天数,可以为负数
    :param time: 格式  / 使用斜杠分隔符  - 使用中划线分隔符  datetime 使用datetime格式  year 使用年月日格式
    :return: 
    """
    if time == "/":
        return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y/%m/%d")
    elif time == "-":
        return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    elif time == "datetime":
        return datetime.datetime.now() + datetime.timedelta(days=days)
    elif time == "year":
        return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y年%m月%d日")
    else:
        return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime(str(time))

def get_now_datetime():
    #返回当前时间时间戳
    return datetime.datetime.now().timestamp()