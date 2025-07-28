import cx_Oracle
from sqlalchemy import create_engine, text, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from playwright01.utils.logger import logger


class DatabaseUtil:
    """基于 oracledb 驱动的数据库工具类"""

    def __init__(self, username, password, host, port, service_name, **kwargs):
        """
        初始化数据库连接
        """
        # 默认连接参数
        default_params = {
            'pool_pre_ping': True,
            'pool_recycle': 1800,
            'pool_size': 5,
            'max_overflow': 2,
            'pool_timeout': 30
        }
        default_params.update(kwargs)

        try:
            self.engine = create_engine(
                f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}",
                **default_params
            )
            self.Session = sessionmaker(bind=self.engine)
            logger.info("DatabaseUtil - 数据库连接成功")
        except SQLAlchemyError as e:
            logger.error(f"DatabaseUtil - 数据库连接失败: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """连接上下文管理器"""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except SQLAlchemyError as e:
            logger.error(f"DatabaseUtil - 数据库连接错误: {e}")
            raise
        finally:
            if connection:
                connection.close()

    def execute_query(self, query, params=None):
        """执行查询语句"""
        try:
            with self.get_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(f"DatabaseUtil - 查询失败: {e}")
            return None

    def execute_update(self, query, params=None):
        """执行更新语句"""
        try:
            with self.get_connection() as connection:
                trans = connection.begin()
                try:
                    result = connection.execute(text(query), params or {})
                    trans.commit()
                    return result.rowcount
                except:
                    trans.rollback()
                    raise
        except SQLAlchemyError as e:
            logger.error(f"DatabaseUtil - 执行失败: {e}")
            return None

    def get_session(self):
        """获取会话"""
        return self.Session()

    def close(self):
        """关闭连接池"""
        if self.engine:
            self.engine.dispose()
            logger.info("DatabaseUtil - 数据库连接池已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class CxOracleDB:
    """基于 cx_Oracle 驱动的数据库工具类"""

    def __init__(self, username, password, host, port, service_name, lib_dir=None):
        """
        初始化数据库连接
        """
        # 初始化 Oracle 客户端
        if lib_dir:
            try:
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
                logger.info(f"CxOracleDB - 成功初始化 Oracle 客户端: {lib_dir}")
            except Exception as e:
                logger.error(f"CxOracleDB - 初始化 Oracle 客户端失败: {e}")
                raise

        # 创建 DSN 和引擎
        try:
            dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
            self.engine = create_engine(f"oracle+cx_oracle://{username}:{password}@{dsn_tns}")
            logger.info("CxOracleDB - 数据库连接成功")
        except Exception as e:
            logger.error(f"CxOracleDB - 数据库连接失败: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """连接上下文管理器"""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except SQLAlchemyError as e:
            logger.error(f"CxOracleDB - 数据库连接错误: {e}")
            raise
        finally:
            if connection:
                connection.close()

    def execute_query(self, query, params=None):
        """执行查询语句"""
        try:
            with self.get_connection() as connection:
                result = connection.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(f"CxOracleDB - 查询失败: {e}")
            return None

    def execute_update(self, query, params=None):
        """执行更新语句"""
        try:
            with self.get_connection() as connection:
                trans = connection.begin()
                try:
                    result = connection.execute(text(query), params or {})
                    trans.commit()
                    return result.rowcount
                except:
                    trans.rollback()
                    raise
        except SQLAlchemyError as e:
            logger.error(f"CxOracleDB - 执行失败: {e}")
            return None

    def close(self):
        """关闭连接"""
        if self.engine:
            self.engine.dispose()
            logger.info("CxOracleDB - 数据库连接已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 使用示例
def example_usage():
    """使用示例"""

    # 使用 DatabaseUtil (推荐)
    try:
        with DatabaseUtil("user", "pass", "host", "1521", "service") as db:
            # 查询操作
            results = db.execute_query("SELECT * FROM users WHERE id = :user_id",
                                       {"user_id": 123})

            # 更新操作
            affected_rows = db.execute_update(
                "UPDATE users SET name = :name WHERE id = :id",
                {"name": "new_name", "id": 123}
            )

            print(f"查询结果: {results}")
            print(f"影响行数: {affected_rows}")
    except Exception as e:
        logger.error(f"DatabaseUtil 使用出错: {e}")

    # 使用 CxOracleDB (传统方式)
    try:
        with CxOracleDB("user", "pass", "host", "1521", "service",
                        lib_dir="/path/to/oracle/client") as db:
            results = db.execute_query("SELECT * FROM users WHERE id = :user_id",
                                       {"user_id": 123})
            print(f"查询结果: {results}")
    except Exception as e:
        logger.error(f"CxOracleDB 使用出错: {e}")
