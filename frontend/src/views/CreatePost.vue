<template>
  <div class="create-post">
    <h2>发布新帖</h2>

    <el-form :model="form" label-width="80px">
      <!-- 标题 -->
      <el-form-item label="标题" :rules="[{ required: true, message: '请输入标题' }]">
        <el-input v-model="form.title" placeholder="请输入帖子标题"></el-input>
      </el-form-item>

      <!-- 内容 -->
      <el-form-item label="内容" :rules="[{ required: true, message: '内容不能为空' }]">
        <el-input v-model="form.content" type="textarea" :rows="4" placeholder="请输入内容"></el-input>
      </el-form-item>

      <!-- 作者 -->
      <el-form-item label="作者">
        <el-input v-model="form.author" placeholder="匿名"></el-input>
      </el-form-item>

      <!-- 分类 -->
      <el-form-item label="分类">
        <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
          <el-option label="动漫" value="动漫"></el-option>
          <el-option label="电影" value="电影"></el-option>
          <el-option label="电视剧" value="电视剧"></el-option>
          <el-option label="游戏" value="游戏"></el-option>
        </el-select>
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitPost" style="width: 100%">提交</el-button>
        <el-button @click="$router.back()" style="width: 100%; margin-top: 10px;">取消</el-button>
      </el-form-item>
    </el-form>

    <!-- 成功提示 -->
    <el-alert
      v-if="successMessage"
      :title="successMessage"
      type="success"
      show-icon
      :closable="false"
    ></el-alert>

    <!-- 错误提示 -->
    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      :closable="false"
    ></el-alert>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 表单数据
const form = ref({
  title: '',
  content: '',
  author: '',
  category: ''
})

// 提示信息
const successMessage = ref('')
const errorMessage = ref('')

// 提交帖子到后端
async function submitPost() {
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/posts', form.value)
    console.log('新增成功:', res.data)

    successMessage.value = '帖子发布成功！'
    errorMessage.value = ''

    // 可选：1.5秒后跳转首页
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (error) {
    errorMessage.value = '发布失败，请重试。'
    successMessage.value = ''
    console.error('提交失败:', error)
  }
}
</script>

<style scoped>
.create-post {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-form {
  margin-top: 20px;
}

.el-alert {
  margin-top: 20px;
}
</style>