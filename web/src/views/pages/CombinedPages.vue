<template>
  <ShowCards
    :pages="pages"
    :title="title"
    :loading="loading"
    @scroll="handleScroll"
    @wheel="handleWheel"
    @sortOptionChanged="handleSortOptionChanged"
    @timeRangeChanged="handleTimeRangeChanged"
  ></ShowCards>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject, provide } from 'vue'
import { all_subjects_key } from '@/key'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'
import {
  // filter_subscribe_key,
  filter_keyword_key,
  search_keyword_key
} from '@/key'
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
// import { tr } from 'element-plus/es/locales.mjs'
const props = defineProps<{
  pageType: 'all' | 'daily' | 'site' | 'category'
  site_id?: String
  category_id?: String
  subject_id?: String
}>()

const EmptySite: Site = { id: 0, name: '', url: '', icon: '' }

let searchKeyword = ref('')
provide(search_keyword_key, searchKeyword)

let subjects = inject(all_subjects_key)!

let pages = ref<PageItem[]>([])
let loading = ref(true)
let title = ref('')
let site = ref<Site>(EmptySite)
let count = ref(props.pageType === 'all' || props.pageType === 'site' ? 50 : 10)

// let filter_subscribe = inject(filter_subscribe_key)!
let filter_keyword = inject(filter_keyword_key)!

let currentSortOption = ref<SortType>('time')
let timeStart = ref<string | null>(null)

const fetchPages = (count: number) => {
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
      body.today = true
      title.value = '每日更新'
      break
    case 'site':
      if (!props.site_id) return
      body.site = Number(props.site_id)
      break
    case 'category':
      if (!props.category_id) return
      body.category = Number(props.category_id)
      body.count_for_each_site = true
      break
  }
  getPages({ body: body })
    .then((res) => res.data)
    .then((data) => {
      pages.value = data!.data!
      done = true
      loading.value = false
      console.log('pages:', pages.value.length)
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
  console.log('site:', data)
  // data.pages = site.value.pages
  site.value = data
}

async function updateCategory() {
  const { data, error } = await getCategory({ path: { cate_id: Number(props.category_id) } })
  if (error) {
    console.error(error)
    return
  }
  title.value = data.name
}

const handleTimeRangeChanged = (start: string | null) => {
  timeStart.value = start
  fetchPages(count.value)
}

const handleSortOptionChanged = (sortOption: SortType) => {
  currentSortOption.value = sortOption
  fetchPages(count.value)
}

const selectedCategories = ref<number[]>([])
const selectedSubjects = ref<number[]>([])

const updateSelectedCategories = () => {
  const storedCategories = localStorage.getItem('selectedCategories')
  if (storedCategories) {
    selectedCategories.value = JSON.parse(storedCategories)
  }
  fetchPages(count.value)
}

const updateSelectedSubjects = () => {
  const storedSubjects = localStorage.getItem('selectedKeywordCategories')
  if (storedSubjects) {
    selectedSubjects.value = JSON.parse(storedSubjects)
  }
  fetchPages(count.value)
}

onMounted(() => {
  const savedSortOption = localStorage.getItem('selectedSortOption')
  if (savedSortOption) {
    currentSortOption.value = savedSortOption as SortType
  }

  const savedTimeRange = localStorage.getItem('selectedTimeRange')
  if (savedTimeRange && savedTimeRange !== 'all') {
    const now = new Date()
    let start: Date
    const days = parseInt(savedTimeRange)

    if (days === 1) {
      // 昨天的特殊处理
      start = new Date(now)
      const day = now.getDay()
      if (day === 1) {
        start.setDate(now.getDate() - 3)
      } else if (day === 0) {
        start.setDate(now.getDate() - 2)
      } else {
        start.setDate(now.getDate() - 1)
      }
      start.setHours(0, 0, 0, 0)
    } else {
      start = new Date(now)
      start.setDate(now.getDate() - days)
      start.setHours(0, 0, 0, 0)
    }

    timeStart.value = start.toISOString()
  }

  fetchPages(count.value)
  if (props.pageType === 'site' && props.site_id) {
    updateSite()
  }
  if (props.pageType === 'category' && props.category_id) {
    updateCategory()
  }

  updateSelectedCategories()
  updateSelectedSubjects()
  window.addEventListener('selectedCategoriesUpdated', updateSelectedCategories)
  window.addEventListener('selectedSubjectsUpdated', updateSelectedSubjects)
})

watch(searchKeyword, () => {
  fetchPages(count.value)
})

watch(
  [() => props.site_id, () => props.category_id, () => props.subject_id],
  ([newSiteId, newCategoryId, newSubjectId]) => {
    if (newSiteId || newCategoryId || newSubjectId) {
      fetchPages(count.value)
      if (props.pageType === 'site' && newSiteId) {
        updateSite()
      }
      if (props.pageType === 'category' && newCategoryId) {
        updateCategory()
      }
    }
  }
)
const { handleScroll, handleWheel } = useScrollFetch(fetchPages, count.value)
</script>
