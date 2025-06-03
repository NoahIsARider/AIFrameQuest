<template>
  <div class="entries-container">
    <div class="page-header">
      <h2>词条管理</h2>
      <el-button type="primary" @click="openEntryDialog()">添加词条</el-button>
    </div>

    <el-table :data="entriesList" v-loading="loading" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题" width="200"></el-table-column>
      <el-table-column label="封面" width="120">
        <template #default="scope">
          <el-image 
            v-if="scope.row.cover" 
            :src="`/admin/images/${scope.row.cover}`" 
            style="width: 80px; height: 80px" 
            fit="cover"
            :preview-src-list="[`/admin/images/${scope.row.cover}`]">
            <template #error>
              <div class="image-error">
                <el-icon><picture /></el-icon>
                <div>加载失败</div>
              </div>
            </template>
          </el-image>
          <span v-else>无封面</span>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="100"></el-table-column>
      <el-table-column label="描述">
        <template #default="scope">
          <div v-if="scope.row.description && scope.row.description.length">
            <p v-for="(desc, index) in scope.row.description" :key="index">{{ desc }}</p>
          </div>
          <span v-else>无描述</span>
        </template>
      </el-table-column>
      <el-table-column label="评论数" width="100">
        <template #default="scope">
          {{ scope.row.comments ? scope.row.comments.length : 0 }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="openEntryDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteEntry(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 词条编辑对话框 -->
    <el-dialog 
      :title="dialogType === 'add' ? '添加词条' : '编辑词条'" 
      v-model="dialogVisible" 
      width="50%">
      <el-form :model="entryForm" :rules="entryRules" ref="entryFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="entryForm.title"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-input v-model="entryForm.type"></el-input>
        </el-form-item>
        <el-form-item label="封面">
          <el-upload
            class="avatar-uploader"
            action="/api/admin/upload"
            :headers="uploadHeaders"
            :data="{entry_id: currentEntryId, is_cover: 'true'}"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :before-upload="beforeCoverUpload">
            <img v-if="entryForm.cover" :src="`/admin/images/${entryForm.cover}`" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="描述">
          <div v-for="(desc, index) in entryForm.description" :key="index" class="description-item">
            <el-input v-model="entryForm.description[index]"></el-input>
            <el-button type="danger" icon="delete" circle @click="removeDescription(index)"></el-button>
          </div>
          <el-button type="primary" @click="addDescription">添加描述</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveEntry">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Picture } from '@element-plus/icons-vue'

export default {
  name: 'EntriesView',
  components: {
    Plus,
    Picture
  },
  setup() {
    const loading = ref(false)
    const entriesList = ref([])
    const dialogVisible = ref(false)
    const dialogType = ref('add')
    const entryFormRef = ref(null)
    
    const entryForm = reactive({
      id: null,
      title: '',
      type: '',
      cover: '',
      description: [],
      comments: []
    })
    
    const entryRules = {
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请输入类型', trigger: 'blur' }
      ]
    }
    
    const currentEntryId = computed(() => {
      return entryForm.id ? `entry${entryForm.id}` : ''
    })
    
    const uploadHeaders = computed(() => {
      return {
        Authorization: `Bearer ${localStorage.getItem('admin-token')}`
      }
    })
    
    // 获取所有词条
    const fetchEntries = async () => {
      try {
        loading.value = true
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
      } finally {
        loading.value = false
      }
    }
    
    // 打开词条编辑对话框
    const openEntryDialog = (entry) => {
      if (entry) {
        dialogType.value = 'edit'
        Object.assign(entryForm, entry)
      } else {
        dialogType.value = 'add'
        Object.assign(entryForm, {
          id: entriesList.value.length > 0 ? Math.max(...entriesList.value.map(e => e.id)) + 1 : 1,
          title: '',
          type: '',
          cover: '',
          description: [],
          comments: []
        })
      }
      dialogVisible.value = true
    }
    
    // 保存词条
    const saveEntry = () => {
      entryFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            const entryId = `entry${entryForm.id}`
            await axios.put(`/api/admin/entries/${entryId}`, entryForm)
            ElMessage.success('保存成功')
            dialogVisible.value = false
            fetchEntries()
          } catch (error) {
            console.error('保存词条失败:', error)
            ElMessage.error('保存词条失败')
          }
        }
      })
    }
    
    // 删除词条
    const deleteEntry = (entry) => {
      ElMessageBox.confirm(`确定要删除词条「${entry.title}」吗?`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const entryId = `entry${entry.id}`
          await axios.delete(`/api/admin/entries/${entryId}`)
          ElMessage.success('删除成功')
          fetchEntries()
        } catch (error) {
          console.error('删除词条失败:', error)
          ElMessage.error('删除词条失败')
        }
      }).catch(() => {})
    }
    
    // 处理封面上传成功
    const handleCoverSuccess = (response) => {
      entryForm.cover = response.image.file_name
      ElMessage.success('封面上传成功')
    }
    
    // 上传前检查
    const beforeCoverUpload = (file) => {
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
    
    // 添加描述
    const addDescription = () => {
      entryForm.description.push('')
    }
    
    // 删除描述
    const removeDescription = (index) => {
      entryForm.description.splice(index, 1)
    }
    
    onMounted(() => {
      fetchEntries()
    })
    
    return {
      loading,
      entriesList,
      dialogVisible,
      dialogType,
      entryForm,
      entryRules,
      entryFormRef,
      currentEntryId,
      uploadHeaders,
      openEntryDialog,
      saveEntry,
      deleteEntry,
      handleCoverSuccess,
      beforeCoverUpload,
      addDescription,
      removeDescription
    }
  }
}
</script>

<style scoped>
.entries-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.description-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.description-item .el-input {
  margin-right: 10px;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 120px;
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
}

.image-error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
}

.image-error .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.avatar {
  width: 120px;
  height: 120px;
  display: block;
  object-fit: cover;
}
</style>