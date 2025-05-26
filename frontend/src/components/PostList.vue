<template>
  <div class="post-list">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎来到AIFrameQuest拟像社区</h2>
            </div>
          </template>
          <!-- <el-input
            v-model="searchQuery"
            placeholder="搜索文章..."
            class="search-input"
            :prefix-icon="Search"
          /> -->
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="post-grid">
      <el-col :xs="24" :sm="12" :md="8" v-for="post in filteredPosts" :key="post.id">
        <el-card class="post-card" :body-style="{ padding: '0px' }">
          <img 
            :src="getCoverUrl(post.cover) || 'https://via.placeholder.com/300x200'" 
            class="post-image"
            @error="handleImageError"
          >
          <div class="post-content">
            <h3 class="post-title">
              <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
            </h3>
            <p class="post-summary">{{ post.content }}</p>
            <div class="post-meta">
              <el-avatar :size="24" :src="post.authorAvatar">{{ post.title.charAt(0) }}</el-avatar>
              <span class="author-name" v-if="post.author">{{ post.author }}</span>
              <el-tag size="small" type="info">{{ post.date }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="filteredPosts.length === 0" description="暂无文章" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const store = useStore();
const posts = ref([]);
const searchQuery = ref('');

// 处理封面图片URL
const getCoverUrl = (coverPath) => {
  if (!coverPath) return null;
  
  // 从路径中提取文件名
  let filename = coverPath;
  
  // 移除可能的前缀路径
  if (filename.includes('backend/images/')) {
    filename = filename.replace('backend/images/', '');
  } else if (filename.includes('backend\\images\\')) {
    filename = filename.replace('backend\\images\\', '');
  }
  
  // 对文件名进行编码
  const encodedFilename = encodeURIComponent(filename);
  
  // 构建完整URL
  const imageUrl = `http://127.0.0.1:5000/images/${encodedFilename}`;
  console.log('Image URL:', imageUrl);
  return imageUrl;
};

// 处理图片加载错误
const handleImageError = (e) => {
  console.error('图片加载失败:', e);
  e.target.src = 'https://via.placeholder.com/300x200';
};

const filteredPosts = computed(() => {
  if (!searchQuery.value) return posts.value;
  return posts.value.filter(post => 
    post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (post.content && post.content.toLowerCase().includes(searchQuery.value.toLowerCase()))
  );
});

onMounted(async () => {
  try {
    await store.dispatch('fetchPosts');
    posts.value = store.state.posts;
    console.log('获取到的帖子数据:', posts.value);
  } catch (error) {
    console.error('获取帖子失败:', error);
    ElMessage.error('获取帖子数据失败，请稍后重试');
  }
});
</script>

<style scoped>
.post-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  margin-bottom: 20px;
}

.post-grid {
  margin-top: 20px;
}

.post-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.post-card:hover {
  transform: translateY(-5px);
}

.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.post-content {
  padding: 15px;
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 1.2em;
}

.post-title a {
  color: #303133;
  text-decoration: none;
}

.post-title a:hover {
  color: #409EFF;
}

.post-summary {
  color: #606266;
  margin: 10px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.author-name {
  color: #606266;
  font-size: 0.9em;
}
</style>