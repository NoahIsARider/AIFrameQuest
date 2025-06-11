<template>
  <div class="login-container">
    <div class="login-box">
      <h2>AIFrameQuest 管理系统</h2>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" class="login-form">
        <el-form-item prop="id">
          <el-input v-model="loginForm.id" placeholder="管理员ID" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="loginForm.email" placeholder="邮箱" prefix-icon="Message"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" class="login-button">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Key } from '@element-plus/icons-vue'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)

    const loginForm = reactive({
      id: '',
      email: '',
      password: ''
    })

    const loginRules = {
      id: [
        { required: true, message: '请输入管理员ID', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
      ]
    }

    const handleLogin = () => {
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            loading.value = true
            const response = await axios.post('/api/admin/login', loginForm)
            const { token, admin } = response.data
            
            // 保存token和管理员信息
            localStorage.setItem('admin-token', token)
            localStorage.setItem('admin-info', JSON.stringify(admin))
            
            ElMessage.success('登录成功')
            router.push('/dashboard')
          } catch (error) {
            console.error('登录失败:', error)
            ElMessage.error(error.response?.data?.message || '登录失败，请检查ID、邮箱和密码')
          } finally {
            loading.value = false
          }
        }
      })
    }

    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
  background:linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.0)),url('@/assets/images/background_noah.png') no-repeat center center;
  background-size: cover;
}

.login-box {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #015ebc;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  background-color: #015ebc;
}
</style>