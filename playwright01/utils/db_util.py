import oracledb
import cx_Oracle
from sqlalchemy import create_engine, text, NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus  # 防止密码含特殊字符
from playwright01.utils.log_util import *

# 数据库连接信息
db_username = ""
db_password = ""
db_service_name = ""
db_host = ""
db_port = ""





# 尝试导入 oracledb（新驱动）
try:
    import oracledb

    ORACLEDB_AVAILABLE = True
except ImportError:
    ORACLEDB_AVAILABLE = False

# 尝试导入 cx_Oracle（旧驱动）
try:
    import cx_Oracle

    CX_ORACLE_AVAILABLE = True
except ImportError:
    CX_ORACLE_AVAILABLE = False


class OracleDB:
    def __init__(
            self,
            username,
            password,
            host,
            port,
            service_name=None,
            sid=None,
            mode="auto",  # "thin", "thick", "cx_oracle", "auto"
            lib_dir=None,  # 仅 thick / cx_oracle 需要
    ):
        """
        统一 Oracle 数据库连接工具类，支持 11.2 ~ 19c+

        :param mode:
            - "thin": 使用 oracledb Thin 模式（仅 12.1+）
            - "thick": 使用 oracledb Thick 模式（需 Instant Client，支持 11.2+）
            - "cx_oracle": 使用旧版 cx_Oracle（需 Instant Client）
            - "auto": 自动选择（优先 thin → thick → cx_oracle）
        """
        if not all([username, password, host, port]):
            raise ValueError("数据库连接参数不能为空")
        if not (service_name or sid):
            raise ValueError("必须提供 service_name 或 sid")

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name
        self.sid = sid
        self.lib_dir = lib_dir
        self.mode = mode.lower()

        # 构造 DSN 字符串
        if service_name:
            self.dsn_str = f"{host}:{port}/{service_name}"
        else:
            self.dsn_str = f"{host}:{port}:{sid}"

        # 安全编码密码
        safe_password = quote_plus(password)

        # 自动选择驱动
        self.engine = None
        self._init_engine(safe_password)

        # 创建 Session 工厂
        self.Session = sessionmaker(bind=self.engine)

    def _init_engine(self, safe_password):
        """初始化 SQLAlchemy 引擎"""
        url_base = f"{self.username}:{safe_password}@{self.dsn_str}"

        if self.mode == "thin":
            if not ORACLEDB_AVAILABLE:
                raise RuntimeError("oracledb 未安装，请运行: pip install oracledb")
            # Thin 模式：无需 init_client
            database_url = f"oracle+oracledb://{url_base}"
            self.engine = create_engine(
                database_url,
                pool_size=1,
                max_overflow=0,
                echo=False
            )

        elif self.mode == "thick":
            if not ORACLEDB_AVAILABLE:
                raise RuntimeError("oracledb 未安装，请运行: pip install oracledb")
            # 初始化 Thick 模式
            try:
                if self.lib_dir:
                    oracledb.init_oracle_client(lib_dir=self.lib_dir)
                else:
                    oracledb.init_oracle_client()  # 从 PATH 加载
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Oracle Client in thick mode: {e}")
            database_url = f"oracle+oracledb://{url_base}"
            self.engine = create_engine(
                database_url,
                pool_size=1,
                max_overflow=0,
                echo=False
            )

        elif self.mode == "cx_oracle":
            if not CX_ORACLE_AVAILABLE:
                raise RuntimeError("cx_Oracle 未安装，请运行: pip install cx_Oracle")
            try:
                if self.lib_dir:
                    cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)
                else:
                    cx_Oracle.init_oracle_client()
            except Exception as e:
                raise RuntimeError(f"Failed to initialize cx_Oracle client: {e}")
            database_url = f"oracle+cx_oracle://{url_base}"
            self.engine = create_engine(
                database_url,
                pool_size=1,
                max_overflow=0,
                echo=False
            )

        elif self.mode == "auto":
            # 尝试顺序：thin → thick → cx_oracle
            errors = []

            # 1. 尝试 Thin 模式（最快，无依赖）
            if ORACLEDB_AVAILABLE:
                try:
                    database_url = f"oracle+oracledb://{url_base}"
                    engine = create_engine(database_url, pool_size=1, max_overflow=0, echo=False)
                    # 测试连接
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1 FROM DUAL"))
                    self.engine = engine
                    print("✅ 使用 oracledb Thin 模式")
                    return
                except Exception as e:
                    errors.append(f"Thin mode failed: {e}")

            # 2. 尝试 Thick 模式
            if ORACLEDB_AVAILABLE:
                try:
                    if self.lib_dir:
                        oracledb.init_oracle_client(lib_dir=self.lib_dir)
                    else:
                        oracledb.init_oracle_client()
                    database_url = f"oracle+oracledb://{url_base}"
                    engine = create_engine(database_url, pool_size=1, max_overflow=0, echo=False)
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1 FROM DUAL"))
                    self.engine = engine
                    print("✅ 使用 oracledb Thick 模式")
                    return
                except Exception as e:
                    errors.append(f"Thick mode failed: {e}")

            # 3. 尝试 cx_Oracle
            if CX_ORACLE_AVAILABLE:
                try:
                    if self.lib_dir:
                        cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)
                    else:
                        cx_Oracle.init_oracle_client()
                    database_url = f"oracle+cx_oracle://{url_base}"
                    engine = create_engine(database_url, pool_size=1, max_overflow=0, echo=False)
                    with engine.connect() as conn:
                        conn.execute(text("SELECT 1 FROM DUAL"))
                    self.engine = engine
                    print("✅ 使用 cx_Oracle 模式")
                    return
                except Exception as e:
                    errors.append(f"cx_Oracle mode failed: {e}")

            # 全部失败
            raise RuntimeError("所有 Oracle 驱动模式均失败:\n" + "\n".join(errors))

        else:
            raise ValueError("mode 必须是 'thin', 'thick', 'cx_oracle' 或 'auto'")

    def execute_query(self, query, params=None):
        """执行查询"""
        try:
            with self.engine.connect() as connection:
                if isinstance(query, str):
                    query_obj = text(query)
                else:
                    query_obj = query

                # 生成调试 SQL
                debug_sql = _render_sql_for_logging(query_obj, params)
                log_sql.info(f"[QUERY] {debug_sql}")

                result = connection.execute(query_obj, params or {})
                return result.fetchall()

        except SQLAlchemyError as e:
            error_msg = f"查询失败: {e}"
            print(error_msg)
            log_sql.error(error_msg)
            return None

    def execute_update(self, query, params=None):
        """执行更新/插入/删除"""
        try:
            with self.engine.connect() as connection:
                if isinstance(query, str):
                    query_obj = text(query)
                else:
                    query_obj = query

                # 生成调试 SQL
                debug_sql = _render_sql_for_logging(query_obj, params)
                log_sql.info(f"[UPDATE] {debug_sql}")

                result = connection.execute(query_obj, params or {})
                connection.commit()
                return result.rowcount

        except SQLAlchemyError as e:
            error_msg = f"执行失败: {e}"
            print(error_msg)
            log_sql.error(error_msg)
            return None

    def get_session(self):
        """获取 ORM Session"""
        return self.Session()

    def close(self):
        """关闭连接池"""
        if self.engine:
            self.engine.dispose()

