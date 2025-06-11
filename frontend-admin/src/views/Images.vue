<template>
  <div class="images-container">
    <div class="page-header">
      <h2>图片管理</h2>
  <div class="button-group">
    <el-button type="primary" @click="openUploadDialog">上传图片</el-button>
    <el-button type="danger" @click="triggerSimpleAction">重置图片索引</el-button>
  </div>
    </div>
    
    <!-- 图片上传对话框 -->
    <el-dialog
      title="上传图片"
      v-model="uploadDialogVisible"
      width="30%">
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="选择词条">
          <el-select v-model="uploadForm.entry_id" placeholder="选择关联词条" clearable style="width: 100%;">
            <el-option
              v-for="entry in entriesList"
              :key="entry.key"
              :label="entry.title"
              :value="entry.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="图片文件">
          <el-upload
            class="upload-demo"
            action="/api/admin/upload"
            :headers="uploadHeaders"
            :data="uploadForm"
            :show-file-list="true"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            :limit="1"
            :auto-upload="false"
            ref="uploadRef">
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload">上传</el-button>
        </span>
      </template>
    </el-dialog>

    <el-form :inline="true" class="filter-form">
      <el-form-item label="词条筛选">
        <el-select v-model="filterEntry" placeholder="选择词条" clearable style="width: 300px;">
          <el-option
            v-for="entry in entriesList"
            :key="entry.key"
            :label="entry.title"
            :value="entry.key">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <div class="images-container-wrapper">
      <div v-loading="loading" class="images-grid" v-infinite-scroll="loadMore" :infinite-scroll-disabled="loading || allLoaded" infinite-scroll-distance="10">
        <el-empty v-if="imagesList.length === 0 && !loading" description="暂无图片"></el-empty>
        <div v-else class="image-card" v-for="image in imagesList" :key="image.id">
          <div class="image-wrapper">
            <el-image 
              :src="image.url" 
              fit="cover"
              :preview-src-list="[image.url]"
              :initial-index="0"
              :preview-teleported="true"
              :z-index="3000">
              <template #error>
                <div class="image-error">
                  <el-icon><picture /></el-icon>
                  <div>加载失败</div>
                </div>
              </template>
            </el-image>
            <div class="image-info">
              <p>ID: {{ image.id }}</p>
              <p>文件名: {{ image.file_name }}</p>
              <p>词条: {{ image.title }}</p>
            </div>
            <div class="image-actions">
              <el-button type="danger" size="small" @click="deleteImage(image)">删除</el-button>
            </div>
          </div>
        </div>
        
        <!-- 加载更多提示 -->
        <div v-if="loadingMore" class="loading-more">
          <el-icon class="is-loading"><loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-if="allLoaded && imagesList.length > 0" class="no-more">
          <span>没有更多图片了</span>
        </div>
      </div>
      
      <!-- 分页信息 -->
      <div class="pagination-info" v-if="imagesList.length > 0">
        <span>共 {{ totalImages }} 张图片，当前显示 {{ imagesList.length }} 张</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture, Loading } from '@element-plus/icons-vue'

