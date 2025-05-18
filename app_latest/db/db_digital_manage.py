"""
数字人管理数据库操作模块
"""
# 从app.db.py导入DatabaseManager类
from db.app_db import DatabaseManager

# 数据库连接依赖
def get_db():
    """
    获取数据库连接的依赖函数，用于FastAPI依赖注入
    """
    db = DatabaseManager()
    try:
        db.connect()
        # 确保表存在
        if not db.check_table_exists():
            db.create_table()
        else:
            # 如果表已存在，检查并添加可能缺失的列
            db.add_missing_columns()
        yield db
    finally:
        db.disconnect() 