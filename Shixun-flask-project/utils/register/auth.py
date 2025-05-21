import json
import os
from flask import jsonify

# 用户数据文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(BASE_DIR, 'data', 'users.json')

def load_users():
    """加载用户数据"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded users from {USERS_FILE}: {data}")  # 调试信息
                return data
        print(f"Users file not found at {USERS_FILE}")  # 调试信息
        return {"users": []}
    except Exception as e:
        print(f"Error loading users: {str(e)}")  # 调试信息
        return {"users": []}

def save_users(data):
    """保存用户数据"""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved users to {USERS_FILE}")  # 调试信息
    except Exception as e:
        print(f"Error saving users: {str(e)}")  # 调试信息

def register_user(username, password):
    """注册新用户"""
    users_data = load_users()
    
    # 检查用户名是否已存在
    if any(user['username'] == username for user in users_data['users']):
        return jsonify({"status": "error", "message": "用户名已存在"}), 400
    
    # 添加新用户
    users_data['users'].append({
        "username": username,
        "password": password  # 注意：实际应用中应该对密码进行加密
    })
    
    save_users(users_data)
    return jsonify({"status": "success", "message": "注册成功"}), 200

def login_user(username, password):
    """用户登录"""
    users_data = load_users()
    print(f"Attempting login for user {username}")  # 调试信息
    print(f"Available users: {users_data}")  # 调试信息
    
    # 查找用户
    user = next((user for user in users_data['users'] 
                if user['username'] == username and user['password'] == password), None)
    
    if user:
        print(f"Login successful for user {username}")  # 调试信息
        return jsonify({
            "status": "success",
            "message": "登录成功",
            "token": f"user-token-{username}"
        })
    print(f"Login failed for user {username}")  # 调试信息
    return jsonify({"status": "error", "message": "用户名或密码错误"}), 401 