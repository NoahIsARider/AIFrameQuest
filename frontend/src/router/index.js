import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Hot from '../views/Hot.vue';
import My from '../views/My.vue';
import Login from '../views/Login.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/hot',
    name: 'Hot',
    component: Hot,
    meta: { requiresAuth: true }
  },
  {
    path: '/my',
    name: 'My',
    component: My,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    // 需要登录但未登录，重定向到登录页
    next({ name: 'Login' })
  } else if (to.name === 'Login' && token) {
    // 已登录但访问登录页，重定向到首页
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router;