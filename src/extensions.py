from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# 创建 Limiter 实例
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv('LIMITER_STORAGE_URI', 'memory://')  # 使用内存存储或其他存储方案
)

# 这里可以添加其他共享的扩展，如数据库实例等
