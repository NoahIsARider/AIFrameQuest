<template>
  <div class="login-container">
    <div class="login-box">
      
      <el-card class="login-card" shadow="never">
        <div class="login-header">
        <h2>{{ isLogin ? '欢迎登录AIFrameQuest' : 'AIFrameQuest用户注册' }}</h2>
        <p class="subtitle">{{ isLogin ? '请登录您的账号' : '创建您的新账号' }}</p>
      </div>
        <!-- 登录表单 -->
        <el-form
          v-if="isLogin"
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="0"
          class="login-form"
        >
          <el-form-item prop="email">
            <el-input 
              v-model="loginForm.email" 
              placeholder="请输入邮箱"
              prefix-icon="Message"
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
          <el-form-item prop="email">
            <el-input 
              v-model="registerForm.email" 
              placeholder="请输入邮箱"
              prefix-icon="Message"
            />
          </el-form-item>
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
import { Message, Lock } from '@element-plus/icons-vue'
import axios from 'axios'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()
const isLogin = ref(true)
const loginFormRef = ref(null)
const registerFormRef = ref(null)

// 登录表单数据
const loginForm = reactive({
  email: '',
  password: ''
})

// 注册表单数据
const registerForm = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

// 登录表单验证规则
const loginRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 注册表单验证规则
const registerRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
  ],
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
          email: loginForm.email,
          password: loginForm.password
        })
        
        if (response.data.status === 'success') {
          // 存储用户信息和token
          // 从token中提取用户名（token格式为'user-token-用户名'）
          const username = response.data.token.split('-')[2]
          localStorage.setItem('username', username)
          localStorage.setItem('token', response.data.token)
          
          // 触发storage事件，通知其他页面更新状态
          window.dispatchEvent(new StorageEvent('storage', {
            key: 'username',
            newValue: username
          }))
          
          ElMessage.success('登录成功')
          window.location.reload();
          // 确保路由存在后再跳转
          if (router.hasRoute('Home')) {
            router.push('/home')
          } else {
            console.error('Home route not found')
            ElMessage.error('路由配置错误，请联系管理员')
          }
        } else {
          ElMessage.error(response.data.message || '邮箱或密码错误')
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
          email: registerForm.email,
          password: registerForm.password
        })
        
        if (response.data.status === 'success') {
          ElMessage.success('注册成功，请登录')
          isLogin.value = true
          // 清空注册表单
          registerForm.email = ''
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

const login = async () => {
  try {
    const response = await axios.post('/api/login', {
      username: username.value,
      password: password.value,
    });
    if (response.data.success) {
      // 使用修改后的mutation名称
      store.commit('setToken', response.data.token);
      store.commit('setUsername', username) // 更新 Vuex Store 的 username
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('username', username.value);
      router.push('/admin/dashboard');
    } else {
      alert(response.data.message);
    }
  } catch (error) {
    console.error(error);
    alert('登录失败');
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background:linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.8)),url('@/assets/images/login_background_lijun.png') no-repeat center center;
    /* background:linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.3)),url('@/assets/images/图片1.png') no-repeat center center; */
  background-size: cover;
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
  color: #1a237e;
}

.login-header h2 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #1565c0;
  font-weight: 600;
}

.subtitle {
  font-size: 16px;
  color: #283593;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(21, 101, 192, 0.1);
  border: 1px solid rgba(21, 101, 192, 0.2);
}

.login-form {
  padding: 20px 0;
}

.submit-btn {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
  background: #1565c0;
  border-color: #1565c0;
  font-weight: 500;
}

.submit-btn:hover {
  background: #0d47a1;
  border-color: #0d47a1;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #283593;
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
  box-shadow: 0 0 0 1px #90caf9;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #1565c0;
}

:deep(.el-input__inner) {
  height: 40px;
}

:deep(.el-button--primary.is-link) {
  color: #1565c0;
  font-weight: 500;
}

:deep(.el-button--primary.is-link:hover) {
  color: #0d47a1;
}
</style>