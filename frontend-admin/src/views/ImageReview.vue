<template>
  <div class="image-review-container">

    <div class="page-header">
      <h1>图片审核</h1>
      
      <!-- AI审核按钮 -->
      <div class="action-buttons">
        <el-button 
          type="primary" 
          :loading="analyzing" 
          @click="analyzeImagesWithAI"
        >
          AI审核图片
        </el-button>
      </div>
    </div>
    
    <!-- 筛选表单 -->
    <div class="filter-form">
      <el-form :inline="true">
        <el-form-item label="词条">
          <el-select v-model="filterEntry" placeholder="选择词条" clearable style="width: 200px;">
            <el-option
              v-for="entry in entriesList"
              :key="entry.key"
              :label="entry.title"
              :value="entry.key"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="filterStatus" placeholder="选择状态" clearable style="width: 200px;">
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 图片列表 -->
    <div v-else class="images-list">
      <el-empty v-if="filteredImages.length === 10" description="暂无待审核图片"></el-empty>
      <div v-else class="images-grid">
        <div class="image-card" v-for="image in filteredImages" :key="image.id">
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
          </div>
          <div class="image-info">
            <p>ID: {{ image.id }}</p>
            <p>文件名: {{ image.file_name }}</p>
            <p>词条: {{ getEntryTitle(image.entry) }}</p>
            <p>上传者: {{ image.uploader }}</p>
            <p>上传时间: {{ image.upload_time }}</p>
            <p>状态: <el-tag :type="getStatusType(image.status)">{{ getStatusText(image.status) }}</el-tag></p>
            <p v-if="image.description">描述: {{ image.description }}</p>
            
            <!-- AI审核结果 -->
            <p v-if="image.ai_moderation">
              AI审核: 
              <el-tag :type="getAIModerationLabelType(image)">
                {{ getAIModerationLabel(image) }}
              </el-tag>
              
              <!-- AI审核详情 -->
              <el-popover
                placement="right"
                width="300"
                trigger="hover"
              >
                <template #reference>
                  <el-button link type="primary" size="small">查看详情</el-button>
                </template>
                
                <template #default>
                  <div v-if="image.ai_moderation.error">
                    <p>审核失败: {{ image.ai_moderation.error }}</p>
                  </div>
                  <div v-else>
                    <h4>审核结果</h4>
                    <p>是否适当: {{ image.ai_moderation.is_appropriate ? '是' : '否' }}</p>
                    <p v-if="image.ai_moderation.issues">
                      存在问题: {{ formatIssues(image.ai_moderation.issues) }}
                    </p>
                    <p v-if="image.ai_moderation.explanation">
                      解释: {{ image.ai_moderation.explanation }}
                    </p>
                    <p v-if="image.ai_moderation.recommendation">
                      建议: {{ image.ai_moderation.recommendation }}
                    </p>
                    <p v-if="image.ai_moderation.relevance">
                      相关性评分: {{ image.ai_moderation.relevance }}/10
                    </p>
                    <p v-if="image.ai_moderation.relevance_explanation">
                      相关性解释: {{ image.ai_moderation.relevance_explanation }}
                    </p>
                    
                    <h4 v-if="image.content_analysis">内容分析</h4>
                    <p v-if="image.content_analysis.description">
                      描述: {{ image.content_analysis.description }}
                    </p>
                    <p v-if="image.content_analysis.content_type">
                      内容类型: {{ image.content_analysis.content_type }}
                    </p>
                    <p v-if="image.content_analysis.sensitive_content !== undefined">
                      敏感内容: {{ image.content_analysis.sensitive_content ? '是' : '否' }}
                    </p>
                    <p v-if="image.content_analysis.sensitive_details">
                      敏感内容详情: {{ image.content_analysis.sensitive_details }}
                    </p>
                    <p v-if="image.content_analysis.relevance_score">
                      相关性评分: {{ image.content_analysis.relevance_score }}/10
                    </p>
                    <p v-if="image.content_analysis.relevance_details">
                      相关性详情: {{ image.content_analysis.relevance_details }}
                    </p>
                  </div>
                </template>
              </el-popover>
            </p>
          </div>
          <div class="image-actions" v-if="image.status === 'pending'">
            <div class="action-row">
              <el-button type="success" size="small" @click="approveImage(image)">通过</el-button>
              <el-button type="danger" size="small" @click="rejectImage(image)">拒绝</el-button>
            </div>
            <div class="action-row" style="margin-top: 8px;">
              <el-button 
                type="primary" 
                size="small" 
                :loading="image.analyzing" 
                @click="analyzeImageWithAI(image)"
              >
                AI审核
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'

