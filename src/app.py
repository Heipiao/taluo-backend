from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote
import os
import logging

from extensions import limiter  # 导入公共的 limiter 实例

# 设置日志格式，包含时间、日志级别、文件名和行号
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = SQLAlchemy()

def create_app():
    # 加载 .env 文件
    load_dotenv()

    app = Flask(__name__)

    # 从环境变量中获取数据库连接信息
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = quote(os.getenv('DB_PASSWORD', ''))
    database = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT', 3306)




    # 检查环境变量是否正确加载
    if not all([host, user, password, database]):
        raise ValueError(
            "One or more required environment variables are missing: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME"
        )

    # 组装 SQLALCHEMY_DATABASE_URI
    db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    # 配置 SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 1,
        'pool_size': 10,
        'max_overflow': 5,
        'connect_args': {
            'connect_timeout': 10,  # 连接超时（秒）
            'read_timeout': 30,     # 读取超时（秒）
            'write_timeout': 30     # 写入超时（秒）
        }
    }

    try:
        limiter.init_app(app)
        logger.info("Limiter initialized successfully.")
    except Exception as e:
        logger.error(f"Limiter initialization failed: {e}", exc_info=True)
        raise e
    

    # 初始化数据库
    db.init_app(app)
    # 配置日志
    logging.info(f"Database URI: {db_uri}")

    # 注册蓝图
    with app.app_context():
        from routes.user_routes import bp as user_bp
        from routes.system_routes import bp as system_bp
        from routes.product_routes import bp as product_bp
 
        app.register_blueprint(user_bp, url_prefix='/taluo/user')  # 设置用户模块 URL 前缀
        app.register_blueprint(system_bp, url_prefix='/taluo/system')  # 设置系统模块 URL 前缀
        app.register_blueprint(product_bp, url_prefix='/taluo/translate')  # 设置系统模块 URL 前缀

        # 自动创建数据库表
        db.create_all()
        logging.info("Database tables created.")

    return app
