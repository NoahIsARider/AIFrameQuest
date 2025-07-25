<template>
  <div class="rank-container">
    <!-- 标签页 -->
    <el-tabs v-model="activeTab" class="category-tabs">
      <!-- 浏览量排行榜 -->
      <el-tab-pane label="浏览量排行榜" name="views">
        <div class="content-wrapper">
          <div class="main-content">
            <!-- 帖子列表 -->
            <el-row :gutter="20">
              <el-col :span="24" v-for="post in sortedByViews" :key="post.id">
                <el-card class="post-card" @click="$router.push(`/post/${post.id}`)">
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
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <div class="rank-info-box">
            <p>排行榜的计算标准：以浏览次数从高到低进行排序。</p>
          </div>
        </div>
      </el-tab-pane>

      <!-- 讨论量排行榜 -->
      <el-tab-pane label="讨论量排行榜" name="comments">
        <div class="content-wrapper">
          <div class="main-content">
            <!-- 帖子列表 -->
            <el-row :gutter="20">
              <el-col :span="24" v-for="post in sortedByComments" :key="post.id">
                <el-card class="post-card" @click="$router.push(`/post/${post.id}`)">
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
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <div class="rank-info-box">
            <p>排行榜的计算标准：以评论数量从高到低进行排序。</p>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { View, ChatDotRound } from '@element-plus/icons-vue'

// 响应式数据
const activeTab = ref('views')
const posts = ref([]) // 存储所有帖子

// 获取帖子数据
async function fetchPosts() {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/posts')
    posts.value = res.data
  } catch (error) {
    console.error('获取帖子失败:', error)
    ElMessage.error('获取帖子数据失败，请稍后重试')
  }
}

onMounted(() => {
  fetchPosts()
})

// 排序后的帖子列表（按浏览量降序）
const sortedByViews = computed(() => {
  return [...posts.value].sort((a, b) => b.views - a.views)
})

// 排序后的帖子列表（按评论量降序）
const sortedByComments = computed(() => {
  return [...posts.value].sort((a, b) => b.comments - a.comments)
})

// 标签颜色映射
const getTagType = (category) => {
  const typeMap = {
    '动漫': 'success',
    '电影': 'warning',
    '电视剧': 'info',
    '游戏': 'danger',
    '迷因': 'primary'
  }
  return typeMap[category] || 'info'
}
</script>

<style scoped>
.rank-container {
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
  flex: 3;
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
.rank-info-box {
  flex: 1;
  border: 2px #2c3e50;
  border-radius: 8px;
  padding: 10px;
  background-color: #f9f9f9;
  color: #2c3e50;
  font-size: 1em;
  height: fit-content;
}
</style>