import { createRouter, createWebHistory } from 'vue-router';
import PostList from './components/PostList.vue';
import PostDetail from './components/PostDetail.vue';
import My from './views/My.vue';
import Hot from './views/Hot.vue';
import Result from './views/Result.vue';
import Login from './views/Login.vue';
import CreatePost from './views/CreatePost.vue';
import VersionPlan from './views/VersionPlan.vue';
import TextSearch from './views/TextSearch.vue';
import TextSearchResult from './views/TextSearchResult.vue';
import Quiz from './views/Quiz.vue';
import Rank from './views/Rank.vue';
import SubmitEntry from './views/SubmitEntry.vue';
import SubmitSuggestion from './views/SubmitSuggestion.vue';
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
  },
  {
    path: '/text-search',
    name: 'TextSearch',
    component: TextSearch
  },
  {
    path: '/text-search-result',
    name: 'TextSearchResult',
    component: TextSearchResult
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: Quiz,
  },
  {
    path: '/rank',
    name: 'Rank',
    component: Rank
  },
  {
    path: '/submit-entry',
    name: 'SubmitEntry',
    component: SubmitEntry
  },
  {
    path: '/submit-suggestion',
    name: 'SubmitSuggestion',
    component: SubmitSuggestion
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