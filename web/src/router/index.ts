import { createRouter, createWebHistory } from 'vue-router'
import AllSitePages from '@/views/pages/AllSitePages.vue'

const page_rule = (name: string) => {
  return {
    path: 'page/:page_id(\\d+)',
    name: `${name}-page`,
    props: true,
    component: () => import('@/views/ArticleView.vue')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AllSitePages,
      children: [page_rule('home')]
    },
    {
      path: '/404',
      name: '404',
      component: () => import('@/views/404Error.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/site/:site_id(\\d+)',
      name: 'site',
      props: true,
      component: () => import('@/views/pages/SitePages.vue'),
      children: [page_rule('site')]
    },
    {
      path: '/bookmarks',
      name: 'bookmarks',
      component: () => import('@/views/pages/BookmarksPages.vue'),
      children: [page_rule('bookmarks')]
    }
  ]
})

export default router
