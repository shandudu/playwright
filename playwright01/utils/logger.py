# utils/logger.py
import logging
import os
from pathlib import Path
import sys
from datetime import datetime


class Logger:
    """
    自定义日志类，用于统一管理项目中的日志记录
    """

    def __init__(self, name: str = "playwright_ui_test", log_level: int = logging.INFO):
        """
        初始化日志器

        Args:
            name: 日志器名称
            log_level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """设置日志处理器"""
        # 创建日志目录
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)

        # 文件日志处理器
        log_file = log_dir / f"ui_test_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 控制台日志处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器到日志器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        """记录debug级别日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录info级别日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录warning级别日志"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录error级别日志"""
        self.logger.error(message)

    def critical(self, message: str):
        """记录critical级别日志"""
        self.logger.critical(message)

    def exception(self, message: str):
        """记录异常日志"""
        self.logger.exception(message)


# 创建全局日志实例
ui_logger = Logger()

# 为了兼容现有代码中的logger使用方式
logger = logging.getLogger("playwright_ui_test")

# 如果需要在其他模块中使用，可以这样导入：
# from playwright01.utils.logger import ui_logger
# 或者
# from playwright01.utils.logger import logger
