import { createRouter, createWebHistory } from 'vue-router'
import AllSitePages from '@/views/pages/AllSitePages.vue'
import MainView from '@/views/MainView.vue'
import { inject } from 'vue'
import { user_key } from '@/key'
import { getUserStatus } from '@/sdk/sdk.gen'

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
          path: 'category/:category_id(\\d+)',
          name: 'category',
          props: true,
          component: () => import('@/views/pages/CategoryPages.vue'),
          children: [page_rule('category')]
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
          path: 'user',
          name: 'UserPage',
          component: () => import('@/views/pages/UserPage.vue'),
          children: [
            {
              path: 'subscriptions',
              name: 'subscriptions',
              component: () => import('@/views/pages/SubscriptionsPage.vue')
            },
            {
              path: 'keywords',
              name: 'keywords',
              component: () => import('@/views/pages/KeywordsPage.vue')
            }
          ]
        },
        {
          path: 'manage',
          name: 'manage',
          component: () => import('@/views/pages/ManagePages.vue'),
          children: [page_rule('manage')]
        },
        {
          path: 'help',
          name: 'help',
          component: () => import('@/views/pages/HelpPage.vue')
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
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    }
  ]
})

router.beforeEach(async (to, from) => {
  from // eslint-disable-line
  const user = inject(user_key)!
  if (to.name != 'login' && to.name != 'register' && to.name != '404' && !user.value) {
    const { data } = await getUserStatus()
    if (!data!.is_login) router.push({ name: 'login', query: { next: to.fullPath } })
    else user.value = data!.user!
  } else if (to.name == 'login' && user.value) {
    if (to.query.next) router.push(to.query.next as string)
    else router.push({ name: 'home' })
  }
})

export default router
