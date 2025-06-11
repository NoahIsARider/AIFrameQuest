<template>
  <div class="submit-container">
    <el-card class="submit-card">
      <template #header>
        <span>提交词条</span>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="词条名称">
          <el-input v-model="form.name" placeholder="请输入词条名称"></el-input>
        </el-form-item>
        <el-form-item label="词条类型">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="动漫" value="动漫"></el-option>
            <el-option label="电影" value="电影"></el-option>
            <el-option label="电视剧" value="电视剧"></el-option>
            <el-option label="游戏" value="游戏"></el-option>
            <el-option label="迷因" value="迷因"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="词条介绍">
          <el-input
            type="textarea"
            v-model="form.description"
            :rows="5"
            placeholder="请输入词条介绍"
          ></el-input>
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
  name: '',
  type: '',
  description: ''
})
const loading = ref(false)

async function handleSubmit() {
  if (!form.value.name || !form.value.type || !form.value.description) {
    ElMessage.warning('请填写完整信息')
    return
  }
  loading.value = true
  try {
    // 构造词条数据结构
    const entryData = {
      title: form.value.name,
      type: form.value.type,
      description: [form.value.description],
      cover: ''
    }
    // 调用词条API创建词条
    const res = await axios.post('http://127.0.0.1:5000/api/entries', entryData)
    if (res.data && res.data.status === 'success') {
      ElMessage.success('提交成功！')
      form.value.name = ''
      form.value.type = ''
      form.value.description = ''
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