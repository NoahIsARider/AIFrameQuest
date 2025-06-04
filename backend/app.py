import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from functools import wraps
from utils.login import register_user, login_user
from utils.list import read_posts, write_posts, get_post_detail
from utils.faiss_search import process_search_request, initialize_index
from utils.text_to_image_search import process_text_search_request, initialize_text_to_image_index
from utils_database.models import db, Image, Post, Comment
import os
import json
import os
import jwt
import datetime
from functools import wraps
from werkzeug.utils import secure_filename

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 配置Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持
#配置数据库
app.config.from_pyfile('utils_database/config.py')
db.init_app(app) 

# 配置文件上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 未审核图片文件夹路径
UNCENSORED_IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images_uncensored')
os.makedirs(UNCENSORED_IMAGE_FOLDER, exist_ok=True)

# 未审核图片信息文件路径
UNCENSORED_INFO_FILE = os.path.join(UNCENSORED_IMAGE_FOLDER, 'info.json')
# JWT配置
JWT_SECRET_KEY = 'your-secret-key'  # 在生产环境中应该使用环境变量
JWT_EXPIRATION_DELTA = datetime.timedelta(days=7)

# 管理员API密钥
ADMIN_API_KEY = 'admin-secret-key'  # 在生产环境中应该使用环境变量

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 辅助函数
def load_json_data(filename):
    """从JSON文件加载数据"""
    try:
        with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载{filename}数据失败: {str(e)}")
        return {}

def load_admins():
    """从JSON文件加载管理员数据"""
    return load_json_data('admins')

def generate_admin_token(admin_id, email):
    """生成JWT Token"""
    payload = {
        'admin_id': admin_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

# 装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查请求头中的API密钥
        api_key = request.headers.get('X-Admin-Key')
        if api_key != ADMIN_API_KEY:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] if 'Bearer' in request.headers['Authorization'] else None
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_admin = data['email']
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
            
        return f(current_admin, *args, **kwargs)
    return decorated

# 路由
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login_page():
    return render_template('login.html')

# 用户认证API
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

# 帖子相关API
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

@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        from utils_database.models import Post
        
        new_post_data = request.json
        
        # 准备帖子数据
        title = new_post_data.get('title', '')
        content = new_post_data.get('content', '')
        cover = new_post_data.get('cover', '')
        post_type = new_post_data.get('category', '动漫')
        
        # 创建描述JSON
        description = [content] if content else []
        
        # 创建新帖子对象
        new_post = Post(
            title=title,
            description=json.dumps(description, ensure_ascii=False),
            cover=cover,
            type=post_type
        )
        
        # 添加到数据库并提交
        db.session.add(new_post)
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "帖子创建成功",
            "post_id": new_post.id
        }), 201
    except Exception as e:
        logger.error(f"创建帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        from utils_database.models import Post
        
        # 获取帖子数据
        post_data = request.json
        
        # 查找帖子
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "帖子不存在"}), 404
        
        # 更新帖子数据
        if 'title' in post_data:
            post.title = post_data['title']
        
        if 'content' in post_data:
            # 更新描述JSON
            description = [post_data['content']] if post_data['content'] else []
            post.description = json.dumps(description, ensure_ascii=False)
        
        if 'cover' in post_data:
            post.cover = post_data['cover']
        
        if 'category' in post_data:
            post.type = post_data['category']
        
        # 提交更改
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "帖子更新成功"
        }), 200
    except Exception as e:
        logger.error(f"更新帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        from utils_database.models import Post
        
        # 查找帖子
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "帖子不存在"}), 404
        
        # 删除帖子
        db.session.delete(post)
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "帖子删除成功"
        }), 200
    except Exception as e:
        logger.error(f"删除帖子时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 评论相关API
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    try:
        from utils_database.models import Comment, Post
        
        # 获取评论数据
        comment_data = request.json
        
        # 查找帖子
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"error": "帖子不存在"}), 404
        
        # 创建新评论
        new_comment = Comment(
            post_id=post_id,
            name=comment_data.get('name', '匿名用户'),
            text=comment_data.get('text', ''),
            rating=comment_data.get('rating'),
            date=datetime.datetime.now()
        )
        
        # 添加到数据库并提交
        db.session.add(new_comment)
        db.session.commit()
        
        # 返回成功响应
        return jsonify({
            "status": "success",
            "message": "评论添加成功",
            "comment_id": new_comment.id
        }), 201
    except Exception as e:
        logger.error(f"添加评论时出错: {str(e)}")
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

