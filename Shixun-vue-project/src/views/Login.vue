<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>{{ isLogin ? '欢迎登录' : '用户注册' }}</h2>
        <p class="subtitle">{{ isLogin ? '请登录您的账号' : '创建您的新账号' }}</p>
      </div>
      
      <el-card class="login-card" shadow="never">
        <!-- 登录表单 -->
        <el-form
          v-if="isLogin"
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="0"
          class="login-form"
        >
          <el-form-item prop="username">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入用户名"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              prefix-icon="Lock"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" class="submit-btn">登录</el-button>
          </el-form-item>
          <div class="form-footer">
            <span>还没有账号？</span>
            <el-button link type="primary" @click="isLogin = false">立即注册</el-button>
          </div>
        </el-form>

        <!-- 注册表单 -->
        <el-form
          v-else
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-width="0"
          class="login-form"
        >
          <el-form-item prop="username">
            <el-input 
              v-model="registerForm.username" 
              placeholder="请输入用户名"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              prefix-icon="Lock"
            />
          </el-form-item>
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              show-password
              prefix-icon="Lock"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister" class="submit-btn">注册</el-button>
          </el-form-item>
          <div class="form-footer">
            <span>已有账号？</span>
            <el-button link type="primary" @click="isLogin = true">立即登录</el-button>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const isLogin = ref(true)
const loginFormRef = ref(null)
const registerFormRef = ref(null)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

// 登录表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 注册表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.post('/api/auth/login', {
          username: loginForm.username,
          password: loginForm.password
        })
        
        if (response.data.status === 'success') {
          // 存储用户信息和token
          localStorage.setItem('username', loginForm.username)
          localStorage.setItem('token', response.data.token || 'user-token-' + Date.now())
          
          // 触发storage事件，通知其他页面更新状态
          window.dispatchEvent(new StorageEvent('storage', {
            key: 'username',
            newValue: loginForm.username
          }))
          
          ElMessage.success('登录成功')
          
          // 确保路由存在后再跳转
          if (router.hasRoute('Home')) {
            router.push('/home')
          } else {
            console.error('Home route not found')
            ElMessage.error('路由配置错误，请联系管理员')
          }
        } else {
          ElMessage.error(response.data.message || '用户名或密码错误')
        }
      } catch (error) {
        console.error('Login error:', error)
        ElMessage.error(error.response?.data?.message || '登录失败，请稍后重试')
      }
    }
  })
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.post('/api/auth/register', {
          username: registerForm.username,
          password: registerForm.password
        })
        
        if (response.data.status === 'success') {
          ElMessage.success('注册成功，请登录')
          isLogin.value = true
          // 清空注册表单
          registerForm.username = ''
          registerForm.password = ''
          registerForm.confirmPassword = ''
        } else {
          ElMessage.error(response.data.message || '注册失败')
        }
      } catch (error) {
        if (error.response?.data?.message === '用户名已存在') {
          ElMessage.warning('用户名已存在，请直接登录')
          isLogin.value = true
          // 将注册表单的用户名和密码填入登录表单
          loginForm.username = registerForm.username
          loginForm.password = registerForm.password
        } else {
          ElMessage.error(error.response?.data?.message || '注册失败')
        }
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: fixed;
  top: 0;
  left: 0;
  margin: 0;
  padding: 0;
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
  color: white;
}

.login-header h2 {
  font-size: 28px;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  opacity: 0.8;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.login-form {
  padding: 20px 0;
}

.submit-btn {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #606266;
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-input__inner) {
  height: 40px;
}
</style> 