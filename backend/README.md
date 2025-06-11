# AIFrameQuest 后端服务

## 系统架构

本项目后端采用 Flask 框架构建，提供 RESTful API 服务，支持用户认证、内容管理、图像搜索等功能。

## 功能特点

- 🔐 用户注册与登录认证
- 📝 多分类内容管理（动漫、电影、电视剧、游戏等）
- 💬 评论与评分系统
- 🔍 基于 FAISS 的图像相似度搜索
- 🖼️ 静态资源服务（图片文件）
- 📊 RESTful API 设计
- 👨‍💼 完整的管理员后台
- 🔢 帖子浏览次数统计与显示
- ⭐ 用户评分系统
- 🖼️ 多图片轮播展示
- 💡 用户模块增强：实现识图问答、文字搜图（多模态检索）API，以及图片上传申请处理逻辑
- 🛡️ 管理员模块增强：集成AI自动审核图片与评论功能
- 🚀 新增相关API接口以支持上述高级功能

## 技术栈

- **Web 框架**: Flask
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **图像处理**: PIL, FAISS, PyTorch
- **认证**: JWT
- **其他**: NumPy, Pandas
- **AI/ML模型**: 用于支持识图问答、多模态搜索及内容审核

## 环境要求

- Python >= 3.8
- MySQL >= 5.7
- 推荐使用虚拟环境

## 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# Linux/Mac 激活虚拟环境
# source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

## 开发环境配置

### 1. 配置数据库连接

编辑 `utils_database/config.py` 文件，修改数据库连接信息：

```python
# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': '你的用户名',            # 修改为你自己的用户名
    'password': '你的密码',          # 修改为你自己的密码
    'database': 'aiframequest'      # 修改为你创建的库名称
}
```

### 2. 配置 JWT 密钥

编辑 `utils/login.py` 文件，修改 JWT 密钥：

```python
# JWT 密钥
JWT_SECRET = "your-secret-key"  # 修改为你自己的密钥
```

## 项目结构

```
backend/
├── app.py                 # 用户后端入口
├── app-admin.py           # 管理后台后端入口
├── requirements.txt       # 后端依赖
├── data/                  # JSON 数据文件
├── images/                # 图片存储目录
├── uploads/               # 上传文件临时目录
├── utils/                 # 用户端工具函数
│   ├── faiss_search.py    # 图像搜索功能
│   ├── list.py            # 帖子管理功能
│   ├── login.py           # 用户认证功能
│   ├── views.py           # 浏览次数统计功能
│   ├── text_to_image_search.py   # 文字搜图功能
│   └── guess_entry.py     # 识图问答小游戏功能
├── utils_admin/           # 管理后台工具函数
└── utils_database/        # 数据库相关工具
    ├── config.py          # 数据库配置
    ├── init_db.py         # 数据库初始化
    ├── import_data.py     # 数据导入
    └── models.py          # 数据模型
```

## 数据库初始化

### 1. 创建数据库

```sql
CREATE DATABASE aiframequest CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 创建数据表

```bash
python -m utils_database.init_db
```

### 3. 导入初始数据

```bash
python -m utils_database.import_data
```

## 启动服务

### 开发模式

```bash
# 启动用户后端（端口 5000）
python app.py

# 在另一个终端启动管理后台后端（端口 5001）
python app-admin.py
```

### 生产部署

#### 使用 Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
gunicorn -w 4 -b 0.0.0.0:5001 app-admin:app
```

#### 使用 Waitress (Windows)

```bash
pip install waitress
waitress-serve --port=5000 app:app
waitress-serve --port=5001 app-admin:app
```

#### 使用 Docker

```bash
# 构建镜像
docker build -t aiframequest-backend .

# 运行容器
docker run -p 5000:5000 -p 5001:5001 aiframequest-backend
```

## API 文档

### 用户端 API

#### 用户注册

```
URL: /api/register
方法: POST
认证: 不需要
请求体:
{
    "username": "用户名",
    "password": "密码"
}
成功响应:
{
    "message": "注册成功",
    "token": "JWT令牌"
}
```

