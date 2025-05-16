# 社区讨论平台

一个基于 Vue 3 + Element Plus 的现代化社区讨论平台，支持多分类内容展示、用户互动等功能。

## 功能特点

- 🎯 多分类内容展示（动漫、电影、电视剧、游戏等）
- 💬 实时讨论和评论功能
- 🔍 内容搜索功能
- 👤 用户个人中心
- 📱 响应式设计，支持移动端访问

## 技术栈

- Vue 3
- Vue Router
- Vuex
- Element Plus
- Vite

## 项目设置

### 环境要求

- Node.js >= 16.0.0
- npm >= 7.0.0

### 安装步骤

1. 克隆项目
```bash
git clone [项目地址]
cd [项目目录]
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 构建生产版本
```bash
npm run build
```

### 开发环境配置

1. 确保已安装所需依赖：
```bash
npm install element-plus @element-plus/icons-vue
```

2. 在 `vite.config.js` 中配置项目：
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    open: true
  }
})
```

## 项目结构

```
src/
├── components/        # 组件目录
│   ├── Nav.vue       # 导航组件
│   ├── PostList.vue  # 帖子列表组件
│   └── ...
├── views/            # 页面目录
│   ├── Home.vue      # 首页
│   ├── Hot.vue       # 热门页面
│   └── My.vue        # 个人中心
├── router/           # 路由配置
├── store/            # 状态管理
├── assets/           # 静态资源
└── App.vue           # 根组件
```

## 使用说明

### 开发模式

1. 启动开发服务器：
```bash
npm run dev
```

2. 访问开发环境：
- 打开浏览器访问 `http://localhost:5173`

### 生产部署

1. 构建生产版本：
```bash
npm run build
```

2. 部署步骤：
- 将 `dist` 目录下的文件部署到 Web 服务器
- 配置服务器支持 HTML5 History 模式
- 确保所有路由都指向 `index.html`

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/your/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 常见问题

1. 如果遇到依赖安装问题：
```bash
npm install --legacy-peer-deps
```

2. 如果遇到图标加载问题：
- 确保已安装 `@element-plus/icons-vue`
- 检查图标名称是否正确

3. 如果遇到路由问题：
- 检查 `router.js` 配置
- 确保服务器配置支持 HTML5 History 模式

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