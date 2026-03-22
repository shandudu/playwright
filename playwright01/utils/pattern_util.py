"""
Pattern Util - 正则模式工具箱
=============================

一个综合性的正则表达式处理工具类，整合了日常开发中常用的正则处理逻辑。

功能模块：
- 🏷️ 标题处理：页面标题、时间戳、日期等后缀清理
- 🔍 数据提取：从文本中提取数字、邮箱、URL、身份证等
- ✅ 验证工具：验证格式是否符合预期
- 🧹 文本清理：去除多余空格、特殊字符等
- 📝 模式库：常用正则表达式预定义

Author: MiniMax Agent
"""

import re
from typing import Optional, List, Dict, Any, Callable, Union, Pattern
from dataclasses import dataclass, field
from enum import Enum
import logging
from functools import wraps

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据结构定义
# =============================================================================

@dataclass
class CleanRule:
    """
    清理规则数据类

    Attributes:
        name: 规则名称
        pattern: 正则表达式模式
        replacement: 替换字符串，None 表示删除匹配部分
        description: 规则描述
        priority: 优先级，数字越大优先级越高
    """
    name: str
    pattern: str
    replacement: Optional[str] = None
    description: str = ""
    priority: int = 0


@dataclass
class ExtractResult:
    """提取结果数据类"""
    success: bool
    value: Any = None
    match_obj: Optional[re.Match] = None
    error: Optional[str] = None


