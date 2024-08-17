import { createRouter, createWebHistory } from 'vue-router'
import EmptyView from '@/views/EmptyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: EmptyView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/site/:site_id',
      name: 'site',
      props: true,
      component: () => import('@/views/SitePages.vue')
    }
  ]
})

export default router
