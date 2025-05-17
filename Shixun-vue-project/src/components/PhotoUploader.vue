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
            :auto-upload="false"
          >
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <div class="el-upload__text">拖拽图片到这里或</div>
            
            <el-button type="primary">选择图片</el-button>
            
          </el-upload>
          <el-button type="success" @click="goToResult">开始识别</el-button>
        </el-col>
      </el-row>
    </el-main>
    
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { UploadFilled, Cpu } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const fileList = ref<UploadUserFile[]>([

])

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  console.log(file, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
  ElMessage.warning(
    `The limit is 3, you selected ${files.length} files this time, add up to ${
      files.length + uploadFiles.length
    } totally`
  )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
  return ElMessageBox.confirm(
    `Cancel the transfer of ${uploadFile.name} ?`
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
  // 这里可以处理图片上传逻辑
  // file.raw 为原始文件对象
  console.log('上传的文件:', file);
}

const goToResult = () => {
  // 这里可以先调用AI识别API，识别完成后跳转
  router.push('/result')
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
</style>