@dataclass
class ValidationResult:
    """验证结果数据类"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    value: Any = None


# =============================================================================
# 常用正则模式库
# =============================================================================

class RegexPatterns:
    """
    常用正则表达式模式库

    Usage:
        pattern = RegexPatterns.EMAIL
        if re.match(pattern, email):
            print("Valid email")
    """

    # ==================== 基础模式 ====================
    ANY_DIGIT = r"\d"
    ANY_LETTER = r"[a-zA-Z]"
    ANY_CHINESE = r"[\u4e00-\u9fff]"
    ANY_ALPHANUMERIC = r"[a-zA-Z0-9]"

    # ==================== 数字相关 ====================
    INTEGER = r"-?\d+"  # 整数
    POSITIVE_INTEGER = r"\d+"  # 正整数
    NEGATIVE_INTEGER = r"-\d+"  # 负整数
    DECIMAL = r"-?\d+\.?\d*"  # 小数
    PERCENTAGE = r"\d+\.?\d*%"  # 百分比
    PHONE_CN = r"1[3-9]\d{9}"  # 中国手机号
    PHONE_CN_WITH_AREA = r"\d{3,4}-?\d{7,8}"  # 中国固定电话
    PHONE_INTERNATIONAL = r"\+86-?\d{3,4}-?\d{7,8}"  # 国际电话
    ZIP_CODE = r"\d{6}"  # 中国邮编

    # ==================== 标识符 ====================
    EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # 邮箱
    URL = r"https?://[^\s<>\"]+/?[^\s<>\"]*"  # URL
    DOMAIN = r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"  # 域名
    IP_V4 = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IPv4
    IP_V6 = r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"  # IPv6

    # ==================== 身份证和证件 ====================
    ID_CARD_CN = r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]"  # 中国身份证
    PASSPORT_CN = r"[a-zA-Z]\d{8}"  # 中国护照
    HK_MACAO_PASS = r"[HM]\d{10}"  # 港澳通行证

    # ==================== 时间和日期 ====================
    TIME_HMS = r"\d{2}:\d{2}:\d{2}"  # 时分秒 HH:MM:SS
    TIME_HMS_WITH_MS = r"\d{2}:\d{2}:\d{2}\.\d+"  # 带毫秒
    TIME_HM = r"\d{2}:\d{2}"  # 时分 HH:MM
    DATE_YYYY_MM_DD = r"\d{4}-\d{2}-\d{2}"  # 日期 YYYY-MM-DD
    DATE_YYYYMMDD = r"\d{8}"  # 日期 YYYYMMDD
    DATE_SLASH = r"\d{4}/\d{2}/\d{2}"  # 日期 YYYY/MM/DD
    DATETIME_ISO = r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"  # ISO日期时间
    DATETIME_CN = r"\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}"  # 中文日期

    # ==================== 金额和价格 ====================
    PRICE_CN = r"¥\s*\d+\.?\d*"  # 人民币价格
    PRICE_CN_WAN = r"\d+\.?\d*[万千]元"  # 万元
    PRICE_USD = r"\$\s*\d+\.?\d*"  # 美元价格
    PRICE_EUR = r"€\s*\d+\.?\d*"  # 欧元价格
    AMOUNT_WITH_UNIT = r"\d+\.?\d*\s*[万千百亿个只条件台部套]?"  # 带单位的数量

    # ==================== 代码和标识 ====================
    ORDER_ID = r"[A-Z]{1,3}\d{10,}"  # 订单号
    INVOICE_NO = r"[A-Z]{2}\d{12}"  # 发票号
    TRADE_NO = r"\d{20,}"  # 交易号
    VERSION = r"v\d+\.\d+\.\d+"  # 版本号
    SEMVER = r"\d+\.\d+\.\d+(?:-[\w.]+)?"  # 语义化版本
    UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"  # UUID
    MAC_ADDRESS = r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}"  # MAC地址

    # ==================== HTML和XML ====================
    HTML_TAG = r"<[^>]+>"  # HTML标签
    HTML_IMAGE = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'  # 图片标签
    HTML_LINK = r'<a[^>]+href=["\']([^"\']+)["\']'  # 链接标签
    XML_TAG = r"</?[a-zA-Z][a-zA-Z0-9]*[^>]*>"  # XML标签

    # ==================== 文件路径 ====================
    FILE_PATH_UNIX = r"/(?:[^/\0]+/?)+"  # Unix路径
    FILE_PATH_WINDOWS = r"[a-zA-Z]:\\(?:[^\\\0]+/?)+"  # Windows路径
    FILE_EXTENSION = r"\.[a-zA-Z0-9]+"  # 文件扩展名
    FILE_NAME = r"[^\/\\\0]+\.[a-zA-Z0-9]+"  # 文件名

    # ==================== 其他常用 ====================
    CHINESE_NAME = r"[\u4e00-\u9fff]{2,4}"  # 中文姓名
    CAR_LICENSE_PLATE = r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{4,5}[A-Z0-9挂学警港澳]"  # 车牌
    VIN_CODE = r"[A-HJ-NPR-Z0-9]{17}"  # 车架号
    CREDIT_CARD = r"\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}"  # 信用卡


# =============================================================================
# 标题处理工具
# =============================================================================

class TitleCleaner:
    """
    页面标题清理器

    提供多种页面标题后缀清理功能，如时间戳、日期、网站后缀等。
    """

    # 预设的清理规则
    DEFAULT_RULES: List[CleanRule] = [
        # 时间戳后缀：HH:MM:SS
        CleanRule(
            name="time_suffix",
            pattern=r"\s+\d{2}:\d{2}:\d{2}$",
            description="清理时间戳后缀（如：页面标题 12:34:56）",
            priority=100
        ),
        # 带毫秒的时间戳
        CleanRule(
            name="time_with_millis",
            pattern=r"\s+\d{2}:\d{2}:\d{2}\.\d+$",
            description="清理带毫秒的时间戳后缀",
            priority=100
        ),
        # 12小时制时间（带AM/PM）
        CleanRule(
            name="time_12hour",
            pattern=r"\s+\d{1,2}:\d{2}:\d{2}\s*(?:AM|PM|am|pm)$",
            description="清理12小时制时间后缀",
            priority=100
        ),
        # 日期后缀：YYYY-MM-DD 或 YYYY/MM/DD
        CleanRule(
            name="date_standard",
            pattern=r"\s+\d{4}[-/]\d{1,2}[-/]\d{1,2}$",
            description="清理标准日期后缀（如：2024-03-22）",
            priority=90
        ),
        # 短日期后缀：MM-DD 或 MM/DD
        CleanRule(
            name="date_short",
            pattern=r"\s+\d{1,2}[-/]\d{1,2}$",
            description="清理短日期后缀（如：03-22）",
            priority=80
        ),
        # 常见网站后缀
        CleanRule(
            name="site_suffix",
            pattern=r"\s*[-–—―|]\s*[^\s]+$",
            description="清理网站后缀（如：- 网站名）",
            priority=70
        ),
        # 括号内容后缀
        CleanRule(
            name="bracket_suffix",
            pattern=r"\s*[（\(）【\[][^\)）\]]+[）\）】\]]$",
            description="清理括号内容后缀",
            priority=60
        ),
        # 动态数字标识
        CleanRule(
            name="dynamic_number",
            pattern=r"\s*[(#\[【]\d+[)\]#\]]+$",
            description="清理动态数字标识",
            priority=50
        ),
        # 尾部多余空格
        CleanRule(
            name="trailing_space",
            pattern=r"\s+$",
            description="清理尾部空格",
            priority=10
        ),
    ]

    def __init__(self, rules: Optional[List[CleanRule]] = None):
        """初始化标题清理器"""
        self.rules: List[CleanRule] = rules or self.DEFAULT_RULES.copy()
        self.rules.sort(key=lambda x: x.priority, reverse=True)

    def add_rule(self, rule: CleanRule) -> "TitleCleaner":
        """添加清理规则"""
        self.rules.append(rule)
        self.rules.sort(key=lambda x: x.priority, reverse=True)
        return self

    def remove_rule(self, rule_name: str) -> "TitleCleaner":
        """移除指定规则"""
        self.rules = [r for r in self.rules if r.name != rule_name]
        return self

    def clean(
        self,
        title: str,
        skip_rules: Optional[List[str]] = None,
        preserve_brackets: bool = False
    ) -> str:
        """
        清理标题

        Args:
            title: 原始标题
            skip_rules: 要跳过的规则名称列表
            preserve_brackets: 是否保留括号内容

        Returns:
            清理后的标题
        """
        if not title:
            return ""

        skip_rules = skip_rules or []
        result = title

        for rule in self.rules:
            if rule.name in skip_rules:
                continue
            if preserve_brackets and rule.name in ["bracket_suffix", "dynamic_number"]:
                continue

            try:
                new_result = re.sub(rule.pattern, rule.replacement or "", result)
                if new_result != result:
                    logger.debug(f"应用规则 '{rule.name}': '{result}' -> '{new_result}'")
                    result = new_result
            except re.error as e:
                logger.warning(f"规则 '{rule.name}' 正则表达式错误: {e}")

        # 清理多余空格
        result = re.sub(r"\s+", " ", result).strip()

        return result

    def clean_simple(self, title: str) -> str:
        """
        简单清理（仅清理时间戳后缀）

        Args:
            title: 原始标题

        Returns:
            清理后的标题
        """
        if not title:
            return ""
        return re.sub(r"\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?$", "", title).strip()


# =============================================================================
# 提取工具
# =============================================================================

class ExtractUtil:
    """
    数据提取工具

    提供从文本中提取各种类型数据的功能。
    """

    @staticmethod
    def extract_number(text: str, pattern: str = None) -> Optional[Union[int, float]]:
        """
        提取数字

        Args:
            text: 原始文本
            pattern: 自定义模式，默认提取整数或小数

        Returns:
            提取的数字，失败返回 None
        """
        pattern = pattern or r"-?\d+\.?\d*"
        match = re.search(pattern, text)
        if match:
            value = match.group()
            return float(value) if "." in value else int(value)
        return None

    @staticmethod
    def extract_all_numbers(text: str, as_float: bool = False) -> List[Union[int, float]]:
        """
        提取所有数字

        Args:
            text: 原始文本
            as_float: 是否转换为浮点数

        Returns:
            数字列表
        """
        matches = re.findall(r"-?\d+\.?\d*", text)
        if as_float:
            return [float(m) for m in matches]
        return [int(float(m)) if "." not in m else float(m) for m in matches]

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """提取邮箱"""
        match = re.search(RegexPatterns.EMAIL, text)
        return match.group() if match else None

    @staticmethod
    def extract_all_emails(text: str) -> List[str]:
        """提取所有邮箱"""
        return re.findall(RegexPatterns.EMAIL, text)

    @staticmethod
    def extract_url(text: str) -> Optional[str]:
        """提取URL"""
        match = re.search(RegexPatterns.URL, text)
        return match.group() if match else None

    @staticmethod
    def extract_all_urls(text: str) -> List[str]:
        """提取所有URL"""
        return re.findall(RegexPatterns.URL, text)

    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """提取手机号（中国大陆）"""
        match = re.search(RegexPatterns.PHONE_CN, text)
        return match.group() if match else None

    @staticmethod
    def extract_all_phones(text: str) -> List[str]:
        """提取所有手机号"""
        return re.findall(RegexPatterns.PHONE_CN, text)

    @staticmethod
    def extract_id_card(text: str) -> Optional[str]:
        """提取身份证号"""
        match = re.search(RegexPatterns.ID_CARD_CN, text)
        return match.group() if match else None

    @staticmethod
    def extract_chinese(text: str) -> str:
        """提取所有中文"""
        return "".join(re.findall(RegexPatterns.ANY_CHINESE, text))

    @staticmethod
    def extract_by_pattern(text: str, pattern: str, group: int = 0) -> Optional[str]:
        """
        使用自定义正则提取

        Args:
            text: 原始文本
            pattern: 正则表达式
            group: 要提取的分组索引

        Returns:
            提取的内容
        """
        match = re.search(pattern, text)
        if match:
            return match.group(group)
        return None

    @staticmethod
    def extract_between(text: str, start: str, end: str, include_markers: bool = False) -> Optional[str]:
        """
        提取两个标记之间的内容

        Args:
            text: 原始文本
            start: 开始标记
            end: 结束标记
            include_markers: 是否包含标记

        Returns:
            提取的内容
        """
        pattern = f"{re.escape(start)}(.*?){re.escape(end)}"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1)
            if include_markers:
                return f"{start}{content}{end}"
            return content
        return None

    @staticmethod
    def extract_json_field(text: str, field: str) -> Optional[str]:
        """
        简单提取JSON字段（不依赖json库）

        Args:
            text: 包含JSON的文本
            field: 字段名

        Returns:
            字段值
        """
        # 匹配 "field": "value" 或 'field': 'value'
        pattern = rf'["\']{field}["\']\s*:\s*["\']([^"\']*)["\']'
        match = re.search(pattern, text)
        if match:
            return match.group(1)

        # 匹配 "field": value (数字或布尔值)
        pattern = rf'["\']{field}["\']\s*:\s*(\d+\.?\d*|true|false|null)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None


# =============================================================================
# 验证工具
# =============================================================================

class ValidateUtil:
    """
    数据验证工具

    提供各种数据格式验证功能。
    """

    @staticmethod
    def is_email(value: str) -> bool:
        """验证邮箱"""
        return bool(re.fullmatch(RegexPatterns.EMAIL, value))

    @staticmethod
    def is_url(value: str) -> bool:
        """验证URL"""
        return bool(re.fullmatch(RegexPatterns.URL, value))

    @staticmethod
    def is_phone_cn(value: str) -> bool:
        """验证中国手机号"""
        return bool(re.fullmatch(RegexPatterns.PHONE_CN, value))

    @staticmethod
    def is_id_card_cn(value: str) -> bool:
        """验证中国身份证号"""
        if not re.fullmatch(RegexPatterns.ID_CARD_CN, value):
            return False
        # 校验最后一位
        if len(value) == 18:
            factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = "10X98765432"
            total = sum(int(value[i]) * factors[i] for i in range(17))
            return check_codes[total % 11] == value[-1].upper()
        return True

    @staticmethod
    def is_ip_v4(value: str) -> bool:
        """验证IPv4地址"""
        return bool(re.fullmatch(RegexPatterns.IP_V4, value))

    @staticmethod
    def is_postal_code(value: str) -> bool:
        """验证中国邮编"""
        return bool(re.fullmatch(RegexPatterns.ZIP_CODE, value))

    @staticmethod
    def is_version(value: str) -> bool:
        """验证版本号 (v1.2.3 或 1.2.3)"""
        pattern = r"v?\d+\.\d+\.\d+(?:-[\w.]+)?"
        return bool(re.fullmatch(pattern, value))

    @staticmethod
    def is_plate_number(value: str) -> bool:
        """验证车牌号"""
        return bool(re.fullmatch(RegexPatterns.CAR_LICENSE_PLATE, value))

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        """验证是否匹配自定义正则"""
        return bool(re.fullmatch(pattern, value))

    @staticmethod
    def contains_pattern(value: str, pattern: str) -> bool:
        """验证是否包含指定模式"""
        return bool(re.search(pattern, value))

    @staticmethod
    def validate_length(
        value: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> ValidationResult:
        """验证字符串长度"""
        errors = []
        length = len(value)

        if min_length is not None and length < min_length:
            errors.append(f"长度({length})小于最小要求({min_length})")

        if max_length is not None and length > max_length:
            errors.append(f"长度({length})超过最大限制({max_length})")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            value=value
        )

    @staticmethod
    def validate_range(
        value: Union[int, float],
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None
    ) -> ValidationResult:
        """验证数值范围"""
        errors = []

        if min_value is not None and value < min_value:
            errors.append(f"数值({value})小于最小值({min_value})")

        if max_value is not None and value > max_value:
            errors.append(f"数值({value})超过最大值({max_value})")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            value=value
        )


# =============================================================================
# 文本清理工具
# =============================================================================

class TextCleaner:
    """
    文本清理工具

    提供各种文本清理功能。
    """

    @staticmethod
    def remove_whitespace(text: str, preserve_spaces: bool = True) -> str:
        """
        去除多余空白字符

        Args:
            text: 原始文本
            preserve_spaces: 是否保留单词间单个空格

        Returns:
            清理后的文本
        """
        if preserve_spaces:
            # 多个空格合并为一个
            return re.sub(r" +", " ", text).strip()
        else:
            # 完全去除空格
            return re.sub(r"\s+", "", text)

    @staticmethod
    def remove_newlines(text: str, preserve_spaces: bool = True) -> str:
        """
        去除换行符

        Args:
            text: 原始文本
            preserve_spaces: 是否用空格替换换行符

        Returns:
            清理后的文本
        """
        if preserve_spaces:
            return re.sub(r"[\r\n]+", " ", text).strip()
        else:
            return re.sub(r"[\r\n]+", "", text)

    @staticmethod
    def remove_html_tags(text: str, preserve_content: bool = True) -> str:
        """
        去除HTML标签

        Args:
            text: 原始文本
            preserve_content: 是否保留标签内容

        Returns:
            清理后的文本
        """
        if preserve_content:
            # 替换为单个空格
            return re.sub(r"<[^>]+>", " ", text)
        else:
            return re.sub(r"<[^>]+>", "", text)

    @staticmethod
    def remove_special_chars(text: str, keep_chinese: bool = True) -> str:
        """
        去除特殊字符

        Args:
            text: 原始文本
            keep_chinese: 是否保留中文

        Returns:
            清理后的文本
        """
        if keep_chinese:
            pattern = r"[^a-zA-Z0-9\u4e00-\u9fff\s\-.,!?。，！？]"
        else:
            pattern = r"[^a-zA-Z0-9\s\-.,!?。，！？]"

        return re.sub(pattern, "", text)

    @staticmethod
    def normalize_spaces(text: str) -> str:
        """
        标准化空格（去除首尾空格，多个空格合并为一个）

        Args:
            text: 原始文本

        Returns:
            标准化后的文本
        """
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        截断文本

        Args:
            text: 原始文本
            max_length: 最大长度
            suffix: 截断后缀

        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def extract_and_clean_numbers(text: str) -> str:
        """
        仅保留数字

        Args:
            text: 原始文本

        Returns:
            仅包含数字的文本
        """
        return re.sub(r"\D+", "", text)


# =============================================================================
# 便捷函数
# =============================================================================

# 创建默认清理器实例
_default_title_cleaner = TitleCleaner()


def clean_title(title: str, **kwargs) -> str:
    """
    清理页面标题的便捷函数

    Args:
        title: 原始标题
        **kwargs: 传递给 TitleCleaner.clean() 的参数

    Returns:
        清理后的标题
    """
    return _default_title_cleaner.clean(title, **kwargs)


def clean_title_simple(title: str) -> str:
    """
    简单清理标题（仅清理时间戳）

    Args:
        title: 原始标题

    Returns:
        清理后的标题
    """
    return _default_title_cleaner.clean_simple(title)


def extract_numbers(text: str) -> List[Union[int, float]]:
    """提取所有数字"""
    return ExtractUtil.extract_all_numbers(text)


def extract_urls(text: str) -> List[str]:
    """提取所有URL"""
    return ExtractUtil.extract_all_urls(text)


def extract_emails(text: str) -> List[str]:
    """提取所有邮箱"""
    return ExtractUtil.extract_all_emails(text)


def is_valid_email(value: str) -> bool:
    """验证邮箱"""
    return ValidateUtil.is_email(value)


def is_valid_phone(value: str) -> bool:
    """验证手机号"""
    return ValidateUtil.is_phone_cn(value)


def remove_html(text: str) -> str:
    """去除HTML标签"""
    return TextCleaner.remove_html_tags(text)


def normalize_text(text: str) -> str:
    """标准化文本"""
    return TextCleaner.normalize_spaces(text)


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    # 数据结构
    "CleanRule",
    "ExtractResult",
    "ValidationResult",

    # 模式库
    "RegexPatterns",

    # 工具类
    "TitleCleaner",
    "ExtractUtil",
    "ValidateUtil",
    "TextCleaner",

    # 便捷函数
    "clean_title",
    "clean_title_simple",
    "extract_numbers",
    "extract_urls",
    "extract_emails",
    "is_valid_email",
    "is_valid_phone",
    "remove_html",
    "normalize_text",
]