#### 用户登录

```
URL: /api/login
方法: POST
认证: 不需要
请求体:
{
    "username": "用户名",
    "password": "密码"
}
成功响应:
{
    "message": "登录成功",
    "token": "JWT令牌"
}
```

#### 获取所有帖子

```
URL: /api/posts
方法: GET
认证: 不需要
查询参数:
- category: 分类 (可选)
- page: 页码 (可选，默认为1)
- per_page: 每页数量 (可选，默认为10)
成功响应:
{
    "posts": [
        {
            "id": 1,
            "title": "帖子标题",
            "content": "帖子内容",
            "category": "分类",
            "author": "作者",
            "created_at": "创建时间",
            "updated_at": "更新时间",
            "views": 浏览次数,
            "avg_rating": 平均评分,
            "rating_count": 评分数量,
            "images": ["图片1.jpg", "图片2.jpg"]
        },
        ...
    ],
    "total": 总数量,
    "pages": 总页数,
    "current_page": 当前页码
}
```

#### 获取单个帖子详情

```
URL: /api/posts/<int:post_id>
方法: GET
认证: 不需要
成功响应:
{
    "id": 1,
    "title": "帖子标题",
    "content": "帖子内容",
    "category": "分类",
    "author": "作者",
    "created_at": "创建时间",
    "updated_at": "更新时间",
    "views": 浏览次数,
    "avg_rating": 平均评分,
    "rating_count": 评分数量,
    "images": ["图片1.jpg", "图片2.jpg"],
    "comments": [
        {
            "id": 1,
            "content": "评论内容",
            "author": "评论作者",
            "created_at": "评论时间"
        },
        ...
    ]
}
```

#### 更新帖子浏览次数

```
URL: /api/posts/<int:post_id>/views
方法: POST
认证: 不需要
请求体: 不需要
成功响应:
{
    "message": "浏览次数已更新",
    "views": 更新后的浏览次数
}
```

#### 创建新帖子

```
URL: /api/posts
方法: POST
认证: 需要 JWT
请求体:
{
    "title": "帖子标题",
    "content": "帖子内容",
    "category": "分类"
}
成功响应:
{
    "message": "帖子创建成功",
    "post_id": 帖子ID
}
```

#### 更新帖子

```
URL: /api/posts/<int:post_id>
方法: PUT
认证: 需要 JWT
请求体:
{
    "title": "新标题",
    "content": "新内容",
    "category": "新分类"
}
成功响应:
{
    "message": "帖子更新成功"
}
```

#### 删除帖子

```
URL: /api/posts/<int:post_id>
方法: DELETE
认证: 需要 JWT
成功响应:
{
    "message": "帖子删除成功"
}
```

#### 添加评论

```
URL: /api/posts/<int:post_id>/comments
方法: POST
认证: 需要 JWT
请求体:
{
    "content": "评论内容",
    "rating": 评分 (1-5, 可选)
}
成功响应:
{
    "message": "评论添加成功",
    "comment_id": 评论ID
}
```

#### 获取帖子的所有图片

```
URL: /api/posts/<int:post_id>/images
方法: GET
认证: 不需要
成功响应:
{
    "images": ["图片1.jpg", "图片2.jpg", ...]
}
```

#### 访问图片文件

```
URL: /images/<path:filename>
方法: GET
认证: 不需要
成功响应: 图片文件
```

#### 访问上传的文件

```
URL: /uploads/<path:filename>
方法: GET
认证: 不需要
成功响应: 上传的文件
```

#### 图片搜索

```
URL: /api/search/image
方法: POST
认证: 不需要
请求体: 表单数据，包含图片文件
成功响应:
{
    "results": [
        {
            "post_id": 帖子ID,
            "title": "帖子标题",
            "image": "图片文件名",
            "similarity": 相似度
        },
        ...
    ]
}
```

### 管理后台 API

#### 管理员登录

```
URL: /api/admin/login
方法: POST
认证: 不需要
请求体:
{
    "username": "管理员用户名",
    "password": "管理员密码"
}
成功响应:
{
    "message": "登录成功",
    "token": "JWT令牌"
}
```

