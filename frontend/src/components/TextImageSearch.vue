<template>
  <el-container class="text-search-page">
    <!-- 顶部导航 -->
    <el-header class="header-bar">
      <div class="logo">AIFrameQuest</div>
      <el-link href="/" class="nav-link" type="primary">首页</el-link>
    </el-header>

    <el-main class="main-content">
      <el-row justify="center">
        <el-col :span="20">
          <div class="search-container">
            <h2>文字搜图-BETA</h2>
            <p class="description">输入描述文字，搜索相关图片</p>
            
            <el-input
              v-model="searchQuery"
              placeholder="请输入描述文字，例如：一只可爱的猫"
              class="search-input"
              clearable
              @keyup.enter="startSearch"
            >
              <template #append>
                <el-button @click="startSearch" :loading="loading">
                  <el-icon><Search /></el-icon>
                  搜索
                </el-button>
              </template>
            </el-input>
            
            <div class="search-tips">
              <p>搜索提示：</p>
              <ul>
                <li>使用简洁明了的描述</li>
                <li>可以尝试描述图片的主体、颜色、场景等</li>
                <li>例如："蓝天下的樱花树"、"奔跑的黑色小狗"</li>
              </ul>
            </div>
            <div class="search-tips">
              <p>英雄帖：</p>
              <ul>
                <li>文字搜图模块对于描述迷因的图片和文字的匹配效果一般</li>
                <li>我们期待您能给出轻量级而效果理想的解决方案</li>
                <li>被采纳的建议将获得奖励，欢迎联系我们：aiframequest@gmail.com</li>
              </ul>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const router = useRouter()
const store = useStore()

const searchQuery = ref('')
const loading = ref(false)

const startSearch = async () => {
  if (!searchQuery.value || searchQuery.value.trim() === '') {
    ElMessage.warning('请输入搜索文字')
    return
  }
  
  loading.value = true
  
  try {
    // 发送请求到后端
    const response = await axios.post('http://127.0.0.1:5000/api/text-to-image-search', {
      query: searchQuery.value
    })
    
    console.log('搜索结果:', response.data)
    
    // 更新搜索结果到store并跳转到result页面
    if (response.data && response.data.results && response.data.results.length > 0) {
      // 将搜索结果存储到store
      store.commit('SET_SEARCH_RESULTS', response.data.results)
      store.commit('SET_UPLOADED_IMAGE', null) // 文字搜索没有上传图片
      store.commit('SET_SEARCH_QUERY', searchQuery.value)
      
      // 跳转到文字搜图专用结果页面
      router.push('/text-search-result')
    } else {
      ElMessage.warning('未找到相关图片')
    }
  } catch (error) {
    console.error('文字搜图失败:', error)
    ElMessage.error('文字搜图失败: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.text-search-page {
  min-height: 100vh;
  background: #fff;

}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  font-size: 2rem;
  color: #409eff;
  font-family: 'Pacifico', cursive;
}

.nav-link {
  font-size: 1rem;
}

.main-content {
  margin-top: 30px;
}

.search-container {
  padding: 30px;
  border-radius: 8px;
  background: transparent;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-container h2 {
  margin-top: 0;
  color: #303133;
  font-size: 24px;
}

.description {
  color: #606266;
  margin-bottom: 20px;
}

.search-input {
  margin-bottom: 20px;
}

.search-tips {
  margin-top: 30px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  color: #606266;
}

.search-tips p {
  margin-top: 0;
  font-weight: bold;
}

.search-tips ul {
  padding-left: 20px;
  margin-bottom: 0;
}

.search-tips li {
  margin-bottom: 5px;
}
</style>