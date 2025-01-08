import pymysql
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 从环境变量中获取数据库连接信息
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
port = int(os.getenv('DB_PORT', 3306))  # 默认端口为 3306

# 测试数据库连接
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    print("Connection successful")
except pymysql.MySQLError as e:
    print(f"Error connecting to database: {e}")


import time
from sqlalchemy import create_engine, text

# 假设 user, password, host, port, database 这些变量已正确定义
db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
print("Database URI:", db_uri)

url = db_uri

# 创建引擎，指定 pool_recycle=1
engine = create_engine(url, pool_recycle=1)

query = 'SELECT now();'

with engine.connect() as conn:
    result = conn.execute(text("SELECT NOW()"))
    rows = result.fetchall()
    print(rows)
