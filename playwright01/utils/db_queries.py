from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


class DbQueries:
    """Database query helper for test cases.

    This class expects a `db_client` instance that implements:
    `execute_query(sql: str, params: dict | None) -> list | None`
    """

    _ALLOWED_JOIN_TYPES = {"INNER", "LEFT", "RIGHT", "FULL"}

    def __init__(self, db_client: Any) -> None:
        self.db_client = db_client

    def production_join_query(
        self,
        main_table: str,
        joins: List[Dict[str, str]],
        select_fields: Optional[List[str]] = None,
        where_conditions: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list:
        """General multi-table JOIN query.

        Args:
            main_table: Main table with alias, e.g. "disposition dis".
            joins: JOIN config list.
            select_fields: Query fields list, defaults to all fields.
            where_conditions: Condition map, supports:
                - equal: {"col": "value"}
                - in: {"col": ["a", "b"]}
                - compare: {"col": {"$gt": 1, "$lte": 10}}
            order_by: ORDER BY expression, e.g. "dis.created_at DESC".
            limit: Positive integer limit.
        """
        if not isinstance(main_table, str) or not main_table.strip():
            raise ValueError("main_table must be a non-empty string")

        if joins is None:
            joins = []
        if not isinstance(joins, list):
            raise ValueError("joins must be a list")

        select_clause = self._build_select_clause(select_fields)
        join_sql = self._build_join_clause(joins)
        where_sql, params = self._build_where_clause(where_conditions)

        order_sql = f" ORDER BY {order_by}" if order_by else ""
        limit_sql = self._build_limit_clause(limit)

        query_sql = (
            f"SELECT {select_clause} "
            f"FROM {main_table.strip()} "
            f"{join_sql}{where_sql}{order_sql}{limit_sql}"
        )

        result = self.db_client.execute_query(query_sql, params)
        return result if result is not None else []

    def _build_select_clause(self, select_fields: Optional[List[str]]) -> str:
        if not select_fields:
            return "*"
        if not isinstance(select_fields, list):
            raise ValueError("select_fields must be a list of strings")

        cleaned_fields: List[str] = []
        for field in select_fields:
            if not isinstance(field, str) or not field.strip():
                raise ValueError(f"invalid field: {field!r}")
            cleaned_fields.append(field.strip())
        return ", ".join(cleaned_fields)

    def _build_join_clause(self, joins: List[Dict[str, str]]) -> str:
        join_parts: List[str] = []
        for join_cfg in joins:
            if not isinstance(join_cfg, dict):
                raise ValueError(f"invalid join config: {join_cfg!r}")

            join_type = str(join_cfg.get("type", "INNER")).upper().strip()
            table = str(join_cfg.get("table", "")).strip()
            on_expr = str(join_cfg.get("on", "")).strip()

            if join_type not in self._ALLOWED_JOIN_TYPES:
                raise ValueError(f"unsupported join type: {join_type}")
            if not table:
                raise ValueError(f"join table is required: {join_cfg!r}")
            if not on_expr:
                raise ValueError(f"join ON expression is required: {join_cfg!r}")

            join_parts.append(f"{join_type} JOIN {table} ON {on_expr}")

        return (" " + " ".join(join_parts)) if join_parts else ""

    def _build_limit_clause(self, limit: Optional[int]) -> str:
        if limit is None:
            return ""
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive int")
        return f" LIMIT {limit}"

    def _build_where_clause(
        self, where_conditions: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Build WHERE SQL and parameter map."""
        if not where_conditions:
            return "", {}
        if not isinstance(where_conditions, dict):
            raise ValueError("where_conditions must be a dict")

        params: Dict[str, Any] = {}
        where_parts: List[str] = []
        op_map = {
            "$gt": ">",
            "$gte": ">=",
            "$lt": "<",
            "$lte": "<=",
            "$ne": "!=",
        }

        for idx, (field, value) in enumerate(where_conditions.items()):
            if not isinstance(field, str) or not field.strip():
                raise ValueError(f"invalid where field: {field!r}")
            field = field.strip()

            if isinstance(value, list):
                if not value:
                    continue
                placeholders: List[str] = []
                for sub_idx, sub_value in enumerate(value):
                    param_key = f"in_{idx}_{sub_idx}"
                    placeholders.append(f":{param_key}")
                    params[param_key] = sub_value
                where_parts.append(f"{field} IN ({', '.join(placeholders)})")
                continue

            if isinstance(value, dict):
                for op_idx, (op_key, op_value) in enumerate(value.items()):
                    if op_key not in op_map:
                        raise ValueError(f"unsupported operator: {op_key}")
                    param_key = f"cond_{idx}_{op_idx}"
                    where_parts.append(f"{field} {op_map[op_key]} :{param_key}")
                    params[param_key] = op_value
                continue

            param_key = f"eq_{idx}"
            where_parts.append(f"{field} = :{param_key}")
            params[param_key] = value

        where_sql = f" WHERE {' AND '.join(where_parts)}" if where_parts else ""
        return where_sql, params


# from playwright01.utils.db_util import DatabaseUtil
# from playwright01.utils.db_queries import DbQueries
#
# db = DatabaseUtil(username, password, host, port, service_name)
# queries = DbQueries(db)
#
# rows = queries.production_join_query(
#     main_table="disposition dis",
#     joins=[
#         {"type": "LEFT", "table": "atl_disposition ad", "on": "dis.disposition = ad.disposition"},
#     ],
#     select_fields=["dis.DISPOSITION", "ad.productionline"],
#     where_conditions={
#         "dis.status": "ACTIVE",
#         "ad.productionline": ["A", "B"],
#         "dis.created_at": {"$gte": "2026-01-01"},
#     },
#     order_by="dis.created_at DESC",
#     limit=100,
# )


def 生产库通用联表查询(
        self,
        main_table: str,  # 主表（含别名）
        joins: list,  # 关联表列表
        select_fields: list = None,
        where_conditions: dict = None,
        order_by: str = None,
        limit: int = None
) -> list:
    """
    多表 JOIN 查询方法

    :param main_table: 主表名（含别名），如 "disposition dis"
    :param joins: 关联表配置列表
        示例:
        [
            {
                "type": "LEFT",              # JOIN 类型: INNER, LEFT, RIGHT, FULL
                "table": "atl_disposition ad",  # 表名（含别名）
                "on": "dis.disposition = ad.disposition"  # ON 条件（字符串）
            },
            {
                "type": "INNER",
                "table": "products p",
                "on": "orders.product_id = p.id"
            }
        ]
    :param select_fields: 要查询的字段，如 ["dis.DISPOSITION", "ad.productionline"]
    :param where_conditions: WHERE 条件字典
        - 等值: {"col": "value"}
        - IN: {"col": ["a", "b"]}
        - 比较: {"col": {"$gt": value}}
    :param order_by: 排序，如 "dis.created_at DESC"
    :param limit: 返回条数限制
    :return: 查询结果列表
    """
    if not main_table or not isinstance(main_table, str):
        print("错误：主表名不能为空")
        return []

    # --- 处理 SELECT ---
    if not select_fields or not isinstance(select_fields, list):
        select_clause = "*"
    else:
        cleaned_fields = []
        for field in select_fields:
            if not isinstance(field, str):
                print(f"警告：字段名 '{field}' 类型非法")
                return []
            cleaned_fields.append(field)
        select_clause = ", ".join(cleaned_fields)

    # --- 构造 JOIN 子句 ---
    join_parts = []
    for join_config in joins:
        if not isinstance(join_config, dict):
            print(f"警告：JOIN 配置格式错误: {join_config}")
            continue

        join_type = join_config.get("type", "INNER").upper()
        table = join_config.get("table", "")
        on = join_config.get("on", "")

        if not table:
            print(f"警告：缺少表名: {join_config}")
            continue

        if not on:
            print(f"警告：缺少 ON 条件: {join_config}")
            continue

        join_parts.append(f"{join_type} JOIN {table} ON {on}")

    join_sql = " ".join(join_parts) if join_parts else ""

    # --- 构造 WHERE ---
    where_sql, params = self._build_where_clause(where_conditions)

    # --- 构造 ORDER BY ---
    order_sql = f" ORDER BY {order_by}" if order_by else ""

    # --- 构造 LIMIT ---
    limit_sql = f" LIMIT {limit}" if limit else ""

    # --- 组合完整 SQL ---
    query_sql = f"SELECT {select_clause} FROM {main_table} {join_sql}{where_sql}{order_sql}{limit_sql}"

    try:
        result = db_mesp_client.execute_query(query_sql, params)
        return result if result is not None else []
    except Exception as e:
        print(f"联表查询失败: {str(e)}")
        return []


def _build_where_clause(self, where_conditions: dict = None) -> tuple:
    """
    内部方法：构造 WHERE 条件

    :param where_conditions: WHERE 条件字典
    :return: (where_sql字符串, params参数字典)
    """
    if not where_conditions:
        return "", {}

    params = {}
    where_parts = []

    for i, (field, value) in enumerate(where_conditions.items()):
        # 校验字段名
        if not isinstance(field, str) or not field.strip():
            print(f"警告：字段名 '{field}' 非法")
            continue

        if isinstance(value, list):
            # IN 条件
            if not value:
                continue  # 跳过空列表
            placeholders = []
            for j, v in enumerate(value):
                param_key = f"in_{i}_{j}"
                placeholders.append(f":{param_key}")
                params[param_key] = v
            where_parts.append(f"{field} IN ({', '.join(placeholders)})")

        elif isinstance(value, dict):
            # 比较操作符
            for op_key, op_value in value.items():
                placeholder = f"cond_{i}"
                op_map = {
                    "$gt": ">",
                    "$gte": ">=",
                    "$lt": "<",
                    "$lte": "<=",
                    "$ne": "!="
                }
                if op_key in op_map:
                    where_parts.append(f"{field} {op_map[op_key]} :{placeholder}")
                    params[placeholder] = op_value
                else:
                    print(f"警告：不支持的操作符 '{op_key}'，跳过")
                    continue

        else:
            # 默认等值匹配
            placeholder = f"eq_{i}"
            where_parts.append(f"{field} = :{placeholder}")
            params[placeholder] = value

    where_sql = " WHERE " + " AND ".join(where_parts) if where_parts else ""
    return where_sql, params
