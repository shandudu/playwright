from playwright01.data_module import *
from dataclasses import dataclass




@dataclass
class project_data_createProject(As_dict):
    # project_name: str = '自动化创建的项目集_time'
    # project_time: str = ''
    # fater_project: str = ''
    # child_project: str = ''
    项目集名称: str = "自动化创建的项目集_时间戳"
    项目集周期: str = ""
    父项目集: str = ""
    子项目集: str = ""


@dataclass
class project_data_createProject_temp(As_dict):
    项目集名称: str = "自动化创建的项目集_时间戳"
    项目集周期: str = ""
    父项目集: str = ""