export default {
  name: 'ImageReviewView',
  components: {
    Picture
  },
  setup() {
    const loading = ref(false)
    const imagesList = ref([])
    const entriesList = ref([])
    const filterEntry = ref('')
    const filterStatus = ref('pending')
    
    const filteredImages = computed(() => {
      let filtered = imagesList.value
      
      // 按状态筛选
      if (filterStatus.value) {
        filtered = filtered.filter(image => image.status === filterStatus.value)
      }
      
      // 按词条筛选
      if (filterEntry.value) {
        filtered = filtered.filter(image => image.entry === filterEntry.value)
      }
      
      return filtered
    })
    
    // 获取未审核图片列表
    const fetchUncensoredImages = async () => {
      try {
        loading.value = true
        const response = await axios.get('/api/admin/uncensored-images')
        const images = response.data.images
        
        // 转换为数组格式并添加完整的图片URL
        imagesList.value = Object.entries(images).map(([key, image]) => {
          return {
            id: key,
            ...image,
            url: `${axios.defaults.baseURL}/images_uncensored/${image.file_name}` // 添加完整的图片URL路径
          }
        })
        console.log('获取到的未审核图片:', imagesList.value)
      } catch (error) {
        console.error('获取未审核图片失败:', error)
        ElMessage.error('获取未审核图片失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }
    
    // 获取所有词条
    const fetchEntries = async () => {
      try {
        const response = await axios.get('/api/admin/entries')
        const entries = response.data.entries
        
        // 转换为数组格式，并确保每个词条对象包含id属性
        entriesList.value = Object.entries(entries).map(([key, entry]) => {
          // 尝试从key中提取ID（如果key的格式是数字或者类似'entry6'）
          let id = null
          if (/^\d+$/.test(key)) {
            // 如果key是纯数字
            id = parseInt(key)
          } else {
            // 尝试从类似'entry6'的格式中提取数字
            const match = key.match(/entry(\d+)/)
            if (match && match[1]) {
              id = parseInt(match[1])
            }
          }
          
          return {
            key,
            id: id || entry.id || null, // 优先使用提取的ID，其次使用entry对象中的id属性
            ...entry
          }
        })
        
        console.log('获取到的词条列表:', entriesList.value)
      } catch (error) {
        console.error('获取词条失败:', error)
        ElMessage.error('获取词条失败')
      }
    }
    
    // 格式化issues字段，处理不同类型的数据
    const formatIssues = (issues) => {
      if (Array.isArray(issues)) {
        return issues.join(', ')
      } else if (typeof issues === 'object') {
        return JSON.stringify(issues)
      } else {
        return String(issues)
      }
    }
    
    // 获取词条标题
    const getEntryTitle = (entryKey) => {
      if (!entryKey) return '未关联词条'
      
      // 从entry字符串(如"entry6")中提取数字ID
      const match = entryKey.match(/entry(\d+)/)
      if (match && match[1]) {
        const entryId = parseInt(match[1])
        
        // 尝试多种方式查找对应的词条
        // 1. 直接通过id属性匹配
        let entry = entriesList.value.find(e => e.id === entryId)
        if (entry) return entry.title
        
        // 2. 通过key属性匹配(如果key是数字字符串)
        entry = entriesList.value.find(e => e.key === String(entryId))
        if (entry) return entry.title
        
        // 3. 通过key属性匹配完整的entryKey
        entry = entriesList.value.find(e => e.key === entryKey)
        if (entry) return entry.title
        
        // 4. 如果entriesList中的对象有post_id属性
        entry = entriesList.value.find(e => e.post_id === entryId)
        if (entry) return entry.title
        
        // 如果都没找到，返回带ID的未关联提示
        return `未关联词条(ID:${entryId})`
      }
      
      // 如果没有找到匹配的词条，尝试直接在entriesList中查找
      const entry = entriesList.value.find(e => e.key === entryKey)
      return entry ? entry.title : (entryKey || '未关联词条')
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待审核',
        'approved': '已通过',
        'rejected': '已拒绝'
      }
      return statusMap[status] || status
    }
    
    // 获取状态标签类型
    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger'
      }
      return typeMap[status] || ''
    }
    
    // 通过图片审核
    const approveImage = (image) => {
      ElMessageBox.confirm(`确定要通过图片「${image.file_name}」的审核吗?`, '确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(async () => {
        try {
          await axios.post(`/api/admin/uncensored-images/${image.id}/approve`)
          ElMessage.success('审核通过成功')
          fetchUncensoredImages() // 刷新列表
        } catch (error) {
          console.error('审核操作失败:', error)
          ElMessage.error('审核操作失败: ' + error.message)
        }
      }).catch(() => {})
    }
    
    // 拒绝图片审核
    const rejectImage = (image) => {
      ElMessageBox.confirm(`确定要拒绝图片「${image.file_name}」的审核吗?`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.post(`/api/admin/uncensored-images/${image.id}/reject`)
          ElMessage.success('已拒绝该图片')
          fetchUncensoredImages() // 刷新列表
        } catch (error) {
          console.error('审核操作失败:', error)
          ElMessage.error('审核操作失败: ' + error.message)
        }
      }).catch(() => {})
    }
    
    // AI审核图片状态
    const analyzing = ref(false)
    
    // AI审核所有待审核图片
    const analyzeImagesWithAI = async () => {
      try {
        analyzing.value = true
        
        // 检查是否有待审核的图片
        const pendingImages = imagesList.value.filter(img => img.status === 'pending')
        if (pendingImages.length === 0) {
          ElMessage.warning('没有待审核的图片')
          return
        }
        
        // 调用后端API进行AI审核
        const response = await axios.get('/api/admin/analyze/images/ai_moderation')
        
        if (response.data.status === 'success') {
          // 更新图片列表中的AI审核结果
          const results = response.data.results || []
          
          // 将AI审核结果添加到图片列表中
          results.forEach(result => {
            const imageIndex = imagesList.value.findIndex(img => img.id === result.id)
            if (imageIndex !== -1) {
              imagesList.value[imageIndex].ai_moderation = result.moderation
              imagesList.value[imageIndex].content_analysis = result.content_analysis
            }
          })
          
          ElMessage.success(`成功审核 ${results.length} 张图片`)
        } else {
          ElMessage.error('AI审核失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('AI审核图片失败:', error)
        ElMessage.error('AI审核图片失败: ' + error.message)
      } finally {
        analyzing.value = false
      }
    }
    
    // 获取AI审核结果标签
    const getAIModerationLabel = (image) => {
      if (!image.ai_moderation) return null
      
      const moderation = image.ai_moderation
      if (moderation.error) return '审核失败'
      
      return moderation.is_appropriate ? '通过' : '不通过'
    }
    
    // 获取AI审核结果标签类型
    const getAIModerationLabelType = (image) => {
      if (!image.ai_moderation) return ''
      
      const moderation = image.ai_moderation
      if (moderation.error) return 'info'
      
      return moderation.is_appropriate ? 'success' : 'danger'
    }
    
    // 单独审核一张图片
    const analyzeImageWithAI = async (image) => {
      try {
        // 设置该图片的审核状态为正在分析
        const imageIndex = imagesList.value.findIndex(img => img.id === image.id)
        if (imageIndex !== -1) {
          imagesList.value[imageIndex].analyzing = true
        }
        
        // 调用后端API进行AI审核
        const response = await axios.get(`/api/admin/analyze/images/${image.id}/ai_moderation`)
        
        if (response.data.status === 'success') {
          // 更新图片的AI审核结果
          const result = response.data.result
          
          if (imageIndex !== -1) {
            imagesList.value[imageIndex].ai_moderation = result.moderation
            imagesList.value[imageIndex].content_analysis = result.content_analysis
            imagesList.value[imageIndex].analyzing = false
          }
          
          ElMessage.success('AI审核完成')
        } else {
          ElMessage.error('AI审核失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('AI审核图片失败:', error)
        ElMessage.error('AI审核图片失败: ' + error.message)
      } finally {
        // 清除该图片的审核状态
        const imageIndex = imagesList.value.findIndex(img => img.id === image.id)
        if (imageIndex !== -1) {
          imagesList.value[imageIndex].analyzing = false
        }
      }
    }
    
    onMounted(() => {
      fetchUncensoredImages()
      fetchEntries()
    })
    
    return {
      loading,
      analyzing,
      imagesList,
      entriesList,
      filterEntry,
      filterStatus,
      filteredImages,
      getEntryTitle,
      getStatusText,
      getStatusType,
      approveImage,
      rejectImage,
      analyzeImagesWithAI,
      analyzeImageWithAI,
      getAIModerationLabel,
      getAIModerationLabelType,
      formatIssues
    }
  }
}
</script>

<style scoped>
.review-container {
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.image-card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.image-wrapper {
  display: flex;
  flex-direction: column;
}

.image-wrapper .el-image {
  height: 200px;
  width: 100%;
  object-fit: cover;
}

.image-error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
}

.image-info {
  padding: 10px;
  font-size: 14px;
}

.image-info p {
  margin: 5px 0;
  word-break: break-all;
}

.image-actions {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-top: 1px solid #ebeef5;
}

.action-row {
  display: flex;
  justify-content: space-between;
}
</style>