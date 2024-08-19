import { createRouter, createWebHistory } from 'vue-router'
import EmptyView from '@/views/EmptyView.vue'
import WaitChooseSite from '@/views/WaitChooseSite.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WaitChooseSite
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
      component: () => import('@/views/SitePages.vue'),
      children: [
        {
          path: '',
          name: 'site-home',
          component: EmptyView
        },
        {
          path: 'page/:page_id',
          name: 'page',
          props: true,
          component: () => import('@/views/ArticleView.vue')
        }
      ]
    }
  ]
})

export default router
