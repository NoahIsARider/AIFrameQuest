<template>
  <div class="post-detail">
    <!-- 返回按钮 -->
    <div class="back-button-container">
      <el-button type="primary" @click="goBack" icon="ArrowLeft">返回</el-button>
    </div>
    
    <h2>{{ post.title }}</h2>
    
    <!-- 浏览次数和评分信息 -->
    <div class="post-meta-info">
      <span class="views-count"><el-icon><View /></el-icon> 浏览次数: {{ post.views || 0 }}</span>
    </div>
    
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
    <div class="images-section">
      <div class="images-header">
        <h3>词条图片 ({{ postImages.length }})</h3>
        <!-- 添加上传图片按钮，仅在用户登录时显示 -->
        <el-button v-if="isLoggedIn" type="primary" size="small" @click="openUploadDialog">
          <el-icon><upload-filled /></el-icon> 上传图片
        </el-button>
      </div>
      
      <!-- 使用Element Plus的Carousel组件实现轮播图 -->
      <el-carousel
        v-if="postImages.length > 0"
        :interval="4000"
        indicator-position="outside"
        arrow="always"
        :initial-index="carouselIndex"
        @change="handleCarouselChange"
      >
        <el-carousel-item v-for="(chunk, index) in imageChunks" :key="index">
          <div class="image-row">
            <div v-for="image in chunk" :key="image.id" class="image-item">
              <el-image 
                :src="image.url" 
                fit="cover"
                :preview-src-list="imageUrls"
                :initial-index="getImageIndex(image)"
                preview-teleported
              />
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
      
      <el-empty v-else description="暂无图片" />
      
      <!-- 图片上传对话框 -->
      <el-dialog
        v-model="uploadDialogVisible"
        title="上传图片到词条"
        width="30%"
      >
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :limit="1"
          :file-list="fileList"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              请上传jpg/png格式的图片文件，文件大小不超过2MB
            </div>
          </template>
        </el-upload>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="uploadDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitUpload" :loading="uploading">
              上传
            </el-button>
          </span>
        </template>
      </el-dialog>
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
            <span class="comment-author">{{ decodeURIComponent(comment.author) }}</span>
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
import { ref, onMounted, computed, watch } from 'vue';
import { View } from '@element-plus/icons-vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElRate, ElMessage, ElAlert, ElCarousel, ElCarouselItem } from 'element-plus';
import { ArrowLeft, UploadFilled } from '@element-plus/icons-vue';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const store = useStore();
const post = ref({});
const comments = ref([]);
const submitting = ref(false);
const postImages = ref([]);
const carouselIndex = ref(0); // 当前轮播图索引

// 图片上传相关变量
const uploadDialogVisible = ref(false);
const fileList = ref([]);
const selectedFile = ref(null);
const uploading = ref(false);

// 处理轮播图切换事件
const handleCarouselChange = (index) => {
  carouselIndex.value = index;
};

// 获取所有图片URL用于预览
const imageUrls = computed(() => {
  return postImages.value.map(img => img.url);
});

// 将图片分组，每组三张
const imageChunks = computed(() => {
  const chunks = [];
  const images = [...postImages.value];
  
  for (let i = 0; i < images.length; i += 3) {
    chunks.push(images.slice(i, i + 3));
  }
  
  return chunks;
});

// 获取图片在预览列表中的索引
const getImageIndex = (image) => {
  return postImages.value.findIndex(img => img.id === image.id);
};

// 检查用户是否登录
const isLoggedIn = computed(() => {
  return store.state.token && store.state.token !== '';
});

// 获取当前用户名（作为计算属性，确保实时更新）
const username = computed(() => {
  return store.state.username ? decodeURIComponent(store.state.username) : '';
});

// 打开上传对话框
const openUploadDialog = () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录后再上传图片');
    return;
  }
  uploadDialogVisible.value = true;
  fileList.value = [];
  selectedFile.value = null;
};

