<template>
  <div class="entries-uncensored-container">
    <div class="page-header">
      <h2>未审核词条</h2>
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
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'

export default {
  name: 'EntriesUncensoredView',
  components: {
    Picture
  },
  setup() {
    const entriesList = ref([])
    const loading = ref(false)

    // 获取未审核词条列表
    const fetchEntries = async () => {
      loading.value = true
      try {
        const token = localStorage.getItem('admin-token')
        const response = await axios.get('/api/admin/entries-uncensored', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data.status === 'success') {
          const entries = response.data.entries
          entriesList.value = Object.values(entries)
        } else {
          ElMessage.error(response.data.message || '获取未审核词条失败')
        }
      } catch (error) {
        console.error('获取未审核词条出错:', error)
        ElMessage.error(error.response?.data?.message || '获取未审核词条失败')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchEntries()
    })

    return {
      entriesList,
      loading
    }
  }
}
</script>

<style scoped>
.entries-uncensored-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.image-error {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  background-color: #f5f7fa;
  color: #909399;
}
</style>