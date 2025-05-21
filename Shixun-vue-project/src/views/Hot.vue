<template>
  <div class="hot-container">
    <!-- 顶部标签页 -->
    <el-tabs v-model="activeTab" class="category-tabs">
      <el-tab-pane label="全部" name="all">
        <div class="content-wrapper">
          <div class="main-content">
            <el-row :gutter="20">
              <el-col :span="24" v-for="post in filteredPosts" :key="post.id">
                <el-card class="post-card">
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
                    <el-button type="text">
                      <el-icon><Star /></el-icon>
                      收藏 {{ post.favorites }}
                    </el-button>
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
      <el-tab-pane label="动漫" name="anime"></el-tab-pane>
      <el-tab-pane label="电影" name="movie"></el-tab-pane>
      <el-tab-pane label="电视剧" name="tv"></el-tab-pane>
      <el-tab-pane label="游戏" name="game"></el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { 
  View, 
  ChatDotRound, 
  Star, 
  VideoCamera, 
  Film, 
  Monitor, 
  VideoPlay 
} from '@element-plus/icons-vue';

const activeTab = ref('all');
const activeCategory = ref('anime');

// 模拟数据
const posts = ref([
  {
    id: 1,
    title: '《进击的巨人》最终季讨论',
    content: '大家觉得最终季的结局如何？',
    author: '动漫迷',
    authorAvatar: '',
    category: '动漫',
    date: '2024-03-20',
    views: 1234,
    comments: 56,
    favorites: 78
  },
  {
    id: 2,
    title: '《奥本海默》观后感',
    content: '诺兰导演的又一力作，大家觉得如何？',
    author: '电影爱好者',
    authorAvatar: '',
    category: '电影',
    date: '2024-03-19',
    views: 2345,
    comments: 67,
    favorites: 89
  },
  {
    id: 3,
    title: '《三体》电视剧版评价',
    content: '大家觉得电视剧版改编得如何？',
    author: '科幻迷',
    authorAvatar: '',
    category: '电视剧',
    date: '2024-03-18',
    views: 3456,
    comments: 78,
    favorites: 90
  },
  {
    id: 4,
    title: '《艾尔登法环》DLC讨论',
    content: '新DLC的难度如何？',
    author: '游戏玩家',
    authorAvatar: '',
    category: '游戏',
    date: '2024-03-17',
    views: 4567,
    comments: 89,
    favorites: 101
  }
]);

const hotTopics = ref([
  { id: 1, title: '《海贼王》最新话讨论', category: '动漫' },
  { id: 2, title: '《沙丘2》观影体验', category: '电影' },
  { id: 3, title: '《三体》电视剧版评价', category: '电视剧' },
  { id: 4, title: '《艾尔登法环》DLC讨论', category: '游戏' }
]);

const filteredPosts = computed(() => {
  if (activeTab.value === 'all') return posts.value;
  return posts.value.filter(post => {
    const categoryMap = {
      'anime': '动漫',
      'movie': '电影',
      'tv': '电视剧',
      'game': '游戏'
    };
    return post.category === categoryMap[activeTab.value];
  });
});

const getTagType = (category) => {
  const typeMap = {
    '动漫': 'success',
    '电影': 'warning',
    '电视剧': 'info',
    '游戏': 'danger'
  };
  return typeMap[category] || 'info';
};

const handleCategorySelect = (index) => {
  activeCategory.value = index;
  activeTab.value = index;
};
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