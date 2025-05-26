import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from utils.login import register_user, login_user
from utils.list import read_posts, write_posts, get_post_detail
from utils.faiss_search import process_search_request, initialize_index
import os
import json

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 配置Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 确保上传文件夹存在
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 图片文件夹路径
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# 初始化FAISS索引
initialize_index()


@app.route('/api/auth/register', methods=['POST'])
def register():
    """注册接口"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        logger.debug(f"Register attempt - Username: {username}, Email: {email}")
        
        if not username or not email or not password:
            return jsonify({"status": "error", "message": "用户名、邮箱和密码不能为空"}), 400
            
        result = register_user(username, email, password)
        logger.debug(f"Register result: {result}")
        return result
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """登录接口"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        logger.debug(f"Login attempt - Email: {email}")
        
        if not email or not password:
            return jsonify({"status": "error", "message": "邮箱和密码不能为空"}), 400
        
        result = login_user(email, password)
        logger.debug(f"Login result: {result}")
        
        if result[1] == 200:  # 如果登录成功
            return jsonify({
                "status": "success",
                "message": "登录成功",
                "token": result[0].json['token']
            }), 200
        return result
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
# 获取所有帖子,放到/api/posts路径下显示
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        logger.debug("尝试读取帖子数据")
        posts = read_posts()
        logger.debug(f"成功读取帖子数据: {posts}")
        return jsonify(posts)
    except Exception as e:
        logger.error(f"获取帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 获取单个帖子
@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        # 使用新的get_post_detail函数获取详细信息
        post_detail = get_post_detail(post_id)
        if not post_detail:
            return jsonify({"error": "帖子不存在"}), 404
        return jsonify(post_detail)
    except Exception as e:
        logger.error(f"获取单个帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 添加新帖子
@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        posts = read_posts()
        new_post = request.json

        # 自动生成 ID
        max_id = max((p['id'] for p in posts), default=0)
        new_post['id'] = max_id+1
        
        # 设置默认值
        if 'date' not in new_post:
            new_post['date'] = ""
        if 'views' not in new_post:
            new_post['views'] = 0
        if 'comments' not in new_post:
            new_post['comments'] = 0
        if 'favorites' not in new_post:
            new_post['favorites'] = 0

        # 添加到列表并保存
        posts.append(new_post)
        write_posts(posts)
        
        # 返回新创建的帖子详情
        post_detail = get_post_detail(new_post['id'])
        return jsonify(post_detail), 201
    except Exception as e:
        logger.error(f"创建帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 更新帖子
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        posts = read_posts()
        data = request.json

        found = False
        for i, post in enumerate(posts):
            if post['id'] == post_id:
                posts[i] = {**post, **data}
                found = True
                break

        if not found:
            return jsonify({"error": "帖子不存在"}), 404

        write_posts(posts)
        
        # 返回更新后的帖子详情
        post_detail = get_post_detail(post_id)
        return jsonify({"message": "更新成功", "post": post_detail})
    except Exception as e:
        logger.error(f"更新帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 删除帖子
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        # 先检查帖子是否存在
        post_detail = get_post_detail(post_id)
        if not post_detail:
            return jsonify({"error": "帖子不存在"}), 404
            
        # 获取所有帖子并过滤掉要删除的帖子
        posts = read_posts()
        filtered_posts = [p for p in posts if p['id'] != post_id]
        
        # 如果过滤前后数量相同，说明没有找到要删除的帖子
        if len(filtered_posts) == len(posts):
            return jsonify({"error": "帖子不存在"}), 404
            
        # 写入更新后的帖子列表
        write_posts(filtered_posts)
        return jsonify({"message": "删除成功"})
    except Exception as e:
        logger.error(f"删除帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 图片上传和搜索接口
@app.route('/api/image-search', methods=['POST'])
def image_search():
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"error": "没有上传文件"}), 400
            
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({"error": "文件名为空"}), 400
            
        # 处理图片搜索请求
        results = process_search_request(file)
        
        # 返回搜索结果
        return jsonify(results)
    except Exception as e:
        logger.error(f"图片搜索时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 提供图片文件访问
@app.route('/images/<path:filename>')
def serve_image(filename):
    try:
        # 安全地处理路径，防止目录遍历攻击
        safe_filename = os.path.basename(filename)
        if safe_filename != filename:
            logger.warning(f"可能的安全问题: 尝试访问非常规路径 {filename}")
            return jsonify({"error": "Invalid filename"}), 400
            
        # 构建完整路径
        filepath = os.path.join(IMAGE_FOLDER, safe_filename)
        
        logger.debug(f"尝试访问图片: {safe_filename}")
        logger.debug(f"图片目录: {os.path.abspath(IMAGE_FOLDER)}")
        logger.debug(f"完整路径: {filepath}")
        
        # 检查文件是否存在
        if not os.path.exists(filepath):
            logger.error(f"图片文件不存在: {filepath}")
            # 列出目录内容用于调试
            try:
                files = os.listdir(IMAGE_FOLDER)
                logger.debug(f"目录内容: {files}")
            except Exception as e:
                logger.error(f"无法列出目录内容: {str(e)}")
            return jsonify({"error": "Image not found"}), 404
            
        # 发送文件
        logger.debug(f"发送图片: {filepath}")
        return send_from_directory(
            IMAGE_FOLDER, 
            safe_filename,
            mimetype='image/jpeg'  # 显式设置MIME类型
        )
    except Exception as e:
        logger.error(f"提供图片访问时出错: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
        return jsonify({"error": str(e)}), 500

# 提供上传图片文件访问
@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        logger.error(f"提供上传图片访问时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 添加评论和评分
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    try:
        # 导入DATA_FILE路径
        from utils.list import DATA_FILE
        
        data = request.json
        name = data.get('name', '')
        text = data.get('text', '')
        rating = data.get('rating', 0)
        date = data.get('date', '')
        
        if not name or not text:
            return jsonify({"status": "error", "message": "评论者姓名和评论内容不能为空"}), 400
            
        # 获取当前词条数据
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            entries_dict = json.load(f)
            
        entry_key = f"entry{post_id}"
        if entry_key not in entries_dict:
            return jsonify({"status": "error", "message": "词条不存在"}), 404
        
        # 检查用户是否已经评论过
        comment_found = False
        for i, comment in enumerate(entries_dict[entry_key]['comments']):
            if comment['name'] == name:
                # 用户已评论过，更新评论
                entries_dict[entry_key]['comments'][i] = {
                    'name': name,
                    'text': text,
                    'rating': rating,
                    'date': date
                }
                comment_found = True
                message = "评论更新成功"
                break
        
        # 如果用户没有评论过，添加新评论
        if not comment_found:
            new_comment = {
                'name': name,
                'text': text,
                'rating': rating,
                'date': date
            }
            entries_dict[entry_key]['comments'].append(new_comment)
            message = "评论添加成功"
        
        # 保存更新后的数据
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(entries_dict, f, ensure_ascii=False, indent=2)
            
        # 返回更新后的词条详情
        post_detail = get_post_detail(post_id)
        return jsonify({"status": "success", "message": message, "post": post_detail})
    except Exception as e:
        logger.error(f"添加评论时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取词条相关图片
@app.route('/api/posts/<int:post_id>/images', methods=['GET'])
def get_post_images(post_id):
    try:
        # 导入图片数据文件路径
        IMAGES_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'images.json')
        
        # 读取图片信息文件
        with open(IMAGES_JSON_PATH, 'r', encoding='utf-8') as f:
            images_data = json.load(f)
        
        entry_key = f"entry{post_id}"
        
        # 查找与该词条相关的所有图片
        related_images = []
        for picture_key, picture_data in images_data.items():
            if picture_data.get('entry') == entry_key:
                # 构建完整的URL，包含域名和端口
                image_url = f"http://127.0.0.1:5000/images/{picture_data['file_name']}"
                
                image_info = {
                    'id': picture_data['id'],
                    'file_name': picture_data['file_name'],
                    'url': image_url
                }
                related_images.append(image_info)
        
        logger.debug(f"返回词条{post_id}的图片数据: {related_images}")
        return jsonify(related_images)
    except Exception as e:
        logger.error(f"获取词条图片时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)