<template>
  <div class="suggestions-container">
    <div class="page-header">
      <h2>用户建议</h2>
      <!-- 导出按钮 -->
      <el-button type="primary" @click="exportTable">导出表格</el-button>
    </div>

    <el-table :data="suggestionsList" v-loading="loading" border style="width: 100%">
      <el-table-column prop="title" label="标题" width="200"></el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
      <el-table-column prop="username" label="联系邮箱" width="250"></el-table-column>
      <el-table-column prop="time" label="时间" width="180"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'
export default {
  name: 'SuggestionsView',
  setup() {
    const suggestionsList = ref([])
    const loading = ref(false)

    // 获取用户建议列表
    const fetchSuggestions = async () => {
      loading.value = true
      try {
        const token = localStorage.getItem('admin-token')
        const response = await axios.get('/api/admin/suggestions', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data.status === 'success') {
          suggestionsList.value = response.data.suggestions
        } else {
          ElMessage.error(response.data.message || '获取用户建议失败')
        }
      } catch (error) {
        console.error('获取用户建议出错:', error)
        ElMessage.error(error.response?.data?.message || '获取用户建议失败')
      } finally {
        loading.value = false
      }
    }
    // 导出表格功能
    const exportTable = () => {
      if (suggestionsList.value.length === 0) {
        ElMessage.warning('没有数据可导出')
        return
      }

        // 构造导出数据，将 username 替换为 email
    const exportData = suggestionsList.value.map(item => ({
      title: item.title,
      content: item.content,
      email: item.username, // 将 username 替换为 email
      time: item.time
    }))

      // 构造 Excel 数据
      const worksheet = XLSX.utils.json_to_sheet(exportData)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, '用户建议')

      // 导出 Excel 文件
      XLSX.writeFile(workbook, '用户建议.xlsx')
      ElMessage.success('表格导出成功')
    }
    onMounted(() => {
      fetchSuggestions()
    })

    return {
      suggestionsList,
      loading,
      exportTable
    }
  }
}
</script>

<style scoped>
.suggestions-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>