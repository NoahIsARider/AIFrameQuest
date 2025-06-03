import os
import json
import jwt
import datetime
from functools import wraps
from flask import jsonify, request
from utils_database.models import User, Admin, db

# 配置
JWT_SECRET_KEY = "your-jwt-secret-key"  # 应该与主应用中的密钥一致
JWT_EXPIRATION_DELTA = datetime.timedelta(hours=24)

def verify_admin(admin_id, email, password):
    """验证管理员凭据"""
    try:
        # 从数据库中查询管理员用户
        admin = Admin.query.filter_by(id=admin_id, email=email, password=password).first()
        if admin:
            return {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
                'role': admin.role
            }
        return None
    except Exception as e:
        print(f"验证管理员凭据失败: {str(e)}")
        return None

def generate_admin_token(admin_id, email):
    """生成JWT Token"""
    payload = {
        'admin_id': admin_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def token_required(f):
    """验证JWT Token的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_admin = {
                'admin_id': data['admin_id'],
                'email': data['email']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_admin, *args, **kwargs)
    
    return decorated