# 文字搜图接口
@app.route('/api/text-to-image-search', methods=['POST'])
def text_to_image_search():
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 检查是否提供了文本查询
        if not data or 'query' not in data:
            return jsonify({"error": "没有提供文本查询"}), 400
            
        text_query = data.get('query')
        
        # 检查查询文本是否为空
        if not text_query or text_query.strip() == '':
            return jsonify({"error": "查询文本为空"}), 400
            
        # 处理文字搜图请求
        results = process_text_search_request(text_query)
        
        # 返回搜索结果
        return jsonify(results)
    except Exception as e:
        logger.error(f"文字搜图时出错: {str(e)}")
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
            return jsonify({"error": "File not found"}), 404
            
        return send_from_directory(IMAGE_FOLDER, safe_filename)
    except Exception as e:
        logger.error(f"提供图片访问时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        logger.error(f"提供上传图片访问时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 更新帖子浏览次数
@app.route('/api/posts/<int:post_id>/views', methods=['POST'])
def update_post_views(post_id):
    try:
        from utils.views import update_post_views as update_views
        
        # 更新浏览次数
        result = update_views(post_id)
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"更新浏览次数时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 获取帖子图片
@app.route('/api/posts/<int:post_id>/images', methods=['GET'])
def get_post_images(post_id):
    try:
        images = Image.query.filter_by(post_id=post_id).all()
        
        result = []
        for image in images:
            image_data = image.to_dict()
            # 拼接完整 URL
            image_data['url'] = f"http://127.0.0.1:5000/images/{image.file_name}"
            result.append(image_data)
        
        logger.debug(f"返回词条 {post_id} 的图片数据: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取图片时出错: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# 用户上传图片到词条（待审核）
@app.route('/api/posts/<int:post_id>/upload-image', methods=['POST'])
def upload_image_to_post(post_id):
    try:
        # 检查帖子是否存在
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"status": "error", "message": "词条不存在"}), 404
            
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "没有文件"}), 400
            
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({"status": "error", "message": "没有选择文件"}), 400
            
        # 检查文件类型
        if file and allowed_file(file.filename):
            # 安全处理文件名
            filename = secure_filename(file.filename)
            # 添加时间戳前缀，避免文件名冲突
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{timestamp}_{filename}"
            
            # 保存文件到未审核图片文件夹
            file_path = os.path.join(UNCENSORED_IMAGE_FOLDER, new_filename)
            file.save(file_path)
            
            # 从请求头中获取token（用户信息）
            token = request.headers.get('Authorization')
            username = '匿名用户'
            
            # 如果有token，从token中提取用户名
            if token and token.startswith('user-token-'):
                username = token.replace('user-token-', '')
                
            # 获取用户提供的描述信息
            description = request.form.get('description', '')
            
            # 读取现有的info.json文件
            uncensored_images_info = {}
            if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
                try:
                    with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                        uncensored_images_info = json.load(f)
                except json.JSONDecodeError:
                    logger.warning("info.json文件格式错误，将创建新文件")
                    uncensored_images_info = {}
            
            # 生成图片ID
            image_id = f"uncensored_{len(uncensored_images_info) + 1}"
            
            # 添加新图片信息
            uncensored_images_info[image_id] = {
                "file_name": new_filename,
                "post_id": post_id,
                "entry": f"entry{post_id}",
                "uploader": username,
                "upload_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": description,
                "status": "pending"  # 待审核状态
            }
            
            # 保存更新后的info.json文件
            with open(UNCENSORED_INFO_FILE, 'w', encoding='utf-8') as f:
                json.dump(uncensored_images_info, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                "status": "success", 
                "message": "图片上传成功，等待管理员审核",
                "image": {
                    "id": image_id,
                    "file_name": new_filename,
                    "post_id": post_id,
                    "status": "pending"
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "不允许的文件类型"}), 400
    except Exception as e:
        logger.error(f"上传图片到词条时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# 启动应用
if __name__ == '__main__':
    with app.app_context():
        # 初始化图像搜索索引
        initialize_index()
        # 初始化文字搜图索引
        initialize_text_to_image_index()
    app.run(debug=True, port=5000)