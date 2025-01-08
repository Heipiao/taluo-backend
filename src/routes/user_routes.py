from flask import Blueprint, request, jsonify
from services.user_service import register_user, login_user

bp = Blueprint('user', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    apple_id = data.get('apple_id')
    tiktok_id = data.get('tiktok_id')
    wechat_id = data.get('wechat_id')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    result, status_code = register_user(
        username, email, password, phone_number, apple_id, tiktok_id, wechat_id
    )
    return jsonify(result), status_code

@bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result, status_code = login_user(email, password)
    return jsonify(result), status_code
