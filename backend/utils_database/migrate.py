from flask import Flask
from models import db
from sqlalchemy import text, inspect

app = Flask(__name__)
# 使用MySQL数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fanggege@localhost/aiframequest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    try:
        # 检查数据库中的表
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"数据库中的表: {tables}")
        
        # 检查表是否存在，如果存在则添加列
        if 'posts' in tables:
            # 检查列是否已存在
            columns = [column['name'] for column in inspector.get_columns('posts')]
            if 'views' not in columns:
                db.session.execute(text('ALTER TABLE posts ADD COLUMN views INTEGER DEFAULT 0'))
                db.session.commit()
                print('成功添加views列到posts表')
            else:
                print('views列已存在于posts表中')
        else:
            print('未找到posts表')
    except Exception as e:
        print(f"执行过程中出错: {str(e)}")