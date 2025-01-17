from flask import Flask, jsonify, Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin

import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化限流器
limiter = Limiter(
    key_func=get_remote_address,  # 获取客户端 IP
    storage_uri="memory://",    # 使用内存作为存储后端
)
limiter.init_app(app)

# 创建蓝图
bp = Blueprint('test', __name__)

# 测试路由，限流为每天 1 次
@bp.route('/test', methods=['GET'])
@cross_origin()
@limiter.limit("1 per day")
def test_limit():
    client_ip = get_remote_address()
    logger.info(f"Test route accessed by IP: {client_ip}")
    return jsonify({"message": "Request successful"})

# 全局错误处理
@bp.app_errorhandler(429)
def ratelimit_exceeded(e):
    client_ip = get_remote_address()
    logger.warning(f"Rate limit exceeded for IP: {client_ip}")
    return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

# 注册蓝图
app.register_blueprint(bp, url_prefix='/api')

if __name__ == "__main__":
    # 启动服务
    app.run(host="0.0.0.0", port=5000, debug=True)
