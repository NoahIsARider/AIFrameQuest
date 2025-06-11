import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Hot from '../views/Hot.vue';
import My from '../views/My.vue';
import Login from '../views/Login.vue';
import TextSearch from '../views/TextSearch.vue';
import Result from '../views/Result.vue';
import Quiz from '../views/Quiz.vue';
import Rank from '../views/Rank.vue';
import SubmitEntry from '../views/SubmitEntry.vue';
import SubmitSuggestion from '../views/SubmitSuggestion.vue';
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
  },
  {
    path: '/text-search',
    name: 'TextSearch',
    component: TextSearch,
    meta: { requiresAuth: true }
  },
  {
    path: '/result',
    name: 'Result',
    component: Result,
    meta: { requiresAuth: true }
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: Quiz,
    meta: { requiresAuth: true }
  },
  {
    path:'/rank',
    name: 'Rank',
    component: Rank,
    meta: { requiresAuth: true }
  },
  {
    path: '/submit-entry',
    name: 'SubmitEntry',
    component: SubmitEntry,
    meta: { requiresAuth: true }
  },
  {
    path: '/submit-suggestion',
    name: 'SubmitSuggestion',
    component: SubmitSuggestion,
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