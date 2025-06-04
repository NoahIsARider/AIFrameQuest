import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils_admin.auth import verify_admin, generate_admin_token, token_required
import os
import json
import shutil
from werkzeug.utils import secure_filename
from utils_database.models import db, Post, Comment, Image, User
import datetime

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 配置Flask应用
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fanggege@localhost/aiframequest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 确保上传文件夹存在
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 图片文件夹路径
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# 未审核图片文件夹路径
UNCENSORED_IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images_uncensored')
os.makedirs(UNCENSORED_IMAGE_FOLDER, exist_ok=True)

# 未审核图片信息文件路径
UNCENSORED_INFO_FILE = os.path.join(UNCENSORED_IMAGE_FOLDER, 'info.json')

# 数据文件夹路径
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 管理员登录接口
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        admin_id = data.get('id')
        email = data.get('email')
        password = data.get('password')
        
        if not admin_id or not email or not password:
            return jsonify({"status": "error", "message": "ID、邮箱和密码不能为空"}), 400
        
        admin = verify_admin(admin_id, email, password)
        if admin:
            token = generate_admin_token(admin_id, email)
            return jsonify({
                "status": "success", 
                "message": "登录成功",
                "token": token,
                "admin": {
                    "id": admin_id,
                    "username": admin.get('username'),
                    "email": email,
                    "role": admin.get('role')
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "ID、邮箱或密码错误"}), 401
    except Exception as e:
        logger.error(f"管理员登录出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取所有词条
@app.route('/api/admin/entries', methods=['GET'])
@token_required
def get_entries(current_admin):
    try:
        posts = Post.query.all()
        entries = {}
        
        for post in posts:
            entry_key = f"entry{post.id}"
            description = json.loads(post.description) if post.description else []
            
            # 获取评论
            comments = []
            for comment in post.comments:
                comments.append({
                    "name": comment.name,
                    "text": comment.text,
                    "rating": comment.rating or 0,
                    "date": comment.date.isoformat() if comment.date else ""
                })
            
            entries[entry_key] = {
                "id": post.id,
                "title": post.title,
                "type": post.type,
                "description": description,
                "cover": post.cover,
                "comments": comments
            }
        
        return jsonify({"status": "success", "entries": entries}), 200
    except Exception as e:
        logger.error(f"获取词条出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取单个词条
@app.route('/api/admin/entries/<entry_id>', methods=['GET'])
@token_required
def get_entry(current_admin, entry_id):
    try:
        # 从entry_id中提取数字部分
        post_id = int(entry_id.replace("entry", ""))
        post = Post.query.get(post_id)
        
        if post:
            description = json.loads(post.description) if post.description else []
            
            # 获取评论
            comments = []
            for comment in post.comments:
                comments.append({
                    "name": comment.name,
                    "text": comment.text,
                    "rating": comment.rating or 0,
                    "date": comment.date.isoformat() if comment.date else ""
                })
            
            entry = {
                "id": post.id,
                "title": post.title,
                "type": post.type,
                "description": description,
                "cover": post.cover,
                "comments": comments
            }
            
            return jsonify({"status": "success", "entry": entry}), 200
        else:
            return jsonify({"status": "error", "message": "词条不存在"}), 404
    except Exception as e:
        logger.error(f"获取词条出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 更新或创建词条
@app.route('/api/admin/entries/<entry_id>', methods=['PUT'])
@token_required
def update_entry(current_admin, entry_id):
    try:
        data = request.get_json()
        
        # 从entry_id中提取数字部分
        post_id = int(entry_id.replace("entry", "")) if entry_id.startswith("entry") else None
        
        # 查找现有帖子或创建新帖子
        post = Post.query.get(post_id) if post_id else None
        
        if not post:
            # 创建新帖子
            post = Post()
            db.session.add(post)
        
        # 更新帖子字段
        post.title = data.get('title', '')
        post.type = data.get('type', '')
        post.cover = data.get('cover', '')
        
        # 处理描述字段
        description = data.get('description', [])
        post.description = json.dumps(description, ensure_ascii=False)
        
        # 提交更改
        db.session.commit()
        
        # 返回更新后的帖子
        entry = {
            "id": post.id,
            "title": post.title,
            "type": post.type,
            "description": description,
            "cover": post.cover,
            "comments": []
        }
        
        return jsonify({"status": "success", "message": "词条更新成功", "entry": entry}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"更新词条出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 删除词条
@app.route('/api/admin/entries/<entry_id>', methods=['DELETE'])
@token_required
def delete_entry(current_admin, entry_id):
    try:
        # 从entry_id中提取数字部分
        post_id = int(entry_id.replace("entry", ""))
        post = Post.query.get(post_id)
        
        if post:
            # 删除与帖子相关的所有评论
            for comment in post.comments:
                db.session.delete(comment)
            
            # 删除帖子
            db.session.delete(post)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "词条删除成功"}), 200
        else:
            return jsonify({"status": "error", "message": "词条不存在"}), 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除词条出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取所有图片（支持分页和筛选）
@app.route('/api/admin/images', methods=['GET'])
@token_required
def get_images(current_admin):
    try:
        # 获取分页和筛选参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        entry_id = request.args.get('entry_id', '')
        
        # 构建查询
        query = Image.query
        
        # 如果提供了词条ID，进行筛选
        if entry_id and entry_id.startswith('entry'):
            post_id = int(entry_id[5:]) if entry_id[5:].isdigit() else None
            if post_id:
                query = query.filter(Image.post_id == post_id)
        
        # 获取总数
        total_count = query.count()
        
        # 分页
        images = query.order_by(Image.id.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        result = {}
        
        for image in images:
            # 获取关联词条的标题
            entry_title = '未关联词条'
            if image.post_id:
                post = Post.query.get(image.post_id)
                if post:
                    entry_title = post.title
            
            image_key = f"image{image.id}"
            result[image_key] = {
                "id": image.id,
                "url": image.file_name,  # 使用file_name字段代替url
                "title": entry_title,  # 使用关联词条的标题
                "entry": image.entry,  # 保留原始entry字段
                "post_id": image.post_id,  # 添加post_id字段
                "description": ""  # 添加空描述
            }
        
        return jsonify({
            "status": "success", 
            "images": result,
            "pagination": {
                "total": total_count,
                "page": page,
                "per_page": per_page,
                "pages": (total_count + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        logger.error(f"获取图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 上传图片
@app.route('/api/admin/upload', methods=['POST'])
@token_required
def upload_image(current_admin):
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "没有文件"}), 400
        
        file = request.files['file']
        entry_id = request.form.get('entry_id', '')
        is_cover = request.form.get('is_cover', 'false').lower() == 'true'
        
        if file.filename == '':
            return jsonify({"status": "error", "message": "没有选择文件"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(IMAGE_FOLDER, new_filename)
            file.save(file_path)
            
            # 创建新的图片记录，同时设置entry和post_id
            post_id = None
            if entry_id:
                # 如果entry_id格式为'entry数字'，提取数字部分作为post_id
                if entry_id.startswith('entry') and entry_id[5:].isdigit():
                    post_id = int(entry_id[5:])
                # 如果entry_id本身就是数字，直接使用
                elif entry_id.isdigit():
                    post_id = int(entry_id)
                    
                # 只有当明确指定是封面上传时，才更新词条的cover字段
                if post_id and is_cover:
                    post = Post.query.get(post_id)
                    if post:
                        post.cover = new_filename
                        # 移除这里的commit，统一在下面提交
                        logger.debug(f"更新词条 {post_id} 的封面为 {new_filename}")
            
            image = Image(file_name=new_filename, entry=entry_id, post_id=post_id)
            db.session.add(image)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": "图片上传成功",
                "image": {
                    "id": image.id,
                    "file_name": image.file_name,
                    "url": image.file_name,  # 添加url字段，与前端期望的字段名一致
                    "title": image.entry,
                    "description": ""
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "不允许的文件类型"}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"上传图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 删除图片
@app.route('/api/admin/images/<image_id>', methods=['DELETE'])
@token_required
def delete_image(current_admin, image_id):
    try:
        # 从image_id中提取数字部分
        img_id = int(image_id.replace("image", ""))
        image = Image.query.get(img_id)
        
        if image:
            # 删除文件系统中的图片文件
            file_path = os.path.join(IMAGE_FOLDER, image.file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # 删除数据库中的图片记录
            db.session.delete(image)
            db.session.commit()
            
            return jsonify({"status": "success", "message": "图片删除成功"}), 200
        else:
            return jsonify({"status": "error", "message": "图片不存在"}), 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取所有评论
@app.route('/api/admin/comments', methods=['GET'])
@token_required
def get_all_comments(current_admin):
    try:
        comments = Comment.query.all()
        result = []
        
        for comment in comments:
            post = Post.query.get(comment.post_id)
            post_title = post.title if post else "未知词条"
            
            result.append({
                "id": comment.id,
                "post_id": comment.post_id,
                "post_title": post_title,
                "name": comment.name,
                "text": comment.text,
                "rating": comment.rating or 0,
                "date": comment.date.isoformat() if comment.date else ""
            })
        
        return jsonify({"status": "success", "comments": result}), 200
    except Exception as e:
        logger.error(f"获取评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 删除评论
@app.route('/api/admin/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_entry_comment(current_admin, comment_id):
    try:
        comment = Comment.query.get(comment_id)
        
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"status": "success", "message": "评论删除成功"}), 200
        else:
            return jsonify({"status": "error", "message": "评论不存在"}), 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 提供图片文件访问
@app.route('/admin/images/<path:filename>')
def serve_admin_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# 提供未审核图片文件访问
@app.route('/images_uncensored/<path:filename>')
def serve_uncensored_image(filename):
    return send_from_directory(UNCENSORED_IMAGE_FOLDER, filename)

# 获取未审核图片列表
@app.route('/api/admin/uncensored-images', methods=['GET'])
@token_required
def get_uncensored_images(current_admin):
    try:
        # 读取未审核图片信息文件
        uncensored_images = {}
        if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
            try:
                with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                    uncensored_images = json.load(f)
            except json.JSONDecodeError:
                logger.warning("info.json文件格式错误")
                uncensored_images = {}
        
        return jsonify({"status": "success", "images": uncensored_images}), 200
    except Exception as e:
        logger.error(f"获取未审核图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 审核通过图片
@app.route('/api/admin/uncensored-images/<image_id>/approve', methods=['POST'])
@token_required
def approve_image(current_admin, image_id):
    try:
        # 读取未审核图片信息文件
        uncensored_images = {}
        if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
            try:
                with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                    uncensored_images = json.load(f)
            except json.JSONDecodeError:
                logger.warning("info.json文件格式错误")
                return jsonify({"status": "error", "message": "未审核图片信息文件格式错误"}), 500
        
        # 检查图片ID是否存在
        if image_id not in uncensored_images:
            return jsonify({"status": "error", "message": "未找到指定的未审核图片"}), 404
        
        # 获取图片信息
        image_info = uncensored_images[image_id]
        file_name = image_info.get('file_name')
        post_id = image_info.get('post_id')
        entry = image_info.get('entry')
        description = image_info.get('description', '')
        
        # 移动图片文件从未审核文件夹到正式图片文件夹
        src_path = os.path.join(UNCENSORED_IMAGE_FOLDER, file_name)
        dst_path = os.path.join(IMAGE_FOLDER, file_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)  # 复制文件而不是移动，保留原始文件作为备份
            
            # 创建新的图片记录到数据库
            image = Image(file_name=file_name, entry=entry, post_id=post_id)
            db.session.add(image)
            db.session.commit()
            
            # 更新未审核图片状态
            uncensored_images[image_id]['status'] = 'approved'
            
            # 保存更新后的info.json文件
            with open(UNCENSORED_INFO_FILE, 'w', encoding='utf-8') as f:
                json.dump(uncensored_images, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                "status": "success", 
                "message": "图片审核通过，已添加到数据库",
                "image": {
                    "id": image.id,
                    "file_name": file_name,
                    "entry": entry,
                    "post_id": post_id
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "未找到图片文件"}), 404
    except Exception as e:
        db.session.rollback()
        logger.error(f"审核图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 拒绝图片审核
@app.route('/api/admin/uncensored-images/<image_id>/reject', methods=['POST'])
@token_required
def reject_image(current_admin, image_id):
    try:
        # 读取未审核图片信息文件
        uncensored_images = {}
        if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
            try:
                with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                    uncensored_images = json.load(f)
            except json.JSONDecodeError:
                logger.warning("info.json文件格式错误")
                return jsonify({"status": "error", "message": "未审核图片信息文件格式错误"}), 500
        
        # 检查图片ID是否存在
        if image_id not in uncensored_images:
            return jsonify({"status": "error", "message": "未找到指定的未审核图片"}), 404
        
        # 更新未审核图片状态
        uncensored_images[image_id]['status'] = 'rejected'
        
        # 保存更新后的info.json文件
        with open(UNCENSORED_INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump(uncensored_images, f, ensure_ascii=False, indent=2)
        
        return jsonify({"status": "success", "message": "已拒绝该图片"}), 200
    except Exception as e:
        logger.error(f"拒绝图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 情感分析API
from utils_admin.sentiment_analysis import analyze_comments, analyze_sentiment_bert, analyze_sentiment_snownlp, analyze_sentiment_baidu

# 使用SnowNLP分析所有评论
@app.route('/api/admin/analyze/comments/snownlp', methods=['GET'])
@token_required
def analyze_comments_snownlp(current_admin):
    try:
        comments = Comment.query.all()
        comments_data = []
        
        for comment in comments:
            post = Post.query.get(comment.post_id)
            post_title = post.title if post else "未知词条"
            
            # 分析评论情感
            sentiment_result = analyze_sentiment_snownlp(comment.text)
            # 检查是否有错误
            if "error" in sentiment_result:
                logger.warning(f"评论ID {comment.id} 分析失败: {sentiment_result['error']}")
                continue
                
            sentiment_score = sentiment_result["score"]
            sentiment = "正面" if sentiment_score > 0.6 else "负面" if sentiment_score < 0.4 else "中性"
            
            comments_data.append({
                "id": comment.id,
                "post_id": comment.post_id,
                "post_title": post_title,
                "name": comment.name,
                "text": comment.text,
                "rating": comment.rating or 0,
                "date": comment.date.isoformat() if comment.date else "",
                "sentiment_score": sentiment_score,
                "sentiment": sentiment
            })
        
        # 按情感分数排序
        comments_data.sort(key=lambda x: x["sentiment_score"], reverse=True)
        
        return jsonify({"status": "success", "comments": comments_data}), 200
    except Exception as e:
        logger.error(f"分析评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 使用BERT分析所有评论
@app.route('/api/admin/analyze/comments/bert', methods=['GET'])
@token_required
def analyze_comments_bert(current_admin):
    try:
        comments = Comment.query.all()
        comments_data = []
        
        for comment in comments:
            post = Post.query.get(comment.post_id)
            post_title = post.title if post else "未知词条"
            
            # 分析评论情感
            sentiment_result = analyze_sentiment_bert(comment.text)
            
            # 检查是否有错误
            if "error" in sentiment_result:
                logger.warning(f"评论ID {comment.id} BERT分析失败: {sentiment_result['error']}")
                continue
                
            sentiment_score = sentiment_result["score"]
            # 根据分数确定情感标签
            sentiment = "正面" if sentiment_score > 0.6 else "负面" if sentiment_score < 0.4 else "中性"
            
            comments_data.append({
                "id": comment.id,
                "post_id": comment.post_id,
                "post_title": post_title,
                "name": comment.name,
                "text": comment.text,
                "rating": comment.rating or 0,
                "date": comment.date.isoformat() if comment.date else "",
                "sentiment": sentiment,
                "sentiment_score": sentiment_score
            })
        
        # 按情感分数排序
        comments_data.sort(key=lambda x: x["sentiment_score"], reverse=True)
        
        return jsonify({"status": "success", "comments": comments_data}), 200
    except Exception as e:
        logger.error(f"分析评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 使用百度AI分析所有评论
@app.route('/api/admin/analyze/comments/baidu', methods=['GET'])
@token_required
def analyze_comments_baidu(current_admin):
    try:
        comments = Comment.query.all()
        comments_data = []
        
        for comment in comments:
            post = Post.query.get(comment.post_id)
            post_title = post.title if post else "未知词条"
            
            # 分析评论情感
            sentiment_result = analyze_sentiment_baidu(comment.text)
            
            # 检查是否有错误
            if "error" in sentiment_result:
                logger.warning(f"评论ID {comment.id} 百度AI分析失败: {sentiment_result['error']}")
                continue
                
            comments_data.append({
                "id": comment.id,
                "post_id": comment.post_id,
                "post_title": post_title,
                "name": comment.name,
                "text": comment.text,
                "rating": comment.rating or 0,
                "date": comment.date.isoformat() if comment.date else "",
                "sentiment": sentiment_result["sentiment"],
                "sentiment_score": sentiment_result["confidence"]
            })
        
        # 按情感分数排序
        comments_data.sort(key=lambda x: x["sentiment_score"], reverse=True)
        
        return jsonify({"status": "success", "comments": comments_data}), 200
    except Exception as e:
        logger.error(f"分析评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 使用AI审核所有评论
@app.route('/api/admin/analyze/comments/ai_moderation', methods=['GET'])
@token_required
def analyze_comments_ai_moderation(current_admin):
    try:
        # 导入评论审核模块
        from utils_admin.comment_moderation import moderate_comment, analyze_comment_content
        
        comments = Comment.query.all()
        results = []
        
        for comment in comments:
            # 审核评论内容
            moderation_result = moderate_comment(comment.text)
            # 进行深入分析
            content_analysis = analyze_comment_content(comment.text)
            
            results.append({
                "id": comment.id,
                "moderation": moderation_result,
                "content_analysis": content_analysis
            })
        
        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        logger.error(f"AI审核评论出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 使用AI审核所有未审核图片
@app.route('/api/admin/analyze/images/ai_moderation', methods=['GET'])
@token_required
def analyze_images_ai_moderation(current_admin):
    try:
        # 导入图片审核模块
        from utils_admin.image_moderation import moderate_images
        
        # 读取未审核图片信息文件
        uncensored_images = {}
        if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
            try:
                with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                    uncensored_images = json.load(f)
            except json.JSONDecodeError:
                logger.warning("info.json文件格式错误")
                return jsonify({"status": "error", "message": "未审核图片信息文件格式错误"}), 500
        
        # 过滤出待审核的图片
        pending_images = {k: v for k, v in uncensored_images.items() if v.get('status') == 'pending'}
        
        if not pending_images:
            return jsonify({"status": "success", "message": "没有待审核的图片", "results": []}), 200
        
        # 审核图片
        results = moderate_images(pending_images, UNCENSORED_IMAGE_FOLDER)
        
        return jsonify({"status": "success", "results": results}), 200
    except Exception as e:
        logger.error(f"AI审核图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 审核单张图片
@app.route('/api/admin/analyze/images/<image_id>/ai_moderation', methods=['GET'])
@token_required
def analyze_single_image_ai_moderation(current_admin, image_id):
    try:
        # 导入图片审核模块
        from utils_admin.image_moderation import moderate_image, analyze_image_content
        
        # 读取未审核图片信息文件
        uncensored_images = {}
        if os.path.exists(UNCENSORED_INFO_FILE) and os.path.getsize(UNCENSORED_INFO_FILE) > 0:
            try:
                with open(UNCENSORED_INFO_FILE, 'r', encoding='utf-8') as f:
                    uncensored_images = json.load(f)
            except json.JSONDecodeError:
                logger.warning("info.json文件格式错误")
                return jsonify({"status": "error", "message": "未审核图片信息文件格式错误"}), 500
        
        # 检查图片ID是否存在
        if image_id not in uncensored_images:
            return jsonify({"status": "error", "message": "未找到指定的未审核图片"}), 404
        
        # 获取图片信息
        image_info = uncensored_images[image_id]
        file_name = image_info.get('file_name')
        entry = image_info.get('entry')
        
        # 构建图片完整路径
        image_path = os.path.join(UNCENSORED_IMAGE_FOLDER, file_name)
        
        if not os.path.exists(image_path):
            return jsonify({"status": "error", "message": "图片文件不存在"}), 404
        
        # 审核图片
        moderation = moderate_image(image_path, entry)
        
        # 进行深入分析
        content_analysis = analyze_image_content(image_path, entry)
        
        result = {
            'id': image_id,
            'file_name': file_name,
            'entry': entry,
            'moderation': moderation,
            'content_analysis': content_analysis
        }
        
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        logger.error(f"AI审核单张图片出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)