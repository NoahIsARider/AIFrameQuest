import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./views/Dashboard.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard/entries'
      },
      {
        path: 'entries',
        name: 'Entries',
        component: () => import('./views/Entries.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'images',
        name: 'Images',
        component: () => import('./views/Images.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'image-review',
        name: 'ImageReview',
        component: () => import('./views/ImageReview.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'comments',
        name: 'Comments',
        component: () => import('./views/Comments.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'entries-uncensored',
        name: 'EntriesUncensored',
        component: () => import('./views/EntriesUncensored.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'suggestions',
        name: 'Suggestions',
        component: () => import('./views/Suggestions.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = localStorage.getItem('admin-token')
  
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router