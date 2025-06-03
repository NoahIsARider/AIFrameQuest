<template>
  <div class="hot-container">
    <!-- 顶部标签页 -->
    <el-tabs v-model="activeTab" class="category-tabs">
      <el-tab-pane label="全部" name="all">
        <div class="content-wrapper">
          <div class="main-content">
            <!-- 帖子列表 -->
            <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card"   @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                      浏览 {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- 右侧边栏 -->
          <div class="sidebar">
            <!-- 分区导航 -->
            <el-card class="category-card">
              <template #header>
                <div class="card-header">
                  <span>分区导航</span>
                </div>
              </template>
              <el-menu
                :default-active="activeCategory"
                class="category-menu"
                @select="handleCategorySelect"
              >
                <el-menu-item index="anime">
                  <el-icon><VideoCamera /></el-icon>
                  <span>动漫</span>
                </el-menu-item>
                <el-menu-item index="movie">
                  <el-icon><Film /></el-icon>
                  <span>电影</span>
                </el-menu-item>
                <el-menu-item index="tv">
                  <el-icon><Monitor /></el-icon>
                  <span>电视剧</span>
                </el-menu-item>
                <el-menu-item index="game">
                  <el-icon><VideoPlay /></el-icon>
                  <span>游戏</span>
                </el-menu-item>
                <el-menu-item index="meme">
                  <el-icon><ChatSquare /></el-icon>
                  <span>迷因</span>
                </el-menu-item>
              </el-menu>
            </el-card>

            <!-- 热门讨论 -->
            <el-card class="hot-topics-card">
              <template #header>
                <div class="card-header">
                  <span>热门讨论</span>
                </div>
              </template>
              <div class="hot-topics">
                <div v-for="topic in hotTopics" :key="topic.id" class="topic-item">
                  <span class="topic-title">{{ topic.title }}</span>
                  <el-tag size="small" :type="getTagType(topic.category)">{{ topic.category }}</el-tag>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="动漫" name="anime">
         <!-- 帖子列表 -->
         <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card" @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                      浏览 {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                       {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
      </el-tab-pane>
      <el-tab-pane label="电影" name="movie">
        <!-- 帖子列表 -->
        <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card" @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                      浏览 {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
      </el-tab-pane>
      <el-tab-pane label="电视剧" name="tv">
        <!-- 帖子列表 -->
        <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card"  @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                       {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
      </el-tab-pane>
      <el-tab-pane label="游戏" name="game">
        <!-- 帖子列表 -->
        <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card"  @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                       {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
      </el-tab-pane>
      <el-tab-pane label="迷因" name="meme">
        <!-- 帖子列表 -->
        <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card"  @click="$router.push(`/post/${post.id}`)">  <!-- 注意跳转功能待实现 -->
                  <div class="post-header">
                    <el-avatar :size="40" :src="post.authorAvatar">{{ post.author.charAt(0) }}</el-avatar>
                    <div class="post-info">
                      <h3 class="post-title">{{ post.title }}</h3>
                      <div class="post-meta">
                        <span class="author">{{ post.author }}</span>
                        <el-tag size="small" :type="getTagType(post.category)">{{ post.category }}</el-tag>
                        <span class="time">{{ post.date }}</span>
                      </div>
                    </div>
                  </div>
                  <p class="post-content">{{ post.content }}</p>
                  <div class="post-footer">
                    <el-button type="text">
                      <el-icon><View /></el-icon>
                      浏览 {{ post.views }}
                    </el-button>
                    <el-button type="text">
                      <el-icon><ChatDotRound /></el-icon>
                      评论 {{ post.comments }}
                    </el-button>
                    <!-- <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button> -->
                  </div>
                </el-card>
              </el-col>
            </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { 
  View, 
  ChatDotRound, 
  Star, 
  VideoCamera, 
  Film, 
  Monitor, 
  VideoPlay 
} from '@element-plus/icons-vue'

// 响应式数据
const activeTab = ref('all')
const activeCategory = ref('anime')
const posts = ref([]) // 用于存储从后端获取的帖子数据

// 热门话题数据（也可以从后端获取）
const hotTopics = ref([
  { id: 1, title: '《海贼王》最新话讨论', category: '动漫' },
  { id: 2, title: '《沙丘2》观影体验', category: '电影' },
  { id: 3, title: '《三体》电视剧版评价', category: '电视剧' },
  { id: 4, title: '《艾尔登法环》DLC讨论', category: '游戏' }
])

// 从 Flask 后端获取帖子数据
async function fetchPosts() {
  try {
    console.log('开始获取帖子数据...')
    const res = await axios.get('http://127.0.0.1:5000/api/posts')
    console.log('获取到的帖子数据:', res.data)
    
    // 后端已经处理了数据格式转换，直接使用返回的数据
    posts.value = res.data
    
    // 如果需要获取单个帖子的详细信息，可以使用以下方式
    // const postDetail = await axios.get(`http://127.0.0.1:5000/api/posts/${postId}`)
    // 这将返回包含完整comments和description数组的详细信息
    
    console.log('posts.value设置后的值:', posts.value)
  } catch (error) {
    console.error('获取帖子失败:', error)
    // 显示错误提示
    ElMessage.error('获取帖子数据失败，请稍后重试')
  }
}

// 页面加载时自动获取数据
onMounted(() => {
  fetchPosts()
})

// 过滤后的帖子列表
const filteredPosts = computed(() => {
  if (activeTab.value === 'all') return posts.value
  const categoryMap = {
    'anime': '动漫',
    'movie': '电影',
    'tv': '电视剧',
    'game': '游戏',
    'meme': '迷因'
  }
  return posts.value.filter(post => post.category === categoryMap[activeTab.value])
})

// 获取标签颜色类型
const getTagType = (category) => {
  const typeMap = {
    '动漫': 'success',
    '电影': 'warning',
    '电视剧': 'info',
    '游戏': 'danger',
    '迷因':'primary'
  }
  return typeMap[category] || 'info'
}

// 分类菜单选择事件
const handleCategorySelect = (index) => {
  activeCategory.value = index
  activeTab.value = index
}
</script>



<style scoped>
.hot-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.main-content {
  flex: 1;
}

.sidebar {
  width: 300px;
}

.category-tabs {
  margin-bottom: 20px;
}

.post-card {
  margin-bottom: 20px;
}

.post-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.post-info {
  flex: 1;
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 1.2em;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #909399;
  font-size: 0.9em;
}

.post-content {
  color: #606266;
  margin: 15px 0;
  line-height: 1.6;
}

.post-footer {
  display: flex;
  gap: 20px;
  margin-top: 15px;
  border-top: 1px solid #EBEEF5;
  padding-top: 15px;
}

.category-card,
.hot-topics-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-menu {
  border-right: none;
}

.hot-topics {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.topic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #EBEEF5;
}

.topic-title {
  color: #303133;
  font-size: 0.9em;
}

.topic-item:last-child {
  border-bottom: none;
}
</style>