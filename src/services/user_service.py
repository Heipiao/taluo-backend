from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db

def register_user(username, email, password, phone_number=None, apple_id=None, tiktok_id=None, wechat_id=None):
    """
    注册新用户
    """
    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        phone_number=phone_number,
        apple_id=apple_id,
        tiktok_id=tiktok_id,
        wechat_id=wechat_id,
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully", "user_id": new_user.id}, 201

def login_user(email, password):
    """
    用户登录
    """
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "Invalid email or password"}, 401

    return {"message": f"Welcome {user.username}!", "user_id": user.id}, 200
