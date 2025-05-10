<template>
  <ShowCards
    :pages="pages"
    :title="title"
    :loading="loading"
    @scroll="handleScroll"
    @wheel="handleWheel"
  ></ShowCards>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject, provide } from 'vue'
import { user_key, all_subjects_key } from '@/key'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'
import { filter_keyword_key, search_keyword_key } from '@/key'
import {
  getPages,
  getSite,
  getCategory,
  type PageItem,
  type Site,
  type PageGet,
  type SortType
} from '@/sdk'
import { isRequesting, lockRequest, unlockRequest } from '@/useScrollFetch'

const props = defineProps<{
  pageType: 'all' | 'daily' | 'site' | 'category'
  site_id?: String
  category_id?: String
  subject_id?: String
}>()

const EmptySite: Site = { id: 0, name: '', url: '', icon: '' }

const user = inject(user_key)!

let searchKeyword = ref('')
provide(search_keyword_key, searchKeyword)

let subjects = inject(all_subjects_key)!

let pages = ref<PageItem[]>([])
let loading = ref(true)
let title = ref('')
let site = ref<Site>(EmptySite)
let count = ref(50)

let last_subject_id = ref(-1)

let filter_keyword = inject(filter_keyword_key)!

// 筛选状态管理 - 集中在这个组件
const selectedCategories = ref<number[]>([])
const selectedSubjects = ref<number[]>([])
const selectedTimeRange = ref('all')
const currentSortOption = ref<SortType>('time')
let timeStart = ref<string | null>(null)
let today = ref(new Date(new Date().setHours(0, 0, 0, 0)).toISOString())

// 提供筛选状态给子组件
provide('filterState', {
  selectedCategories,
  selectedSubjects,
  selectedTimeRange,
  currentSortOption,
  updateCategories: (categories: number[]) => {
    selectedCategories.value = categories
    localStorage.setItem('selectedCategories', JSON.stringify(categories))
    fetchPages(count.value)
  },
  updateSubjects: (subjects: number[]) => {
    selectedSubjects.value = subjects
    localStorage.setItem('selectedKeywordCategories', JSON.stringify(subjects))
    fetchPages(count.value)
  },
  updateTimeRange: (timeRange: string) => {
    console.log('updateTimeRange', timeRange)
    selectedTimeRange.value = timeRange
    localStorage.setItem('selectedTimeRange', timeRange)
    timeStart.value = calculateTimeStart(timeRange)
    fetchPages(count.value)
  },
  updateSortOption: (sortOption: SortType) => {
    currentSortOption.value = sortOption
    localStorage.setItem('selectedSortOption', sortOption)
    fetchPages(count.value)
  }
})

// 计算时间开始函数 - 移动到这个组件
const calculateTimeStart = (timeRange: string): string | null => {
  if (timeRange === 'all') return null

  const now = new Date()
  let start: string | null = null

  if (timeRange !== 'all') {
    const days = parseInt(timeRange)
    if (days === 1) {
      // 昨天的特殊处理
      const yesterday = new Date(now)
      const day = now.getDay()
      if (day === 1) {
        yesterday.setDate(now.getDate() - 3)
      } else if (day === 0) {
        yesterday.setDate(now.getDate() - 2)
      } else {
        yesterday.setDate(now.getDate() - 1)
      }
      yesterday.setHours(0, 0, 0, 0)
      start = yesterday.toISOString()
    } else {
      // 其他天数范围
      const startTime = new Date(now)
      startTime.setDate(now.getDate() - days)
      startTime.setHours(0, 0, 0, 0)
      start = startTime.toISOString()
    }
  }

  return start
}

const fetchPages = (count: number) => {
  if (!user.value?.group) {
    return
  }
  if (isRequesting.value) {
    return
  }
  lockRequest()
  let done = false
  setTimeout(() => {
    if (!done) {
      loading.value = true
    }
  }, 200)

  let body: PageGet = {
    count: count,
    filter_user_keyword: filter_keyword.value,
    subscribe: 0,
    sort: currentSortOption.value
  }

  if (timeStart.value) {
    body.time_start = timeStart.value
  }

  if (searchKeyword.value) {
    body.search_title = searchKeyword.value
    body.search_content = searchKeyword.value
  }

  if (selectedCategories.value && selectedCategories.value.length > 0) {
    body.category = selectedCategories.value
  }

  if (selectedSubjects.value && selectedSubjects.value.length > 0) {
    body.subject = selectedSubjects.value
  }

  if (props.subject_id) {
    body.subject = Number(props.subject_id)
  }

  switch (props.pageType) {
    case 'all':
      title.value = '全部文章'
      if (props.subject_id) {
        const subject = subjects.value.find((subject) => subject.id === Number(props.subject_id))
        if (subject) {
          title.value = subject.name
        }
      }
      break
    case 'daily':
      body.time_start = today.value
      title.value = '每日更新'
      break
    case 'site':
      if (!props.site_id) return
      body.site = Number(props.site_id)
      if (last_subject_id.value !== -1) {
        body.subject = last_subject_id.value
      }
      break
    case 'category':
      if (!props.category_id) return
      body.category = Number(props.category_id)
      body.count_for_each_site = true
      if (last_subject_id.value !== -1) {
        body.subject = last_subject_id.value
      }
      break
  }

  getPages({ body: body })
    .then((res) => res.data)
    .then((data) => {
      pages.value = data!.data!
      done = true
      loading.value = false
      unlockRequest()
    })
    .catch((err) => {
      console.error('Error fetching data:', err)
      unlockRequest()
    })
}

async function updateSite() {
  const { data, error } = await getSite({ path: { site_id: Number(props.site_id) } })
  if (error) {
    console.error(error)
    return
  }
  title.value = data.name
  site.value = data
}

async function updateCategory() {
  const { data, error } = await getCategory({ path: { cate_id: Number(props.category_id) } })
  if (error) {
    console.error(error)
    return
  }
  title.value = data.name
  last_subject_id.value = data.subject_id ?? -1
}

onMounted(async () => {
  // 从 localStorage 加载筛选条件
  const savedSortOption = localStorage.getItem('selectedSortOption')
  if (savedSortOption) {
    currentSortOption.value = savedSortOption as SortType
  }

  const savedTimeRange = localStorage.getItem('selectedTimeRange')
  if (savedTimeRange) {
    selectedTimeRange.value = savedTimeRange
    timeStart.value = calculateTimeStart(savedTimeRange)
  }

  const storedKeywordCategories = localStorage.getItem('selectedKeywordCategories')
  if (storedKeywordCategories) {
    selectedSubjects.value = JSON.parse(storedKeywordCategories)
  }

  const storedCategories = localStorage.getItem('selectedCategories')
  if (storedCategories) {
    selectedCategories.value = JSON.parse(storedCategories)
  }

  if (props.pageType === 'site' && props.site_id) {
    await updateCategory()
    await updateSite()
  }
  if (props.pageType === 'category' && props.category_id) {
    await updateCategory()
  }
  fetchPages(count.value)
})

watch(searchKeyword, () => {
  fetchPages(count.value)
})

watch(
  [() => props.site_id, () => props.category_id, () => props.subject_id],
  async ([newSiteId, newCategoryId, newSubjectId]) => {
    if (newSiteId || newCategoryId || newSubjectId) {
      if (props.pageType === 'site' && newSiteId) {
        await updateCategory()
        await updateSite()
      }
      if (props.pageType === 'category' && newCategoryId) {
        await updateCategory()
      }
      fetchPages(count.value)
    }
  }
)
const { handleScroll, handleWheel } = useScrollFetch(fetchPages, count.value)
</script>
