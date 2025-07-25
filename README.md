# AIFrameQuest 项目

AIFrameQuest是一个基于 Flask 和 Vue 的现代化社区讨论平台，支持用户认证、内容管理、图像搜索等功能。

在数字时代，我们被海量拟像（数字图像、虚拟存在）包围。虎扑评分将社会抽象为彻底的景观，符号成为唯一的货币；豆瓣是恢复主体性的挣扎，但是后真相不是真相，主体性成为陈词滥调后大众观点也廉价无比。

本软件旨在通过将拟像抽象为可作为价值交换卡片（类似于我们小时候玩的赛尔号卡牌）和审慎的管理系统，帮助用户建立与数字拟像的良性互动关系，探索如何在虚实交织的世界中保持认知平衡。当你认可一个符号后，你才有资格了解一个符号。正像当你爱上一个人后，你才能真正了解ta。

我们用地质时代来为我们的版本命名，因为对于拟像社会的重构是一条漫长的道路，要求我们溯流而上，之后才能顺流而下。我们邀请你和我们一起，在求索世界的过程中中寻找自我，在成为自我的过程中重塑世界。

![图片1](https://github.com/user-attachments/assets/5e0a1fcd-eeff-4e08-8438-7e7e75ec141e)

![image](https://github.com/user-attachments/assets/0def83a1-4d93-419a-af91-b88c194304c1)

## 🙌 设计团队
感谢以下成员的杰出贡献（按字母顺序排列）：

[@Dame](https://github.com/dame-byte)

[@Echo](https://github.com/Echo301)

[@Woodzidream](https://github.com/woodzidream)

[@wwwTwilight](https://github.com/wwwTwilight)

[@yixinD777](https://github.com/yixinD777)

## 🌌 项目概述

本项目是一个完整的全栈应用，包含以下组件：

| 组件名称 | 技术栈 | 说明 |
|---------|-------|------|
| 用户前端 | Vue 3 + Element Plus | 普通用户访问的前端界面 |
| 管理后台前端 | Vue 3 + Element Plus | 管理员使用的后台管理界面 |
| 用户后端 | Flask | 处理普通用户请求的后端服务 |
| 管理后台后端 | Flask | 处理管理员请求的后端服务 |

## 🔮 功能特点

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
- 💡 用户模块：支持识图问答、文字搜图（多模态检索）、图片上传申请
- 🛡️ 管理员模块：支持AI自动审核图片与评论

## 🏛️ 项目结构

```
AIFrameQuest/
├── backend/                # 后端代码
│   ├── app.py             # 用户后端入口
│   ├── app-admin.py       # 管理后台后端入口
│   ├── requirements.txt   # 后端依赖
│   ├── data/              # JSON 数据文件
│   ├── images/            # 图片存储目录
│   ├── uploads/           # 上传文件临时目录
│   ├── utils/             # 用户端工具函数
│   │   ├── faiss_search.py # 图像搜索功能
│   │   ├── list.py         # 帖子管理功能
│   │   ├── login.py        # 用户认证功能
│   │   └── views.py        # 浏览次数统计功能
│   ├── utils_admin/       # 管理后台工具函数
│   └── utils_database/    # 数据库相关工具
│       ├── config.py       # 数据库配置
│       ├── init_db.py      # 数据库初始化脚本
│       ├── import_data.py  # 数据导入脚本
│       ├── models.py       # 数据库模型定义
│       └── migrate.py      # 数据库迁移脚本
├── frontend/              # 用户前端代码
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   ├── package.json       # 前端依赖
│   └── vite.config.js     # Vite 配置
└── frontend-admin/        # 管理后台前端代码
    ├── src/               # 源代码
    ├── public/            # 静态资源
    ├── package.json       # 前端依赖
    └── vite.config.js     # Vite 配置
```

## ⚗️ 环境要求

### 后端
- Python >= 3.8
- MySQL >= 5.7

### 前端
- Node.js >= 16.0.0
- npm >= 7.0.0

## 🚀 部署步骤

### 1. 克隆项目

```bash
git clone [项目地址]
cd AIFrameQuest
```

### 2. 配置数据库

#### 2.1 创建 MySQL 数据库

```sql
CREATE DATABASE aiframequest CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 2.2 配置数据库连接

编辑 `backend/utils_database/config.py` 文件，修改数据库连接信息：

```python
# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': '你的用户名',            # 修改为你自己的用户名
    'password': '你的密码',          # 修改为你自己的密码
    'database': 'aiframequest'      # 修改为你创建的库名称
}
```

### 3. 部署后端

#### 3.1 安装后端依赖

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# Linux/Mac 激活虚拟环境
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3.2 初始化数据库

```bash
# 创建数据表
python -m utils_database.init_db

# 导入初始数据
python -m utils_database.import_data
```

#### 3.3 启动后端服务

```bash
# 启动用户后端（端口 5000）
python app.py

# 在另一个终端启动管理后台后端（端口 5001）
python app-admin.py
```

对于生产环境，建议使用以下方式部署：

```bash
# Windows 使用 Waitress
pip install waitress
waitress-serve --port=5000 app:app
waitress-serve --port=5001 app-admin:app

# Linux/Mac 使用 Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
gunicorn -w 4 -b 0.0.0.0:5001 app-admin:app
```

### 4. 部署前端

#### 4.1 安装前端依赖并启动用户前端

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run dev

# 或构建生产版本
npm run build
```

#### 4.2 安装前端依赖并启动管理后台前端

```bash
cd frontend-admin

# 安装依赖
npm install

# 开发模式启动
npm run serve

# 或构建生产版本
npm run build
```

### 5. 配置前端环境变量

#### 5.1 用户前端环境变量

创建 `.env.development` 或 `.env.production` 文件：

```env
VITE_APP_API_BASE_URL=http://localhost:5000  # 后端API基础URL
```

#### 5.2 管理后台前端环境变量

创建 `.env.development` 或 `.env.production` 文件：

```env
VUE_APP_API_BASE_URL=http://localhost:5001  # 后端API基础URL
```

### 6. 使用 Nginx 部署（生产环境）

#### 6.1 用户前端 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /images/ {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

#### 6.2 管理后台前端 Nginx 配置

```nginx
server {
    listen 80;
    server_name admin.your-domain.com;

    root /path/to/frontend-admin/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/admin/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/images/ {
        proxy_pass http://127.0.0.1:5001;
    }
}
```

## 🌍 访问应用

- 用户前端：http://localhost:5173 (开发) 或 http://your-domain.com (生产)
- 管理后台前端：http://localhost:8080 (开发) 或 http://admin.your-domain.com (生产)
- 用户后端 API：http://localhost:5000
- 管理后台后端 API：http://localhost:5001

## 🗿 常见问题

### 1. 数据库连接问题

- 确保 MySQL 服务已启动
- 检查用户名和密码是否正确
- 确保数据库名称正确

### 2. 图片相似度搜索问题

- 确保已安装 FAISS 和 PyTorch
- 检查图片目录权限是否正确
- 确保图片格式支持（JPG、PNG）

### 3. 前端构建问题

- 确保 Node.js 和 npm 版本符合要求
- 检查环境变量配置是否正确
- 确保所有依赖已正确安装

### 4. 浏览次数统计问题

- 确保前端正确调用了更新浏览次数的API
- 检查数据库中views字段是否正确更新

## 🗺️ 开发阶段路线图  

### 太古代·Beta版（Archean: Beta）  
**核心目标**：验证基础交互模型可行性  
```plaintext
📌 技术实现：  
- 原生JavaScript搭建图片上传/检索原型  
- 基础按钮点击、数据展示交互验证  
- 浏览器本地JSON文件模拟数据存储  

🔍 阶段命名逻辑：  
类比地球生命起源初期，建立最原始的系统基础架构雏形  

```

### 寒武纪·V1版（Cambrian: V1）  
**核心目标**：构建基础功能模块框架  
```plaintext
📌 技术实现：  
- Vue3 + ElementPlus搭建前端界面  
- 实现账号注册/图片搜索/五星评分功能  
- 基于Flask开发简易后端API  

🔍 阶段命名逻辑：  
如同寒武纪生命大爆发，实现功能模块的快速迭代  

```

### 奥陶纪·V2版（Ordovician: V2）  
**核心目标**：增强系统稳定性与扩展性  
```plaintext
📌 技术实现：  
- MySQL替代本地JSON存储用户数据  
- 新增词条申请功能  
- 管理员后台（基础权限控制+数据看板）
- 注入1000+条模拟图片/词条数据(小红书爬虫) 
- 基于深度学习的评论情感分析

🔍 阶段命名逻辑：  
对应奥陶纪生态复杂化，系统开始支撑多角色协作  

```

### 全新世·V3版（Holocene: V3）  
**核心目标**：提升用户体验与数据完整性  
```plaintext
📌 技术实现：  
- 界面视觉改版  
- 优化组件加载速度与交互动效  
- 云端部署（灵感来源于第三周探索性任务）
- 多模态搜索功能（灵感来源于第三周探索性任务）
- 用户互动游戏（灵感来源于第三周探索性任务）

🔍 阶段命名逻辑：  
象征人类文明成熟期，系统进入易用稳定阶段  

```

### 人类世·V4版（Anthropocene: V4）  
**核心目标**：引入智能管理机制  
```plaintext
📌 技术实现：   
- 大模型半自动化词条审核流程
- 与各大网站产生关联（暂定MCP）

🔍 阶段命名逻辑：  
呼应人工智能时代，建立人机协同的内容治理边界  

```


## ⚖️ 许可证

[MIT License](LICENSE)

## 🪨 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。
