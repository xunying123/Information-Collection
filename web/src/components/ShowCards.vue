<script setup lang="ts">
import { ref, defineProps, watch, onMounted, computed, inject } from 'vue'
import { useRoute } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'

import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import { server } from '@/const'
import { search_keyword_key } from '@/key'

interface Cate {
  id: number
  name: string
}

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
let searchKeyword = inject(search_keyword_key)!
let filteredPages = ref<PageItem[]>(props.pages)
let selectedCategories = ref<Cate[]>([])

function filterPages() {
  filteredPages.value = props.pages
  if (selectedCategories.value.length > 0) {
    filteredPages.value = filteredPages.value.filter((page) =>
      selectedCategories.value.some((category) => category.id === page.cate_id)
    )
  }
  if (selectedTimeRange.value !== 'all') {
    const days = parseInt(selectedTimeRange.value)
    const now = new Date()
    let startTime

    if (days === 1) {
      const yesterday = new Date(now)
      const day = now.getDay()
      if (day === 1) {
        // 如果今天是周一
        yesterday.setDate(now.getDate() - 3) // 上一个工作日是周五
      } else if (day === 0) {
        // 如果今天是周日
        yesterday.setDate(now.getDate() - 2) // 上一个工作日是周五
      } else {
        yesterday.setDate(now.getDate() - 1) // 其他情况，上一个工作日是昨天
      }
      yesterday.setHours(0, 0, 0, 0)
      startTime = yesterday
    } else {
      startTime = new Date(now)
      startTime.setDate(now.getDate() - days)
      startTime.setHours(0, 0, 0, 0)
    }

    filteredPages.value = filteredPages.value.filter((page) => {
      const publishTime = new Date(page.publish_time)
      return publishTime >= startTime && publishTime <= now
    })
  }
}

watch(
  () => props.pages,
  (newPages) => {
    filteredPages.value = newPages
    filterPages()
  }
)

const timeOptions = [
  { label: '全部', value: 'all' },
  { label: '1天内', value: '1' },
  { label: '7天内', value: '7' },
  { label: '30天内', value: '30' },
  { label: '一年内', value: '365' }
]
const selectedTimeRange = ref('all')

watch(selectedCategories, filterPages)
watch(selectedTimeRange, filterPages)

const allCategories = ref(new Set<Cate>())

const showChooseCate = computed(() => route.path === '/')

const view = ref('card')
const showSiteCard = computed(
  () =>
    route.path.includes('category') ||
    route.path.includes('daliyupdate') ||
    route.path.includes('bookmarks')
)
// const showSiteCard = computed(() => !route.path.includes('site'))

let options = computed(() => {
  if (showSiteCard.value)
    return [
      { label: '网站卡片', value: 'site' },
      { label: '卡片', value: 'card' },
      { label: '标题列表', value: 'list' },
      { label: '摘要列表', value: 'excerpt' }
    ]
  else
    return [
      { label: '卡片', value: 'card' },
      { label: '标题列表', value: 'list' },
      { label: '摘要列表', value: 'excerpt' }
    ]
})

const route = useRoute()

watch(view, (newView) => {
  localStorage.setItem('viewMode', newView)
  if (!showSiteCard.value) {
    localStorage.setItem('notCateView', newView)
  }
})

onMounted(() => {
  const savedView = localStorage.getItem('viewMode')
  const savedNotCateView = localStorage.getItem('notCateView')
  if (savedView) {
    view.value = savedView
  }
  if (!showSiteCard.value && view.value === 'site') {
    view.value = savedNotCateView ? savedNotCateView : 'card'
  }
  try {
    fetch(`${server}/category`)
      .then((res) => res.json())
      .then((data) => {
        allCategories.value = new Set(data)
      })
  } catch (error) {
    console.error('获取类别信息失败：', error)
  }
})
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-checkbox-group
          v-model="selectedCategories"
          v-if="showChooseCate"
          style="margin-right: 20px"
        >
          <el-checkbox-button v-for="cate in allCategories" :key="cate" :value="cate">
            {{ cate.name }}
          </el-checkbox-button>
        </el-checkbox-group>
        <el-segmented
          v-model="selectedTimeRange"
          :options="timeOptions"
          style="margin-right: 20px"
        />
        <SearchInput @update:searchQuery="searchKeyword = $event" />
        <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
        <slot></slot>
      </div>
      <el-scrollbar
        v-if="pages && pages.length"
        v-loading="loading"
        @scroll="$emit('scroll', $event)"
      >
        <div v-if="view === 'card'" class="container-grid">
          <ArticleCard v-for="page in filteredPages" :key="page.id" :page="page" />
        </div>
        <ArticleList :pages="filteredPages" :showExcerpt="false" v-else-if="view === 'list'" />
        <ArticleList :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'excerpt'" />
        <SiteArticleCard :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'site'" />
      </el-scrollbar>
      <el-empty v-else :image-size="200" />
    </el-main>
    <RouterView />
  </el-container>
</template>

<style scoped>
.container-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 20em);
  gap: 2em;
  padding: 2em;
  justify-content: center;
}

h1 {
  margin: 1em;
  font-weight: bold;
  font-size: 1.5em;
}

.top-down {
  display: grid;
  grid-template-rows: min-content 1fr;
  align-content: start;
  padding: 0;
}

.header {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1em;
  padding-right: 2em;
  flex-wrap: wrap;
}

.header > :first-child {
  margin-right: auto;
}

.spaced-segmented {
  margin-left: 1em;
  width: 23em;
}

.header > h1 {
  margin: 0.2em;
}
</style>
