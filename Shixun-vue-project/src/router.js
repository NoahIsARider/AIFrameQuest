import { createRouter, createWebHistory } from 'vue-router';
import PostList from './components/PostList.vue';
import PostDetail from './components/PostDetail.vue';
import My from './views/My.vue';
import Hot from './views/Hot.vue';
import Result from './views/Result.vue';
import Login from './views/Login.vue';

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
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;