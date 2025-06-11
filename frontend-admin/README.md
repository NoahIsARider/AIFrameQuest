# AIFrameQuest 管理后台前端

## 功能特点

- 🔐 管理员登录认证
- 📝 帖子内容管理（查看、编辑、创建、删除）
- 🖼️ 图片资源管理（查看、上传、删除）
- 💬 评论管理（查看、删除）
- 📊 数据统计与分析
- 🔢 浏览次数与评分数据管理
- 🤖 AI内容审核：集成AI自动审核图片与评论功能，并支持人工复核

## 技术栈

- **前端框架**: Vue 3
- **UI 组件库**: Element Plus
- **状态管理**: Vuex 4
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **构建工具**: Vite

## 项目结构

```
frontend-admin/
├── public/                # 静态资源
├── src/                   # 源代码
│   ├── assets/            # 资源文件
│   ├── components/        # 组件
│   │   ├── Header.vue     # 页头组件
│   │   ├── Sidebar.vue    # 侧边栏组件
│   │   └── ...            # 其他组件
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── store/             # Vuex 状态管理
│   │   └── index.js       # 状态定义
│   ├── views/             # 页面视图
│   │   ├── Login.vue      # 登录页
│   │   ├── Dashboard.vue  # 仪表盘页
│   │   ├── Posts.vue      # 帖子管理页
│   │   ├── Images.vue     # 图片管理页
│   │   ├── Comments.vue   # 评论管理页
│   │   └── ...            # 其他页面
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── index.html             # HTML 模板
├── package.json           # 项目依赖
└── vite.config.js         # Vite 配置
```

## 环境要求

- Node.js >= 16.0.0
- npm >= 7.0.0

## 安装与运行

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

创建 `.env.development` 或 `.env.production` 文件：

```env
VUE_APP_API_BASE_URL=http://localhost:5001  # 管理后台后端API基础URL
```

### 3. 运行开发服务器

```bash
npm run serve
```

### 4. 构建生产版本

```bash
npm run build
```

## 端口说明

- 开发服务器运行在 `http://localhost:8080`
- API 请求会自动代理到后端服务器 `http://localhost:5001`

## API 接口使用说明

管理后台前端通过以下 API 接口与后端交互：

### 1. 管理员登录

```javascript
// 示例代码
async login() {
  try {
    const response = await axios.post('/api/admin/login', {
      username: this.username,
      password: this.password
    });
    localStorage.setItem('admin-token', response.data.token);
    this.$router.push('/dashboard');
  } catch (error) {
    console.error('登录失败:', error);
  }
}
```

### 2. 帖子管理

```javascript
// 获取所有帖子
async fetchPosts() {
  const token = localStorage.getItem('admin-token');
  const response = await axios.get('/api/admin/posts', {
    headers: { Authorization: `Bearer ${token}` }
  });
  this.posts = response.data.posts;
}

// 更新帖子
async updatePost(postId, postData) {
  const token = localStorage.getItem('admin-token');
  await axios.put(`/api/admin/posts/${postId}`, postData, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

// 删除帖子
async deletePost(postId) {
  const token = localStorage.getItem('admin-token');
  await axios.delete(`/api/admin/posts/${postId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}
```

### 3. 图片管理

```javascript
// 获取所有图片
async fetchImages() {
  const token = localStorage.getItem('admin-token');
  const response = await axios.get('/api/admin/images', {
    headers: { Authorization: `Bearer ${token}` }
  });
  this.images = response.data.images;
}

// 上传图片
async uploadImage(file, postId) {
  const token = localStorage.getItem('admin-token');
  const formData = new FormData();
  formData.append('file', file);
  formData.append('post_id', postId);
  
  await axios.post('/api/admin/images', formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
}

// 删除图片
async deleteImage(imageId) {
  const token = localStorage.getItem('admin-token');
  await axios.delete(`/api/admin/images/${imageId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}
```

### 4. 评论管理

```javascript
// 获取所有评论
async fetchComments() {
  const token = localStorage.getItem('admin-token');
  const response = await axios.get('/api/admin/comments', {
    headers: { Authorization: `Bearer ${token}` }
  });
  this.comments = response.data.comments;
}

// 删除评论
async deleteComment(commentId) {
  const token = localStorage.getItem('admin-token');
  await axios.delete(`/api/admin/comments/${commentId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}
```

## 生产部署

### 1. 构建项目

```bash
npm run build
```

构建后的文件将生成在 `dist` 目录中。

### 2. 配置 Nginx

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

### 3. 配置 HTTPS (推荐)

使用 Certbot 获取 SSL 证书：

```bash
sudo certbot --nginx -d admin.your-domain.com
```

## 许可证

[MIT License](../LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。
