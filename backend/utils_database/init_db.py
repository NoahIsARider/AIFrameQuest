import os
import sys
from flask import Flask
from models import db, Post, Image, User,Admin
import config

# 添加项目根目录到系统路径（确保能导入 utils）
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库扩展
db.init_app(app)

try:
    with app.app_context():
        print(" 正在进入应用上下文...")
        
        # 打印当前数据库 URI 验证是否正确
        print(f" 当前数据库: {app.config['SQLALCHEMY_DATABASE_URI']}")

        # 创建所有表
        print(" 开始创建数据库表...")
        db.create_all()
        print(" 成功创建所有数据库表！")
        
except Exception as e:
    print(f" 脚本执行出错: {str(e)}")