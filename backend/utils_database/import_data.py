

import os
import json
from flask import Flask
from models import db, Post, Image, User, Comment, Admin

app = Flask(__name__)
app.config.from_pyfile('config.py')  # 确保 config.py 在 backend/ 目录下
db.init_app(app)

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

# JSON 文件路径
ENTRIES_JSON_PATH = os.path.join(BASE_DIR, 'data', 'entries.json')      
IMAGES_JSON_PATH = os.path.join(BASE_DIR, 'data', 'images.json')
USERS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'users.json')
ADMINS_JSON_PATH = os.path.join(BASE_DIR, 'data', 'admins.json')

def import_posts():
    """将 entries.json 导入 posts 表"""
    print("正在导入帖子数据...")
    try:
        with open(ENTRIES_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key in data:
            entry = data[key]
            existing_post = Post.query.get(entry['id'])
            if not existing_post:
                post = Post(
                    id=entry['id'],
                    title=entry['title'],
                    description=json.dumps(entry['description'], ensure_ascii=False),
                    cover=entry['cover'],
                    type=entry['type'],
                  
                )
                db.session.add(post)

        db.session.commit()
        print("帖子数据导入完成")
    except Exception as e:
        print(f"帖子数据导入失败: {str(e)}")

def import_comments():
    with app.app_context():
        print("正在导入评论数据...")
        with open(ENTRIES_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key in data:
            entry = data[key]
            post_id = entry['id']
            
            # 遍历每条评论
            for comment_data in entry.get('comments', []):
                    comment = Comment(
                        post_id=post_id,
                        name=comment_data['name'],
                        text=comment_data['text'],
                        rating=comment_data.get('rating', 0),
                        date=comment_data.get('date')
                    )
                    db.session.add(comment)

        db.session.commit()
        print(" 评论数据已成功导入数据库")

def import_images():
    """将 images.json 导入 images 表"""
    print(" 正在导入图片数据...")
    try:
        with open(IMAGES_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key in data:
            image_data = data[key]
            existing_image = Image.query.get(image_data['id'])
            if not existing_image:
                image = Image(
                    id=image_data['id'],
                    file_name=image_data['file_name'],
                    entry=image_data['entry'],
                    post_id=int(image_data['entry'][5:])
                )
                db.session.add(image)

        db.session.commit()
        print(" 图片数据导入完成")
    except Exception as e:
        print(f" 图片数据导入失败: {str(e)}")


def import_users():
    """将 users.json 导入 users 表"""
    print(" 正在导入用户数据...")
    try:
        with open(USERS_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key in data:
            user_data = data[key]
            existing_user = User.query.get(user_data['id'])
            if not existing_user:
                user = User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data.get('role', 'user')
                )
                db.session.add(user)

        db.session.commit()
        print(" 用户数据导入完成")
    except Exception as e:
        print(f" 用户数据导入失败: {str(e)}")


def import_admins():
    """将 admins.json 导入 admins 表"""
    print(" 正在导入管理员数据...")
    try:
        with open(ADMINS_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key in data:
            admin_data = data[key]
            existing_admin = Admin.query.get(admin_data['id'])
            if not existing_admin:
                admin = Admin(
                    id=admin_data['id'],
                    username=admin_data['username'],
                    email=admin_data['email'],
                    password=admin_data['password'],
                    role=admin_data.get('role', 'admin')
                )
                db.session.add(admin)

        db.session.commit()
        print(" 管理员数据导入完成")
    except Exception as e:
        print(f" 管理员数据导入失败: {str(e)}")


if __name__ == '__main__':
    with app.app_context():
        import_posts()
        import_images()
        import_users()
        import_admins()
        import_comments()
        print(" 所有数据已成功导入数据库！")