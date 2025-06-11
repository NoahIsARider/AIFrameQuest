<template>
  <div class="dashboard-container">
    <el-container>
      <el-aside width="200px">
        <div class="logo">AIFrameQuest 管理</div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF">
          <el-menu-item index="/dashboard/entries">
            <el-icon><document /></el-icon>
            <span>词条管理</span>
          </el-menu-item>
          <el-menu-item index="/dashboard/images">
            <el-icon><PictureFilled /></el-icon>
            <span>图片管理</span>
          </el-menu-item>
          <el-menu-item index="/dashboard/comments">
            <el-icon><chat-dot-round /></el-icon>
            <span>评论管理</span>
          </el-menu-item>
          <el-menu-item index="/dashboard/image-review">
            <el-icon><PictureRounded /></el-icon>
            <span>图片审核</span>
          </el-menu-item>
          <el-menu-item index="/dashboard/entries-uncensored">
            <el-icon><document /></el-icon>
            <span>未审核词条</span>
          </el-menu-item>
          <el-menu-item index="/dashboard/suggestions">
            <el-icon><ChatLineRound /></el-icon>
            <span>用户建议</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <div class="header-right">
            <span>{{ adminInfo.username || '管理员' }}</span>
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <el-icon><setting /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Document, PictureFilled, ChatDotRound, Setting, ChatLineRound } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { PictureRounded } from '@element-plus/icons-vue'

export default {
  name: 'DashboardView',
  components: {
    Document,
    PictureFilled,
    ChatDotRound,
    Setting,
    PictureRounded,
    ChatLineRound
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const adminInfo = ref({})

    const activeMenu = computed(() => route.path)

    onMounted(() => {
      // 从localStorage获取管理员信息
      const adminInfoStr = localStorage.getItem('admin-info')
      if (adminInfoStr) {
        try {
          adminInfo.value = JSON.parse(adminInfoStr)
        } catch (e) {
          console.error('解析管理员信息失败', e)
        }
      }
    })

    const handleCommand = (command) => {
      if (command === 'logout') {
        ElMessageBox.confirm('确定要退出登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // 清除token和管理员信息
          localStorage.removeItem('admin-token')
          localStorage.removeItem('admin-info')
          ElMessage.success('已退出登录')
          router.push('/login')
        }).catch(() => {})
      }
    }

    return {
      activeMenu,
      adminInfo,
      handleCommand
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  color: #bfcbd9;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 18px;
  color: #fff;
  background-color: #263445;
}

.sidebar-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-right span {
  margin-right: 15px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>