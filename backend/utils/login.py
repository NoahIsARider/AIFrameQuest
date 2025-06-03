import json
import os
from flask import jsonify
import logging
from utils_database.models import User, db
# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 用户数据文件路径
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'users.json')

def load_users():
    """从数据库中读取所有用户，返回兼容原始结构的字典"""
    try:
        users = User.query.all()
        result = {}
        
        for user in users:
            entry_key = f"user{user.id}"
            result[entry_key] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "role": user.role
            }
       
        logger.debug(f"成功从数据库加载 {len(users)} 个用户")
        return result
    
    except Exception as e:
        logger.error(f"加载用户数据失败: {str(e)}")
        return {}
    
def save_users(data):
    """将用户数据保存到数据库中"""
    try:
        # 删除旧用户数据
        User.query.delete()
        
        # 插入新用户数据
        for key, user_data in data.items():
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data.get('role', 'user')
            )
            db.session.add(user)
        
        db.session.commit()
        logger.debug("用户数据已成功写入数据库")
    except Exception as e:
        db.session.rollback()
        logger.error(f"写入用户数据失败: {str(e)}")
        raise e



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