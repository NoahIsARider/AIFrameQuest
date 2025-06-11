# AIFrameQuest 社区讨论平台前端

## 功能特点

- 🔐 用户注册与登录认证
- 📝 多分类内容管理（动漫、电影、电视剧、游戏等）
- 💬 评论与评分系统
- 🔍 基于 FAISS 的图像相似度搜索
- 🖼️ 静态资源服务（图片文件）
- 📊 RESTful API 设计
- 🔢 帖子浏览次数统计与显示
- ⭐ 用户评分系统
- 🖼️ 多图片轮播展示
- 🗣️ 识图问答：用户可上传图片并提问，获取智能解答
- 🔎 文字搜图（多模态）：通过文字描述精确搜索相关图片
- ✨ 图片上传申请：用户可提交图片上传请求，待管理员审核

## 技术栈

- **前端框架**: Vue 3
- **UI 组件库**: Element Plus
- **状态管理**: Vuex 4
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **构建工具**: Vite

## 环境要求

- Node.js >= 16.0.0
- npm >= 7.0.0

## 安装步骤

### 1. 克隆项目

```bash
git clone [项目地址]
cd AIFrameQuest/frontend
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

创建 `.env.development` 或 `.env.production` 文件：

```env
VITE_APP_API_BASE_URL=http://localhost:5000  # 后端API基础URL
```

### 4. 启动开发服务器

```bash
npm run dev
```

## 开发环境

- 开发服务器运行在 `http://localhost:5173`
- API 请求会自动代理到后端服务器

## 项目结构

```
frontend/
├── public/                # 静态资源
├── src/                   # 源代码
│   ├── assets/            # 资源文件
│   ├── components/        # 组件
│   │   ├── Comment.vue    # 评论组件
│   │   ├── Header.vue     # 页头组件
│   │   ├── PostCard.vue   # 帖子卡片组件
│   │   ├── PostDetail.vue # 帖子详情组件
│   │   └── ...            # 其他组件
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── store/             # Vuex 状态管理
│   │   └── index.js       # 状态定义
│   ├── views/             # 页面视图
│   │   ├── Home.vue       # 首页
│   │   ├── Login.vue      # 登录页
│   │   ├── Register.vue   # 注册页
│   │   ├── PostDetail.vue # 帖子详情页
│   │   ├── CreatePost.vue # 创建帖子页
│   │   ├── Hot.vue        # 热门帖子页
│   │   └── ...            # 其他页面
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── index.html             # HTML 模板
├── package.json           # 项目依赖
└── vite.config.js         # Vite 配置
```

## 浏览次数统计功能

浏览次数统计功能通过以下组件实现：

1. **Vuex Store**: `store/index.js` 中的 `fetchPost` action 在获取帖子详情后会调用更新浏览次数的 API
2. **帖子详情组件**: `components/PostDetail.vue` 和 `views/PostDetail.vue` 中显示帖子的浏览次数
3. **热门帖子组件**: `views/Hot.vue` 根据浏览次数排序显示热门帖子

## 生产部署

### 1. 构建生产版本

```bash
npm run build
```

构建后的文件将生成在 `dist` 目录中。

### 2. 部署到 Web 服务器

将 `dist` 目录中的文件复制到 Web 服务器的根目录或相应的子目录中。

### 3. Nginx 配置示例

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

## 常见问题

### 1. 依赖安装问题

如果安装依赖时遇到问题，可以尝试以下解决方案：

```bash
# 清除 npm 缓存
npm cache clean --force

# 使用 --legacy-peer-deps 参数安装
npm install --legacy-peer-deps
```

### 2. 图标加载问题

如果图标无法正常显示，请确保已正确安装 Element Plus 图标：

```bash
npm install @element-plus/icons-vue
```

### 3. 路由问题

如果路由无法正常工作，请检查 `vite.config.js` 中的 `base` 配置是否与部署路径一致。

### 4. 浏览次数统计问题

如果浏览次数无法正常更新，请检查：

- 前端是否正确调用了更新浏览次数的 API
- 网络请求是否成功（检查浏览器开发者工具中的网络请求）
- 后端是否正确处理了浏览次数更新请求

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

[MIT License](../LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。