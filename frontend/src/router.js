import { createRouter, createWebHistory } from 'vue-router';
import PostList from './components/PostList.vue';
import PostDetail from './components/PostDetail.vue';
import My from './views/My.vue';
import Hot from './views/Hot.vue';
import Result from './views/Result.vue';
import Login from './views/Login.vue';
import CreatePost from './views/CreatePost.vue';
import VersionPlan from './views/VersionPlan.vue';

const routes = [
  {
    path: '/Home',
    name: 'Home',
    component: PostList
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetail
  },
  {
    path: '/my',
    name: 'My',
    component: My
  },
  {
    path: '/hot',
    name: 'Hot',
    component: Hot
  },
  {
    path: '/result',
    name: 'Result',
    component: Result
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/create',
    name: 'CreatePost',
    component: CreatePost
  },
  {
    path: '/version-plan',
    name: 'VersionPlan',
    component: VersionPlan
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 全局前置守卫：在每次导航之前执行
router.beforeEach((to, from, next) => {
  // 获取本地存储的token
  const token = localStorage.getItem('token');
  
  // 如果目标路由是登录页
  if (to.path === '/login') {
    // 如果已经有token，说明已登录，重定向到首页
    if (token) {
      next('/home');
    } else {
      // 否则正常进入登录页
      next();
    }
  } else {
    // 如果目标路由不是登录页，检查是否有token
    if (token) {
      // 有token，允许访问
      next();
    } else {
      // 没有token，重定向到登录页
      next('/login');
    }
  }
});

export default router;