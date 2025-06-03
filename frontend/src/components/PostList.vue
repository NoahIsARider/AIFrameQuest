<template>
  <div class="post-list">
    <div class="welcome-section">
      <div class="welcome-card">
        <div class="welcome-header">
          <h1>欢迎来到AIFrameQuest社区</h1>
        </div>
        <div class="welcome-content">
          <p class="welcome-text">在这里，我们探索与符号的共存可能</p>
        </div>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="24">
        <!-- <el-carousel :interval="4000" type="card" height="400px" class="carousel-container">
          <el-carousel-item v-for="(image, index) in carouselImages" :key="index">
            <img :src="image" class="carousel-image" />
          </el-carousel-item>
        </el-carousel> -->
        <el-carousel :interval="4000" type="card" height="400px" class="carousel-container">
          <el-carousel-item
            v-for="(image, index) in carouselImages"
            :key="index"
            @click="openImageDialog(image, index)"
          >
            <img :src="image" class="carousel-image" />
          </el-carousel-item>
        </el-carousel>
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      width="50%"
      :close-on-click-modal="false"
      :destroy-on-close="true"
      class="image-dialog"
    >
      <template #title>
        <span>AIFrameQuest拟像社区</span>
      </template>
      <div class="dialog-content">
        <img :src="selectedImage" alt="轮播图片" class="dialog-image" />
        <p class="dialog-text">{{ selectedMessage }}</p>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

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

// 轮播图片数组
const carouselImages = ref([
  '/src/assets/images/slide1.jpg',
  '/src/assets/images/slide2.jpg',
  '/src/assets/images/slide3.jpg',
]);

const store = useStore();
const posts = ref([]);
const searchQuery = ref('');
const dialogVisible = ref(false); // 控制对话框显示
const selectedImage = ref(''); // 当前选中的图片 URL
const selectedMessage = ref(''); // 当前选中的图片文字描述

const openImageDialog = (image, index) => {
  const messages = [
    '德勒兹的影像理论打破了传统影像理论所建构的既定藩篱，从感知发生的维度、运动绵延和纯粹时间的角度，松动了传统电影理论所建立的稳定的边界，让我们重新理解了影像生成向度上的敞开性与多样性。 德勒兹提出了“物质即影像”的概念，颠覆了传统电影理论中将影像作为再现客观世界的艺术形式这一核心思维。“在德勒兹那里，只有一个存在具有绝对的优先性，除了这个大写的一的存在之外，任何其他的存在物不过是对大写的一的拟像，而德勒兹进一步指出，所有的拟像在等级上是完全平等的，不存在谁优先于谁的问题，既不存在主体优先于对象，也不存在对象优先于主体，因此，德勒兹借助这种方式的同时否定了主体主义和客观主义的真理形式。',
    '流行音乐在数字时代日益成为拟像迷因的载体。其旋律、歌词乃至歌手形象皆可脱离原始语境，被截取、复制、重组为社交媒体的碎片化符号。洗脑副歌与病毒式舞蹈挑战通过算法加速传播，在无限复制的过程中逐渐剥离情感内核，演变为纯粹的文化快消品。这种循环再生产模糊了真实与模仿的边界，音乐本体退居其次，其衍生的符号狂欢成为主导——听众消费的不再是艺术表达，而是被流量赋能的拟像符号，在集体无意识的搬运中完成文化意义的真空循环。',
    '拟像论则是让·鲍德里亚在《拟像与仿真》（1981年）一书中提出的理论。他认为，后现代社会中，拟像的出现使得过去的索绪尔符号学理论中的“所指”已经消失，世界已经由“没有所指的能指”构成，这些符号或者拟像没有根基，只是自我指涉。它不但将不在场的显示为在场，将想像塑造成真实，更破坏一切与“真实”之间的联系，将“真实”吸纳到自身当中，使“真实”与“非真实”之间的区别已经没有意义，也就是鲍德里亚所说的“超真实”。',
  ];

  selectedImage.value = image;
  selectedMessage.value = messages[index] || '暂无描述';
  dialogVisible.value = true;
};
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
  padding: 0;
}

.welcome-section {
  margin-bottom: 30px;
  width: 100%;
}

.welcome-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  padding: 20px;
}

.welcome-header {
  text-align: center;
  padding: 20px 0;
}

.welcome-header h1 {
  margin: 0;
  font-size: 28px;
  color: #0f4478;
  font-weight: 600;
  line-height: 1.4;
}

.welcome-content {
  text-align: center;
  padding: 20px 40px 30px;
}

.welcome-text {
  font-size: 16px;
  color: #606266;
  margin: 0;
  line-height: 1.6;
}

.carousel-container {
  margin-bottom: 30px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

/* 自定义轮播样式 */
:deep(.el-carousel__item) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-carousel__item--card) {
  border-radius: 8px;
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

.image-dialog .dialog-content {
  text-align: center;
}

.image-dialog .dialog-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 20px;
}

.image-dialog .dialog-text {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
}
</style>