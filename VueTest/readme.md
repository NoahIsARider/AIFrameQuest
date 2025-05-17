# Vue + Flask 前后端联通示例

## 项目结构

本项目展示了如何使用Vue 3前端框架与Flask后端框架进行数据交互。项目包含以下主要部分：

### 后端 (backend)
- `app.py`: 主要的Flask应用文件
- `utils/data_utils.py`: 数据处理工具函数
- `data/sample_data.json`: 示例数据文件

### 前端 (frontend)
- `src/views/DataView.vue`: 数据展示页面
- `src/router.js`: 路由配置文件
- `src/components/Nav.vue`: 导航组件

## 实现步骤

### 1. 创建数据文件
在`backend/data`目录下创建`sample_data.json`文件，包含示例数据：
```json
{
    "items": [
        {
            "id": 1,
            "name": "示例项目1",
            "description": "这是一个示例项目描述",
            "status": "进行中"
        },
        {
            "id": 2,
            "name": "示例项目2",
            "description": "另一个示例项目",
            "status": "已完成"
        }
    ]
}
```

### 2. 创建数据处理工具
在`backend/utils`目录下创建`data_utils.py`，包含数据读取逻辑：
```python
def get_json_data():
    """读取JSON文件并返回数据"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'data', 'sample_data.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error reading JSON file: {str(e)}")
```

### 3. 配置Flask API
在`app.py`中配置API端点：
```python
from flask import Flask, jsonify
from utils.data_utils import get_json_data

app = Flask(__name__)

@app.route('/api/get-data', methods=['GET'])
def get_data():
    try:
        data = get_json_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 4. 创建前端页面
在`frontend/src/views`目录下创建`DataView.vue`：
```vue
<template>
  <div class="data-view">
    <h1>数据展示页面</h1>
    <div class="data-container">
      <div v-for="item in items" :key="item.id" class="item-card">
        <h3>{{ item.name }}</h3>
        <p>{{ item.description }}</p>
        <span class="status" :class="item.status === '进行中' ? 'in-progress' : 'completed'">
          {{ item.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: []
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:5000/api/get-data')
        this.items = response.data.items
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }
  }
}
</script>
```

### 5. 配置路由
在`frontend/src/router.js`中添加新路由：
```javascript
import DataView from './views/DataView.vue'

const routes = [
  // ...其他路由
  {
    path: '/data',
    name: 'Data',
    component: DataView
  }
]
```

## 运行项目

1. 启动后端服务器
```bash
cd backend
python app.py
```

2. 启动前端开发服务器
```bash
cd frontend
npm install
npm run serve
```

3. 访问页面
- 前端页面: http://localhost:8080
- 数据页面: http://localhost:8080/data
- 后端API: http://localhost:5000/api/get-data

## 注意事项

1. 确保后端服务器正常运行
2. 如果遇到跨域问题，可以安装flask-cors
   ```bash
   pip install flask-cors
   ```
3. 确保前端axios请求的URL正确指向后端API地址
