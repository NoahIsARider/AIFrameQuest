import { createRouter, createWebHistory } from 'vue-router';
import PostList from './components/PostList.vue';
import PostDetail from './components/PostDetail.vue';
import My from './views/My.vue';
import Hot from './views/Hot.vue';
import Result from './views/Result.vue';

const routes = [
  {
    path: '/',
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
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;