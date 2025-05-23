<template>
  <el-drawer v-model="drawerVisible" title="筛选" size="40em">
    <FilterSidebar
      v-model:selected-categories="selected_categories"
      v-model:selected-subjects="selected_subjects"
      v-model:selected-time-range="selected_time_range"
      v-model:current-sort-option="current_sort_option"
    />
  </el-drawer>
  <ShowCards
    v-model:view="view"
    :pages="pages"
    :title="title"
    :loading="loading"
    :category_id="category_id"
    @scroll="handleScroll"
    @wheel="handleWheel"
  >
    <SearchInput style="width: 16em" @update:search-query="search_keyword = $event" />
    <el-button type="primary" @click="drawerVisible = true">
      <el-icon> <Filter /> </el-icon><span>筛选</span>
    </el-button>
  </ShowCards>
</template>

<script setup lang="ts">
import { ref, watch, inject, computed } from 'vue'
import { all_categories_key, all_subjects_key, user_key, type ViewMode } from '@/key'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/utils/useScrollFetch'
import { getPages } from '@/sdk'
import type { PageItem, PageGet, SortType } from '@/sdk'
import { isRequesting, lockRequest, unlockRequest } from '@/utils/useScrollFetch'
import SearchInput from '@/components/SearchInput.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'

const {
  pageType,
  site_id = 0,
  category_id = undefined,
  subject_id = 0
} = defineProps<{
  pageType: 'all' | 'daily' | 'site' | 'category' | 'subject'
  site_id?: number
  category_id?: number
  subject_id?: number
}>()

// 相关对象
const all_categories = inject(all_categories_key)!
const all_subjects = inject(all_subjects_key)!
const category = computed(() => all_categories.value.find((item) => item.id == category_id))
const subject = computed(() => all_subjects.value.find((item) => item.id == subject_id))
const site = computed(() => category.value?.sites.find((item) => item.id == site_id))

// 渲染数据
const user = inject(user_key)!
const pages = ref<PageItem[]>([])
const title = computed(() => {
  switch (pageType) {
    case 'all':
      return '全部文章'
    case 'daily':
      return '每日更新'
    case 'site':
      return site.value?.name || '网站名称'
    case 'category':
      return category.value?.name || '分类名称'
    case 'subject':
      return subject.value?.name || '专题名称'
    default:
      return '未知'
  }
})
const drawerVisible = ref(false)

// 筛选状态管理 - 集中在这个组件
const selected_categories = ref<number[]>([])
const selected_subjects = ref<number[]>([])
const selected_time_range = ref<number>(0)
const current_sort_option = ref<SortType>('time')
const filter_keyword = ref<boolean>(false)
const count = ref<number>(50)
const view = ref<ViewMode>('card')
const search_keyword = ref<string>('')
const loading = ref(true)

const Today = new Date()
Today.setHours(0, 0, 0, 0)

const time_start = computed<Date | null>(
  () => new Date(Today.getTime() - selected_time_range.value * 24 * 60 * 60 * 1000)
)

const request_body = computed<PageGet>(() => ({
  count: count.value,
  filter_user_keyword: filter_keyword.value,
  subscribe: 0,
  sort: current_sort_option.value,
  count_for_each_site: view.value == 'site',
  ...(site_id ? { site: site_id } : {}),
  // category
  ...(selected_categories.value.length > 0 ? { category: selected_categories.value } : {}),
  ...(category_id != null ? { category: category_id } : {}),
  // subject
  ...(selected_subjects.value.length > 0 ? { subject: selected_subjects.value } : {}),
  ...(category.value?.subject_id ? { subject: category.value.subject_id } : {}),
  ...(subject_id ? { subject: subject_id } : {}),
  // time_start
  ...(time_start.value ? { time_start: time_start.value.toISOString() } : {}),
  ...(pageType == 'daily' ? { time_start: Today.toISOString() } : {}),
  // search
  ...(search_keyword.value
    ? { search_title: search_keyword.value, search_content: search_keyword.value }
    : {})
}))

function fetchPages() {
  if (!user.value?.group) return
  if (isRequesting.value) {
    return
  }
  lockRequest()
  let done = false
  setTimeout(() => {
    if (!done) loading.value = true
  }, 200)

  getPages({ body: request_body.value })
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

const { handleScroll, handleWheel } = useScrollFetch((val) => (count.value = val))

watch(request_body, fetchPages)
</script>