#### 获取所有词条

```
URL: /api/admin/posts
方法: GET
认证: 需要管理员 JWT
查询参数:
- category: 分类 (可选)
- page: 页码 (可选，默认为1)
- per_page: 每页数量 (可选，默认为10)
成功响应:
{
    "posts": [
        {
            "id": 1,
            "title": "帖子标题",
            "content": "帖子内容",
            "category": "分类",
            "author": "作者",
            "created_at": "创建时间",
            "updated_at": "更新时间",
            "views": 浏览次数,
            "avg_rating": 平均评分,
            "rating_count": 评分数量
        },
        ...
    ],
    "total": 总数量,
    "pages": 总页数,
    "current_page": 当前页码
}
```

#### 更新词条

```
URL: /api/admin/posts/<int:post_id>
方法: PUT
认证: 需要管理员 JWT
请求体:
{
    "title": "新标题",
    "content": "新内容",
    "category": "新分类",
    "author": "新作者"
}
成功响应:
{
    "message": "词条更新成功"
}
```

#### 创建词条

```
URL: /api/admin/posts
方法: POST
认证: 需要管理员 JWT
请求体:
{
    "title": "帖子标题",
    "content": "帖子内容",
    "category": "分类",
    "author": "作者"
}
成功响应:
{
    "message": "词条创建成功",
    "post_id": 词条ID
}
```

#### 删除词条

```
URL: /api/admin/posts/<int:post_id>
方法: DELETE
认证: 需要管理员 JWT
成功响应:
{
    "message": "词条删除成功"
}
```

#### 获取所有图片

```
URL: /api/admin/images
方法: GET
认证: 需要管理员 JWT
查询参数:
- page: 页码 (可选，默认为1)
- per_page: 每页数量 (可选，默认为20)
成功响应:
{
    "images": [
        {
            "id": 1,
            "filename": "图片文件名",
            "post_id": 关联的帖子ID,
            "created_at": "创建时间"
        },
        ...
    ],
    "total": 总数量,
    "pages": 总页数,
    "current_page": 当前页码
}
```

#### 上传图片

```
URL: /api/admin/images
方法: POST
认证: 需要管理员 JWT
请求体: 表单数据，包含图片文件和post_id
成功响应:
{
    "message": "图片上传成功",
    "image_id": 图片ID,
    "filename": "图片文件名"
}
```

#### 删除图片

```
URL: /api/admin/images/<int:image_id>
方法: DELETE
认证: 需要管理员 JWT
成功响应:
{
    "message": "图片删除成功"
}
```

#### 访问管理后台图片

```
URL: /admin/images/<path:filename>
方法: GET
认证: 不需要
成功响应: 图片文件
```

#### 获取所有评论

```
URL: /api/admin/comments
方法: GET
认证: 需要管理员 JWT
查询参数:
- post_id: 帖子ID (可选)
- page: 页码 (可选，默认为1)
- per_page: 每页数量 (可选，默认为20)
成功响应:
{
    "comments": [
        {
            "id": 1,
            "content": "评论内容",
            "author": "评论作者",
            "post_id": 关联的帖子ID,
            "post_title": "帖子标题",
            "created_at": "评论时间",
            "rating": 评分
        },
        ...
    ],
    "total": 总数量,
    "pages": 总页数,
    "current_page": 当前页码
}
```

#### 删除评论

```
URL: /api/admin/comments/<int:comment_id>
方法: DELETE
认证: 需要管理员 JWT
成功响应:
{
    "message": "评论删除成功"
}
```

## 浏览次数统计实现

浏览次数统计功能通过以下组件实现：

1. 数据库模型：`Post` 模型中的 `views` 字段存储浏览次数
2. API 接口：`/api/posts/<int:post_id>/views` 用于更新浏览次数
3. 后端实现：`utils/views.py` 中的 `update_post_views` 函数处理浏览次数更新逻辑
4. 前端调用：当用户访问帖子详情页时，前端会自动调用更新浏览次数的 API

## 许可证

[MIT License](../LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。