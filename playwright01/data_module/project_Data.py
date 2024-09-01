from playwright01.data_module import *
from playwright01.dataclasses import dataclass




@dataclass
class project_data_createProject(As_dict):
    project_name: str = '自动化创建的项目集_time'
    project_time: str = ''
    fater_project: str = ''
    child_project: str = ''