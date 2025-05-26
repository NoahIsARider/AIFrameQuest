import json
import os
from flask import jsonify
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 用户数据文件路径
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'users.json')

def load_users():
    """加载用户数据"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"Loaded users from {USERS_FILE}: {data}")
                return data
        logger.debug(f"Users file not found at {USERS_FILE}")
        return {}
    except Exception as e:
        logger.error(f"Error loading users: {str(e)}")
        return {}

def save_users(data):
    """保存用户数据"""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.debug(f"Saved users to {USERS_FILE}")
    except Exception as e:
        logger.error(f"Error saving users: {str(e)}")

def register_user(username, email, password):
    """注册新用户"""
    users_data = load_users()
    
    # 检查用户名是否已存在
    if any(user_data['username'] == username for user_data in users_data.values()):
        return jsonify({"status": "error", "message": "用户名已存在"}), 400
    
    # 检查邮箱是否已存在
    if any(user_data['email'] == email for user_data in users_data.values()):
        return jsonify({"status": "error", "message": "邮箱已存在"}), 400
    
    # 生成新的用户ID
    if users_data:
        new_id = max(int(user_data['id']) for user_data in users_data.values()) + 1
    else:
        new_id = 1
    
    # 创建新的用户数据
    user_key = f"user{new_id}"
    user_data = {
        "id": new_id,
        "username": username,
        "email": email,
        "password": password,  # 注意：实际应用中应该对密码进行加密
        "role": "user"
    }
    
    # 添加新用户
    users_data[user_key] = user_data
    
    save_users(users_data)
    return jsonify({"status": "success", "message": "注册成功"}), 200

def login_user(email, password):
    """用户登录"""
    users_data = load_users()
    
    # 打印所有用户数据用于调试
    logger.debug(f"All users data: {users_data}")
    
    for user_id, user_data in users_data.items():
        if user_data['email'] == email:
            logger.debug(f"Found user with email {email}, password: {user_data['password']}")
            if user_data['password'] == password:
                logger.info(f"Login successful for user: {email}")
                # 生成token（格式：user-token-用户名）
                token = f"user-token-{user_data['username']}"
                return jsonify({
                    "status": "success",
                    "message": "登录成功",
                    "token": token
                }), 200
            else:
                logger.warning(f"Login failed - Password mismatch for email: {email}")
    
    logger.warning(f"Login failed - User not found with email: {email}")
    return jsonify({"status": "error", "message": "邮箱或密码错误"}), 401