export default {
  name: 'ImagesView',
  components: {
    Picture,
    Loading
  },
  setup() {
    const loading = ref(false)
    const imagesList = ref([])
    const entriesList = ref([])
    const filterEntry = ref('')
    const uploadDialogVisible = ref(false)
    const uploadRef = ref(null)
    const uploadForm = ref({
      entry_id: '',
      is_cover: 'false'
    })
    
    // 分页相关
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalImages = ref(0)
    const totalPages = ref(0)
    const loadingMore = ref(false)
    const allLoaded = ref(false)
    
    const uploadHeaders = computed(() => {
      return {
        Authorization: `Bearer ${localStorage.getItem('admin-token')}`
      }
    })
    
    // 监听筛选条件变化，重置分页并重新加载
    watch(filterEntry, () => {
      resetPagination()
      fetchImages()
    })
    
    // 重置分页状态
    const resetPagination = () => {
      currentPage.value = 1
      imagesList.value = []
      allLoaded.value = false
    }
    const triggerSimpleAction = async () => {
      try {
        const response = await axios.post('/api/admin/initialize-index')
        ElMessage.success(response.data.message)
      } catch (error) {
        console.error('重新计算图片指数失败:', error)
        ElMessage.error('重新计算图片指数失败: ' + error.message)
      }
    }
    // 获取图片（支持分页和筛选）
    const fetchImages = async (loadMore = false) => {
      if (loading.value || (loadMore && allLoaded.value)) return
      
      try {
        loading.value = true
        if (loadMore) {
          loadingMore.value = true
        }
        
        // 构建请求参数
        const params = {
          page: currentPage.value,
          per_page: pageSize.value
        }
        
        // 添加筛选条件
        if (filterEntry.value) {
          params.entry_id = filterEntry.value
        }
        
        const response = await axios.get('/api/admin/images', { params })
        const images = response.data.images
        const pagination = response.data.pagination
        
        // 更新分页信息
        totalImages.value = pagination.total
        totalPages.value = pagination.pages
        
        // 转换为数组格式并添加完整的图片URL
        const newImages = Object.entries(images).map(([key, image]) => {
          return {
            key,
            ...image,
            url: `${axios.defaults.baseURL}/admin/images/${image.url}`, // 添加完整的图片URL路径
            file_name: image.url
          }
        })
        
        // 如果是加载更多，则追加到现有列表
        if (loadMore) {
          imagesList.value = [...imagesList.value, ...newImages]
        } else {
          imagesList.value = newImages
        }
        
        // 检查是否已加载全部
        allLoaded.value = currentPage.value >= totalPages.value
        
        console.log('获取到的图片:', newImages)
        console.log('分页信息:', pagination)
      } catch (error) {
        console.error('获取图片失败:', error)
        ElMessage.error('获取图片失败: ' + error.message)
      } finally {
        loading.value = false
        loadingMore.value = false
      }
    }
    
    // 获取所有词条
    const fetchEntries = async () => {
      try {
        const response = await axios.get('/api/admin/entries')
        const entries = response.data.entries
        
        // 转换为数组格式
        entriesList.value = Object.entries(entries).map(([key, entry]) => {
          return {
            key,
            ...entry
          }
        })
      } catch (error) {
        console.error('获取词条失败:', error)
        ElMessage.error('获取词条失败')
      }
    }
    
    // 获取词条标题
    const getEntryTitle = (entryKey) => {
      if (!entryKey) return '未关联词条'
      
      // 处理不同格式的词条ID
      let searchKey = entryKey
      if (entryKey && !entryKey.startsWith('entry') && !isNaN(entryKey)) {
        // 如果是纯数字，添加'entry'前缀
        searchKey = `entry${entryKey}`
      }
      
      const entry = entriesList.value.find(e => e.key === searchKey)
      return entry ? entry.title : (searchKey || '未关联词条')
    }
    
    // 打开上传对话框
    const openUploadDialog = () => {
      uploadDialogVisible.value = true
      uploadForm.value.entry_id = ''
      if (uploadRef.value) {
        uploadRef.value.clearFiles()
      }
    }
    
    // 提交上传
    const submitUpload = () => {
      if (uploadRef.value) {
        uploadRef.value.submit()
      } else {
        ElMessage.warning('请先选择文件')
      }
    }
    
    // 处理上传成功
    const handleUploadSuccess = (response) => {
      ElMessage.success('图片上传成功')
      uploadDialogVisible.value = false
      fetchImages()
    }
    
    // 上传前检查
    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2
      
      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      return true
    }
    
    // 删除图片
    const deleteImage = (image) => {
      ElMessageBox.confirm(`确定要删除图片「${image.file_name}」吗?`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.delete(`/api/admin/images/${image.key}`)
          ElMessage.success('删除成功')
          fetchImages()
        } catch (error) {
          console.error('删除图片失败:', error)
          ElMessage.error('删除图片失败')
        }
      }).catch(() => {})
    }
    
    // 加载更多图片
    const loadMore = () => {
      if (loading.value || loadingMore.value || allLoaded.value) return
      
      currentPage.value++
      fetchImages(true)
    }
    
    onMounted(() => {
      fetchImages()
      fetchEntries()
    })
    
    return {
      loading,
      loadingMore,
      imagesList,
      entriesList,
      filterEntry,
      uploadHeaders,
      uploadDialogVisible,
      uploadForm,
      uploadRef,
      currentPage,
      totalImages,
      totalPages,
      allLoaded,
      getEntryTitle,
      openUploadDialog,
      submitUpload,
      handleUploadSuccess,
      beforeUpload,
      deleteImage,
      loadMore,
      triggerSimpleAction
    }
  }

  
}
</script>

<style scoped>
.images-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 20px;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.image-card {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.image-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.image-wrapper {
  display: flex;
  flex-direction: column;
}

.el-image {
  height: 200px;
  width: 100%;
}

/* 自定义图片预览样式 */
:deep(.el-image-viewer__wrapper) {
  z-index: 3000;
}

:deep(.el-image-viewer__img) {
  max-width: 80%;
  max-height: 80%;
}

.image-error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
  font-size: 14px;
}

.image-error .el-icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.image-info {
  padding: 10px;
  background-color: #f5f7fa;
}

.image-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #606266;
  word-break: break-all;
}

.image-actions {
  padding: 10px;
  display: flex;
  justify-content: flex-end;
}

.images-container-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.loading-more, .no-more {
  text-align: center;
  padding: 15px 0;
  color: #909399;
  font-size: 14px;
}

.loading-more .el-icon {
  margin-right: 5px;
  animation: rotating 2s linear infinite;
}

.pagination-info {
  text-align: center;
  margin-top: 10px;
  color: #606266;
  font-size: 14px;
}

.button-group {
  display: flex;
  gap: 10px; /* 控制按钮之间的间距 */
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>