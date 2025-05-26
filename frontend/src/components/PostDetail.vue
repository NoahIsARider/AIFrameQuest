<template>
  <div class="post-detail">
    <!-- 返回按钮 -->
    <div class="back-button-container">
      <el-button type="primary" @click="goBack" icon="ArrowLeft">返回</el-button>
    </div>
    
    <h2>{{ post.title }}</h2>
    
    <!-- 评分信息 -->
    <div class="rating-section" v-if="post.avg_rating || post.avg_rating === 0">
      <div class="rating-header">
        <span class="rating-score">{{ post.avg_rating }}</span>
        <el-rate v-model="post.avg_rating" disabled show-score :max="10" />
        <span class="rating-count">({{ post.rating_count }} 人评分)</span>
      </div>
    </div>
    
    <!-- 描述信息 -->
    <div class="description-section" v-if="post.description && post.description.length">
      <div v-for="(desc, index) in post.description" :key="index" class="description-item">
        {{ desc }}
      </div>
    </div>
    
    <!-- 图片展示区域 -->
    <div class="images-section" v-if="postImages.length > 0">
      <h3>词条图片 ({{ postImages.length }})</h3>
      <div class="image-gallery">
        <div v-for="image in postImages" :key="image.id" class="image-item">
          <el-image 
            :src="image.url" 
            fit="cover"
            :preview-src-list="imageUrls"
            :initial-index="getImageIndex(image)"
          />
        </div>
      </div>
    </div>
    
    <!-- 添加评论表单 -->
    <div class="add-comment-section">
      <h3>添加评论</h3>
      <div v-if="!isLoggedIn" class="login-tip">
        <el-alert
          title="请先登录后再评论"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <p>登录后可以发表评论和评分</p>
          </template>
        </el-alert>
      </div>
      <div v-else class="comment-form">
        <div class="form-group">
          <label>评分</label>
          <el-rate v-model="newComment.rating" :max="10" show-score />
        </div>
        <div class="form-group">
          <label>评论内容</label>
          <el-input
            v-model="newComment.text"
            type="textarea"
            :rows="4"
            placeholder="请输入您的评论..."
          />
        </div>
        <el-button type="primary" @click="submitComment" :loading="submitting">提交评论</el-button>
      </div>
    </div>
    
    <!-- 评论区 -->
    <div class="comments-section">
      <h3>评论 ({{ comments.length }})</h3>
      <div v-if="comments.length === 0" class="no-comments">
        暂无评论
      </div>
      <div v-else class="comment-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-author">{{ comment.author }}</span>
            <span class="comment-date">{{ comment.date }}</span>
            <div class="comment-rating" v-if="comment.rating">
              <el-rate v-model="comment.rating" disabled show-score :max="10" />
            </div>
          </div>
          <div class="comment-content">
            {{ comment.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElRate, ElMessage, ElAlert } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();
const store = useStore();
const post = ref({});
const comments = ref([]);
const submitting = ref(false);
const postImages = ref([]);

// 获取所有图片URL用于预览
const imageUrls = computed(() => {
  return postImages.value.map(img => img.url);
});

// 获取图片在预览列表中的索引
const getImageIndex = (image) => {
  return postImages.value.findIndex(img => img.id === image.id);
};

// 检查用户是否登录
const isLoggedIn = computed(() => {
  return store.state.token && store.state.token !== '';
});

// 新评论表单数据
const newComment = ref({
  text: '',
  rating: 10,
  name: '',
  date: ''
});

// 提交评论
const submitComment = async () => {
  if (!newComment.value.text) {
    ElMessage.warning('请输入评论内容');
    return;
  }
  
  try {
    submitting.value = true;
    
    // 设置评论者姓名和日期
    newComment.value.name = store.state.username || '匿名用户';
    
    // 设置当前日期
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    newComment.value.date = `${year}-${month}-${day}`;
    
    // 提交评论
    const response = await store.dispatch('addComment', {
      postId: route.params.id,
      comment: newComment.value
    });
    
    // 重新获取帖子详情和评论
    await store.dispatch('fetchPost', route.params.id);
    post.value = store.state.currentPost;
    
    await store.dispatch('fetchComments', route.params.id);
    comments.value = store.state.comments;
    
    // 重置表单
    newComment.value.text = '';
    newComment.value.rating = 5;
    
    // 显示后端返回的消息
    ElMessage.success(response.message || '评论提交成功');
  } catch (error) {
    console.error('提交评论失败:', error);
    ElMessage.error('提交评论失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
};

// 返回功能
const goBack = () => {
  // 检查是否有搜索结果，如果有则返回result页面，否则返回上一页
  // if (store.state.searchResults && store.state.searchResults.length > 0) {
  //   router.push('/result');
  // } else {
    router.go(-1);
  // }
};

onMounted(async () => {
  try {
    // 获取帖子详情
    await store.dispatch('fetchPost', route.params.id);
    post.value = store.state.currentPost;
    
    // 获取评论
    await store.dispatch('fetchComments', route.params.id);
    comments.value = store.state.comments;
    
    // 获取帖子相关图片
    await store.dispatch('fetchPostImages', route.params.id);
    postImages.value = store.state.postImages;
    
    console.log('帖子详情:', post.value);
    console.log('评论数据:', comments.value);
    console.log('图片数据:', postImages.value);
  } catch (error) {
    console.error('获取帖子详情失败:', error);
    ElMessage.error('获取帖子详情失败，请稍后重试');
  }
});
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 返回按钮样式 */
.back-button-container {
  margin-bottom: 20px;
}

/* 标题样式 */
h2 {
  margin-bottom: 20px;
  color: #303133;
  font-size: 24px;
}

/* 评分信息样式 */
.rating-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.rating-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rating-score {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.rating-count {
  color: #909399;
  font-size: 14px;
}

/* 描述部分样式 */
.description-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.description-item {
  margin-bottom: 10px;
  line-height: 1.6;
  color: #606266;
}

/* 图片展示区样式 */
.images-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.images-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.image-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.image-item {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.image-item .el-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 添加评论表单样式 */
.add-comment-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.add-comment-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.login-tip {
  margin-bottom: 15px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #606266;
}

/* 评论区样式 */
.comments-section {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.comments-section h3 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.no-comments {
  color: #909399;
  font-style: italic;
  padding: 10px 0;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 15px 0;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.comment-author {
  font-weight: bold;
  color: #409EFF;
}

.comment-date {
  color: #909399;
  font-size: 0.9em;
}

.comment-rating {
  margin-left: auto;
}

.comment-content {
  line-height: 1.6;
  color: #606266;
}
</style>