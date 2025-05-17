import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Hot from '../views/Hot.vue';
import My from '../views/My.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/hot',
    name: 'Hot',
    component: Hot
  },
  {
    path: '/my',
    name: 'My',
    component: My
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;