from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化数据库
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 注册蓝图
    from app.routes.home import home_bp
    from app.routes.hot import hot_bp
    from app.routes.my import my_bp
    from utils.register.routes import auth_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(hot_bp)
    app.register_blueprint(my_bp)
    app.register_blueprint(auth_bp)
    
    return app 