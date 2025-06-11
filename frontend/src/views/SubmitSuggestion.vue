<template>
  <div class="submit-container">
    <el-card class="submit-card">
      <template #header>
        <span>提交建议</span>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="建议标题">
          <el-input v-model="form.title" placeholder="请输入建议标题"></el-input>
        </el-form-item>
        <el-form-item label="建议内容">
          <el-input
            type="textarea"
            v-model="form.content"
            :rows="6"
            placeholder="请详细描述您的建议"
          ></el-input>
        </el-form-item>
        <el-form-item label="联系邮箱">
          <el-input v-model="form.username" placeholder="请输入联系邮箱"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const form = ref({
  title: '',
  content: '',
  username: ''
})
const loading = ref(false)

async function handleSubmit() {
  if (!form.value.title || !form.value.content) {
    ElMessage.warning('请填写完整信息')
    return
  }
  loading.value = true
  try {
    // 构造建议数据结构
    const suggestionData = {
      title: form.value.title,
      content: form.value.content,
      username: form.value.username 
    }
    // 后端接口
    const res = await axios.post('http://127.0.0.1:5000/api/suggestions', suggestionData)
    if (res.data && res.data.status === 'success') {
      ElMessage.success('提交成功，感谢您的建议！')
      form.value.title = ''
      form.value.content = ''
      form.value.username = ''
    } else {
      ElMessage.error(res.data.message || '提交失败')
    }
  } catch (e) {
    ElMessage.error('提交失败，请稍后重试')
  }
  loading.value = false
}
</script>

<style scoped>
.submit-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
}
.submit-card {
  box-shadow: 0 2px 12px #f0f1f2;
}
</style>