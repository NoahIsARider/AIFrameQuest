<template>
  <div class="app-container">
    <div class="user-status" v-if="currentRoute !== '/login'">
      <template v-if="username">
        <span class="welcome-text">{{ username }}，欢迎您使用</span>
        <el-button link type="primary" @click="handleLogout">退出登录</el-button>
      </template>
      <template v-else>
        <span class="welcome-text">当前未登录</span>
        <el-button link type="primary" @click="goToLogin">去登录</el-button>
      </template>
    </div>
    
    <!-- 在非登录页面显示导航栏 -->
    <Nav v-if="currentRoute !== '/login'" />
    
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Nav from './components/Nav.vue'

const route = useRoute()
const router = useRouter()
const username = ref(localStorage.getItem('username') || '')

const currentRoute = computed(() => route.path)

// 监听路由变化
watch(currentRoute, () => {
  updateUserStatus()
})

// 更新用户状态
const updateUserStatus = () => {
  username.value = localStorage.getItem('username') || ''
}

// 监听localStorage变化
window.addEventListener('storage', (e) => {
  if (e.key === 'username') {
    username.value = e.newValue
  }
})

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('username')
  localStorage.removeItem('token')
  username.value = ''
  ElMessage.success('已退出登录')
  router.push('/login')
}

// 跳转到登录页
const goToLogin = () => {
  router.push('/login')
}

// 组件挂载时更新状态
onMounted(() => {
  updateUserStatus()
  // 如果当前在根路径，重定向到登录页
  if (route.path === '/') {
    router.push('/login')
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
}

.app-container {
  min-height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.user-status {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.welcome-text {
  font-size: 14px;
  color: #333;
}
</style>