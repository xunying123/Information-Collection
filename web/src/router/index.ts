import { createRouter, createWebHistory } from 'vue-router'
import AllSitePages from '@/views/pages/AllSitePages.vue'
import MainView from '@/views/MainView.vue'
import { server } from '@/const'
import { inject } from 'vue'
import { user_key } from '@/key'

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
      name: 'root',
      component: MainView,
      children: [
        {
          path: '',
          name: 'home',
          component: AllSitePages,
          children: [page_rule('home')]
        },
        {
          path: 'daliyupdate',
          name: 'daliyupdate',
          component: () => import('@/views/pages/DailyUpdatePages.vue'),
          children: [page_rule('daliyupdate')]
        },
        {
          path: 'site/:site_id(\\d+)',
          name: 'site',
          props: true,
          component: () => import('@/views/pages/SitePages.vue'),
          children: [page_rule('site')]
        },
        {
          path: 'bookmarks',
          name: 'bookmarks',
          component: () => import('@/views/pages/BookmarksPages.vue'),
          children: [page_rule('bookmarks')]
        },
        {
          path: 'managesites',
          name: 'managesites',
          component: () => import('@/views/pages/ManageSitesPages.vue'),
          children: [page_rule('managesites')]
        }
      ]
    },
    {
      path: '/404',
      name: '404',
      component: () => import('@/views/404Error.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    }
  ]
})

router.beforeEach(async (to, from) => {
  from // eslint-disable-line
  const user = inject(user_key)!
  if (to.name != 'login' && to.name != '404' && !user.value) {
    const data = await fetch(`${server}/user/me`).then((res) => res.json())
    if (data.code == 0) user.value = data.user
    else router.push({ name: 'login', query: { next: to.fullPath } })
  } else if (to.name == 'login' && user.value) {
    if (to.query.next) router.push(to.query.next as string)
    else router.push({ name: 'home' })
  }
})

export default router
