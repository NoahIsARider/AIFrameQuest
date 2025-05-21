from flask import Blueprint, request, jsonify
from .auth import register_user, login_user, load_users
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils.faiss_search.faiss_search import process_search_request, initialize_index, IMAGE_FOLDER, UPLOAD_FOLDER
import os
import logging
import time

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """注册接口"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"status": "error", "message": "用户名和密码不能为空"}), 400
        
    return register_user(username, password)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """登录接口"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    logger.debug(f"Login attempt - Username: {username}, Password: {password}")
    
    # 打印当前所有用户
    users_data = load_users()
    logger.debug(f"Current users: {users_data}")
    
    if not username or not password:
        logger.warning("Login failed - Empty username or password")
        return jsonify({"status": "error", "message": "用户名和密码不能为空"}), 400
    
    result = login_user(username, password)
    logger.debug(f"Login result: {result}")
    return result 

@auth_bp.route('/api/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        # Process the search request using the faiss_search module
        result = process_search_request(file)

        # Check if there was an error
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], dict) and 'error' in result[0]:
            return jsonify(result[0]), result[1]

        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'后端异常: {str(e)}'}), 500