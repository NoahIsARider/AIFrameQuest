import os

# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',            # 修改为你自己的用户名
    'password': '00000000',  # 修改为你自己的密码
    'database': 'aiframequest'  #修改为你创建的库名称 ，建议还是这个名
}

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