// 处理文件变化
const handleFileChange = (file) => {
  // 检查文件类型
  const isImage = file.raw.type.startsWith('image/');
  if (!isImage) {
    ElMessage.error('只能上传图片文件!');
    fileList.value = [];
    return;
  }
  
  // 检查文件大小（限制为2MB）
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!');
    fileList.value = [];
    return;
  }
  
  selectedFile.value = file.raw;
};

// 处理文件移除
const handleFileRemove = () => {
  selectedFile.value = null;
  fileList.value = [];
};

// 提交上传
const submitUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择要上传的图片');
    return;
  }
  
  uploading.value = true;
  
  try {
    // 创建FormData对象
    const formData = new FormData();
    formData.append('file', selectedFile.value);
    
    // 设置请求头
    const headers = {};
    if (store.state.token) {
      headers['Authorization'] = store.state.token;
    }
    
    // 发送请求到后端
    const response = await axios.post(
      `http://127.0.0.1:5000/api/posts/${route.params.id}/upload-image`,
      formData,
      { headers }
    );
    
    console.log('上传响应:', response.data);
    
    if (response.data.status === 'success') {
      ElMessage.success('图片上传成功，等待管理员审核');
      uploadDialogVisible.value = false;
      fileList.value = [];
      selectedFile.value = null;
    } else {
      ElMessage.error(response.data.message || '上传失败');
    }
  } catch (error) {
    console.error('上传图片失败:', error);
    ElMessage.error('上传图片失败: ' + (error.response?.data?.message || error.message));
  } finally {
    uploading.value = false;
  }
};

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
    
    // 设置评论者姓名和日期 - 使用计算属性获取最新的username
    newComment.value.name = username.value || '匿名用户';
    
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
    newComment.value.rating = 10;
    
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

const updatePostViews = async () => {
  try {
    const postId = route.params.id; // 从路由参数中获取帖子 ID
    const response = await axios.post(`/api/posts/${postId}/views`);
    console.log('浏览次数更新成功:', response.data);
  } catch (error) {
    console.error('浏览次数更新失败:', error);
  }
};


onMounted(async () => {
  try {
    // 获取帖子详情
    await store.dispatch('fetchPost', route.params.id);
    post.value = store.state.currentPost;
    
    // 获取评论
    await store.dispatch('fetchComments', route.params.id);
    comments.value = store.state.comments;

    // 监听storage事件
    window.addEventListener('storage', async (event) => {
      if (event.key === 'token' || event.key === 'username') {
        // 当token或username变化时，重新获取帖子详情和评论
        await store.dispatch('fetchPost', route.params.id);
        post.value = store.state.currentPost;
        
        await store.dispatch('fetchComments', route.params.id);
        comments.value = store.state.comments;
      }
    });
    // 页面加载时调用更新浏览次数的接口
    updatePostViews();
    // 监听token变化
    watch(() => store.state.token, async (newToken) => {
      if (newToken) {
        // 当token变化时，重新获取帖子详情和评论
        await store.dispatch('fetchPost', route.params.id);
        post.value = store.state.currentPost;
        
        await store.dispatch('fetchComments', route.params.id);
        comments.value = store.state.comments;
      }
    });
    
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

/* 浏览次数样式 */
.post-meta-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  color: #606266;
  font-size: 14px;
}

.views-count {
  display: flex;
  align-items: center;
  gap: 5px;
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

.images-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.images-section h3 {
  margin-bottom: 0;
  font-size: 18px;
  color: #303133;
}

/* 上传对话框样式 */
.upload-demo {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

/* 轮播图样式 */
.image-row {
  display: flex;
  justify-content: center;
  gap: 15px;
  height: 100%;
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

/* 自定义轮播图样式 */
:deep(.el-carousel__indicators) {
  margin-top: -20px;
  bottom: 10px;
}

:deep(.el-carousel__item) {
  display: flex;
  justify-content: center;
  align-items: center;
}

:deep(.el-carousel__button) {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #dcdfe6;
}

:deep(.el-carousel__indicator.is-active .el-carousel__button) {
  background-color: #409EFF;
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