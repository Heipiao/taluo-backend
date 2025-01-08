from app import db
from datetime import datetime, timezone

def current_utc_time():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = 'taluo_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    apple_id = db.Column(db.String(128), unique=True, nullable=True)
    tiktok_id = db.Column(db.String(128), unique=True, nullable=True)
    wechat_id = db.Column(db.String(128), unique=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=current_utc_time)
    updated_at = db.Column(db.DateTime, default=current_utc_time, onupdate=current_utc_time)

    def __repr__(self):
        return f"<User {self.username}>"
