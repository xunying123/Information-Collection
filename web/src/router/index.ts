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
          path: 'page/:page_id',
          name: 'site-page',
          props: true,
          component: () => import('@/views/ArticleView.vue')
        }
      ]
    },
    {
      path: '/bookmarks',
      name: 'bookmarks',
      component: () => import('@/views/BookmarksView.vue'),
      children: [
        {
          path: 'page/:page_id',
          name: 'bookmarks-page',
          props: true,
          component: () => import('@/views/ArticleView.vue')
        }
      ]
    }
  ]
})

export default router