def _render_sql_for_logging(query_obj, params):
    """
    安全地将 TextClause + params 渲染为可读的 SQL 字符串（仅用于日志！）
    :param query_obj: sqlalchemy.text() 对象
    :param params: dict 参数
    :return: str 可打印的 SQL
    """
    sql_str = str(query_obj)
    if not params or not isinstance(params, dict):
        return sql_str

    # 按参数名长度降序排序，避免短名覆盖长名（如 :id 覆盖 :id2）
    sorted_params = sorted(params.items(), key=lambda x: -len(x[0]))
    rendered = sql_str

    for key, val in sorted_params:
        placeholder = f":{key}"
        if placeholder not in rendered:
            continue  # 跳过未使用的参数

        # 安全转义值
        if val is None:
            replacement = "NULL"
        elif isinstance(val, str):
            # 转义单引号（Oracle 标准）
            safe_val = val.replace("'", "''")
            replacement = f"'{safe_val}'"
        elif isinstance(val, (int, float)):
            replacement = str(val)
        else:
            # 其他类型转为字符串并加引号（保守做法）
            safe_val = str(val).replace("'", "''")
            replacement = f"'{safe_val}'"

        # 只替换第一个匹配项（虽然通常只有一个）
        rendered = rendered.replace(placeholder, replacement, 1)

    return rendered





db_client = OracleDB(db_username, db_password, db_host, db_port, db_service_name)

db_client = OracleDB(db_username, db_password, db_host, db_port, db_service_name,
                           lib_dir=r'C:\ORACLE\instantclient-basic-windows.x64-11.2.0.4.0\instantclient_11_2')

if __name__ == "__main__":

    db_username = ""
    db_password = ""
    db_host = ""
    db_port = ""
    db_service_name = ""
    # 连接参数
    dsn_tns = cx_Oracle.makedsn('', '', service_name='')  # 替换为你的主机名、端口和服务名
    username = ''  # 替换为你的用户名
    password = ''  # 替换为你的密码

    select_result = db_mesp_client.execute_query(
        "SELECT * FROM ")  # 替换为你的SQL查询
    if select_result:
        for row in select_result:
            print(row)
"""
如何使用工具类
1.创建工具类实例
from db_util import DatabaseUtil

# 初始化工具类
db = DatabaseUtil(
        username="your_username"
        password="your_password"
        host="localhost"
        port="1521"
        service_name="orcl"
)

2.执行查询操作

# 执行查询语句
query = " SELECT * FROM inventory2  WHERE CONTAINER = 'N31324091900227-05' "
params = {"limit" : 5}

result = db.execute_query(query, params)
if result:
    for row in result:
        print(row)

3.执行更新操作
#插入数据

# insert_query = '''INSERT INTO employees (employee_id, first_name, last_name)VALUES(:employee_id, :first_name, :last_name)'''

params = {
    "employee_id": 101,
    "first_name": "John",
    "last_name": "Doe"
}
rows_affected = db.execute_update(insert_query, params)
print(f"插入影响操作了{rows_affected} 行")


4.使用会话进行事务操作

session = db.get_session()

    try:
        # 插入操作
        session.execute(
            text("INSERT INTO employees (employee_id, first_name, last_name) values (:id, :fname, :lname)"),
            {"id": 102, "fname": "Jane", "lname": "Smith"}
        )
        # 更新操作
        session.execute(
            text("UPDATE  employees SET  last_name= :lname where employee_id = :id"),
            {"lname": "Johnson", "id": 102}
        )
        # 提交事务
        session.commint()
        print("事务操作成功!")
    except Exception as e:
        session.rollback()
        print(f"事务操作失败，已会滚: {e}")
    finally:
        session.close()

5.关闭数据库连接
在程序结束时，记得关闭连接池
db.close()

"""