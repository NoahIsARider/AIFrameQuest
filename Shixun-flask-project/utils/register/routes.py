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
    """图片上传接口"""
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': '未检测到文件'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '未选择文件'}), 400

    # 获取文件扩展名
    ext = os.path.splitext(file.filename)[1]
    # 用时间戳重命名，防止中文丢失
    filename = f"{int(time.time() * 1000)}{ext}"
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 构造图片访问URL（假设你的 Flask 静态目录为 static）
    url = f'/static/uploads/{filename}'

    return jsonify({'status': 'success', 'url': url})
    # -------------------------------------------------