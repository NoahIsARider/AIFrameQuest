# AIFrameQuest 后端服务

一个基于 Flask 的现代化社区讨论平台后端，支持用户认证、内容管理、图像搜索等功能。

## 功能特点

- 🔐 用户注册与登录认证
- 📝 多分类内容管理（动漫、电影、电视剧、游戏等）
- 💬 评论与评分系统
- 🔍 基于 FAISS 的图像相似度搜索
- 🖼️ 静态资源服务（图片文件）
- 📊 RESTful API 设计

## 技术栈

- Flask 3.0.2 - 轻量级 Web 框架
- Flask-CORS - 跨域资源共享支持
- Flask-SQLAlchemy - ORM 数据库支持
- FAISS - Facebook AI 相似性搜索库
- PyTorch - 深度学习框架（用于图像特征提取）
- JSON - 轻量级数据存储

## 项目设置

### 环境要求

- Python >= 3.8
- pip >= 20.0.0

### 安装步骤

1. 克隆项目
```bash
git clone [项目地址]
cd [项目目录]/backend
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 启动服务器
```bash
python app.py
```

### 开发环境配置

1. 确保已安装所需依赖：
```bash
pip install Flask Flask-CORS Flask-SQLAlchemy python-dotenv PyMySQL
```

2. 对于图像搜索功能，还需安装：
```bash
pip install faiss-cpu torch torchvision Pillow
```

## 项目结构

```
backend/
├── app.py              # 主应用入口
├── requirements.txt    # 依赖列表
├── data/               # 数据存储目录
│   ├── entries.json    # 帖子数据
│   ├── images.json     # 图片元数据
│   └── users.json      # 用户数据
├── images/             # 图片存储目录
├── uploads/            # 上传文件临时目录
└── utils/              # 工具函数目录
    ├── faiss_search.py # 图像搜索功能
    ├── list.py         # 帖子管理功能
    └── login.py        # 用户认证功能
```

## 使用说明

### 开发模式

1. 启动开发服务器：
```bash
python app.py
```

2. 访问开发环境：
- API 服务器运行在 `http://127.0.0.1:5000`
- 可以使用 Postman 或其他 API 测试工具进行接口测试

### 生产部署

1. 使用 Gunicorn 部署（Linux/Mac）：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. 使用 Waitress 部署（Windows）：
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

3. 使用 Docker 部署：
```bash
# 创建 Dockerfile
docker build -t aiframequest-backend .
docker run -p 5000:5000 aiframequest-backend
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /images/ {
        alias /path/to/your/backend/images/;
        expires 7d;
    }

    location /uploads/ {
        alias /path/to/your/backend/uploads/;
        expires 1d;
    }
}
```

## API 文档

### 用户认证

#### 注册用户
- **URL**: `/api/auth/register`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "username": "用户名",
    "email": "邮箱",
    "password": "密码"
  }
  ```
- **成功响应**: `200 OK`
  ```json
  {
    "status": "success",
    "message": "注册成功"
  }
  ```

#### 用户登录
- **URL**: `/api/auth/login`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "email": "邮箱",
    "password": "密码"
  }
  ```
- **成功响应**: `200 OK`
  ```json
  {
    "status": "success",
    "message": "登录成功",
    "token": "user-token-username"
  }
  ```

### 帖子管理

#### 获取所有帖子
- **URL**: `/api/posts`
- **方法**: `GET`
- **成功响应**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "帖子标题",
      "content": "帖子内容",
      "author": "作者",
      "category": "动漫",
      "date": "2023-01-01",
      "views": 0,
      "comments": 1,
      "favorites": 0,
      "cover": "封面图片URL",
      "type": "动漫",
      "description": ["描述1", "描述2"]
    }
  ]
  ```

#### 获取单个帖子
- **URL**: `/api/posts/{post_id}`
- **方法**: `GET`
- **成功响应**: `200 OK`
  ```json
  {
    "id": 1,
    "title": "帖子标题",
    "type": "动漫",
    "description": ["描述1", "描述2"],
    "comments": [
      {
        "name": "评论者",
        "text": "评论内容",
        "rating": 5,
        "date": "2023-01-01"
      }
    ],
    "avg_rating": 5.0,
    "rating_count": 1
  }
  ```

#### 创建帖子
- **URL**: `/api/posts`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "title": "帖子标题",
    "content": "帖子内容",
    "author": "作者",
    "category": "动漫"
  }
  ```
- **成功响应**: `201 Created`

#### 更新帖子
- **URL**: `/api/posts/{post_id}`
- **方法**: `PUT`
- **请求体**:
  ```json
  {
    "title": "更新的标题",
    "content": "更新的内容"
  }
  ```
- **成功响应**: `200 OK`

#### 删除帖子
- **URL**: `/api/posts/{post_id}`
- **方法**: `DELETE`
- **成功响应**: `200 OK`
  ```json
  {
    "message": "删除成功"
  }
  ```

### 评论管理

#### 添加评论
- **URL**: `/api/posts/{post_id}/comments`
- **方法**: `POST`
- **请求体**:
  ```json
  {
    "name": "评论者",
    "text": "评论内容",
    "rating": 5,
    "date": "2023-01-01"
  }
  ```
- **成功响应**: `200 OK`

### 图片管理

#### 获取帖子相关图片
- **URL**: `/api/posts/{post_id}/images`
- **方法**: `GET`
- **成功响应**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "file_name": "image1.jpg",
      "url": "http://127.0.0.1:5000/images/image1.jpg"
    }
  ]
  ```

#### 图片相似度搜索
- **URL**: `/api/image-search`
- **方法**: `POST`
- **请求体**: `multipart/form-data` 包含 `file` 字段
- **成功响应**: `200 OK`
  ```json
  {
    "query_image": "uploaded.jpg",
    "results": [
      {
        "image": "similar1.jpg",
        "distance": 0.25,
        "entry_info": {...}
      }
    ]
  }
  ```

#### 访问图片文件
- **URL**: `/images/{filename}`
- **方法**: `GET`
- **成功响应**: 图片文件

#### 访问上传的图片文件
- **URL**: `/uploads/{filename}`
- **方法**: `GET`
- **成功响应**: 图片文件

## 常见问题

1. 如果遇到 FAISS 安装问题：
```bash
# 对于 CPU 版本
pip install faiss-cpu
# 对于 GPU 版本
pip install faiss-gpu
```

2. 如果遇到图片加载问题：
- 确保图片目录权限正确
- 检查图片路径是否正确
- 确保图片格式支持（JPG、PNG）

3. 如果遇到跨域问题：
- 确保 Flask-CORS 正确配置
- 检查前端请求头设置

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。