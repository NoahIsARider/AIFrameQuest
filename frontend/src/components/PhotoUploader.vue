<template>
  <el-container class="my-page">
    <!-- 顶部导航 -->
    <el-header class="header-bar">
      <div class="logo">AIFrameQuest</div>
      <el-link href="/" class="nav-link" type="primary">首页</el-link>
    </el-header>

    <el-main class="main-content">
      <el-row justify="center">
        <el-col :span="20">
          <el-upload
            class="upload-area"
            drag
            action="#"
            :show-file-list="true"
            :on-change="handleChange"
            :on-remove="handleRemove"
            :auto-upload="false"
            :limit="1"
            :file-list="fileList"
          >
            <template v-if="!uploadedImage">
              <el-icon class="upload-icon"><upload-filled /></el-icon>
              <div class="el-upload__text">拖拽图片到这里或</div>
              <el-button type="primary">选择图片</el-button>
            </template>
            
            <!-- 上传图片预览区域 -->
            <div v-else class="preview-container">
              <h3>预览图片</h3>
              <el-image 
                :src="uploadedImage" 
                fit="contain"
                :preview-src-list="[uploadedImage]"
                :initial-index="0"
                class="preview-image"
                preview-teleported
              />
            </div>
          </el-upload>
          
          <div class="button-container">
            <el-button type="success" @click="startSearch" :loading="loading">开始识别</el-button>
          </div>
        </el-col>
      </el-row>
      
      <!-- 搜索结果将在result页面显示，这里移除搜索结果展示区域 -->
    </el-main>
    
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { UploadFilled, Cpu } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const router = useRouter()
const store = useStore()

const fileList = ref<UploadUserFile[]>([])
const selectedFile = ref(null)
const uploadedImage = ref('')
const loading = ref(false)
const searchResults = ref([])

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  console.log(file, uploadFiles)
  selectedFile.value = null
  uploadedImage.value = ''
  fileList.value = []
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
  ElMessage.warning(
    `最多只能上传1张图片，您选择了${files.length}张图片，总共${files.length + uploadFiles.length}张`
  )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
  return ElMessageBox.confirm(
    `确定要移除 ${uploadFile.name} 吗?`
  ).then(
    () => true,
    () => false
  )
}

const historyImages = ref([
  'https://img1.example.com/1.jpg',
  'https://img2.example.com/2.jpg'
])

const handleChange = (file) => {
  // 保存选中的文件
  selectedFile.value = file.raw
  // 创建预览URL
  uploadedImage.value = URL.createObjectURL(file.raw)
  console.log('上传的文件:', file);
}

// 获取图片URL
const getImageUrl = (imageName) => {
  // 根据后端图片存储路径构建URL
  return `http://127.0.0.1:5000/images/${imageName}`
}

// 查看词条详情
const viewEntryDetail = (entryId) => {
  if (!entryId) return
  
  // 使用 Vue Router 导航到词条详情页
  router.push(`/post/${entryId}`)
}

const startSearch = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择一张图片')
    return
  }
  
  loading.value = true
  searchResults.value = []
  
  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    // 发送请求到后端
    const response = await axios.post('http://127.0.0.1:5000/api/image-search', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    console.log('搜索结果:', response.data)
    
    // 更新搜索结果到store并跳转到result页面
    if (response.data && response.data.results) {
      // 将搜索结果存储到store
      store.commit('SET_SEARCH_RESULTS', response.data.results)
      store.commit('SET_UPLOADED_IMAGE', uploadedImage.value)
      store.commit('SET_SEARCH_QUERY', '图片搜索')
      
      // 跳转到result页面
      router.push('/result')
    } else {
      ElMessage.warning('未找到相似图片')
    }
  } catch (error) {
    console.error('图片搜索失败:', error)
    ElMessage.error('图片搜索失败: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.my-page {
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
.upload-area {
  width: 100%;
  min-height: 300px;
  border: 2px dashed #d9d9d9;
  background: #fafbfc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-sizing: border-box;
}
.upload-icon {
  font-size: 48px;
  color: #a0cfff;
  margin-bottom: 16px;
}
.progress-bar {
  margin-top: 20px;
}
.progress-tip {
  display: flex;
  align-items: center;
  color: #409eff;
  margin-top: 8px;
}
.progress-tip .el-icon {
  margin-right: 8px;
}
.history-card {
  min-height: 300px;
  background: #fafbfc;
}
.history-img {
  margin-bottom: 10px;
}
.history-img .el-image {
  width: 100%;
  height: 60px;
  border-radius: 6px;
  object-fit: cover;
}

.result-card {
  margin-top: 20px;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 18px;
}

.search-results {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.query-image-container {
  margin-bottom: 20px;
}

.result-list {
  margin-top: 10px;
}

.result-item {
  margin-bottom: 15px;
  transition: transform 0.3s;
}

.result-item:hover {
  transform: translateY(-5px);
}

.result-info {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.preview-container {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.preview-image {
  width: 100%;
  height: 400px;
  object-fit: contain;
  border-radius: 8px;
  cursor: pointer;
  background-color: #fafbfc;
}

.query-preview-image {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
  cursor: pointer;
}

.result-preview-image {
  width: 100%;
  height: 200px;
  border-radius: 4px;
  cursor: pointer;
}

/* 添加预览模式样式 */
:deep(.el-image-viewer__wrapper) {
  z-index: 2050;
}

:deep(.el-image-viewer__img) {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* 词条信息样式 */
.entry-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.entry-title {
  margin: 5px 0;
  color: #303133;
  font-weight: bold;
}

.entry-type {
  color: #909399;
  font-size: 12px;
  margin-bottom: 5px;
}

.entry-desc {
  margin-bottom: 10px;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.view-entry-btn {
  margin-top: 5px;
  width: 100%;
}
</style>