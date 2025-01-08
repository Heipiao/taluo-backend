from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote

import os

db = SQLAlchemy()

def create_app():
    load_dotenv()  # 加载 .env 文件

    app = Flask(__name__)
   # 从环境变量中获取数据库连接信息
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = quote(os.getenv('DB_PASSWORD'))
    database = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT', 3306)

    # 检查环境变量是否正确加载
    if not all([host, user, password, database]):
        raise ValueError("One or more required environment variables are missing: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME")

    # 组装 SQLALCHEMY_DATABASE_URI
    db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    print("Database URI:", db_uri)
    
        # 配置 SQLAlchemy 连接池和重试机制
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True, 
        'pool_recycle': 1,
        'pool_size': 10,
        'max_overflow': 5,
        'connect_args': {
            'connect_timeout': 10,   # 连接超时（秒）
            'read_timeout': 30,      # 服务端在读取数据时的超时（秒）
            'write_timeout': 30      # 服务端在写入数据时的超时（秒）
        }
    }



    db.init_app(app)

    with app.app_context():
        from routes.user_routes import bp as user_bp
        app.register_blueprint(user_bp)
        db.create_all()

    return app
