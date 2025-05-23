<template>
  <SearchInput style="width: 16em" @update:search-query="searchKeyword = $event" />
  <el-drawer v-model="drawerVisible" title="筛选" size="40em">
    <FilterSidebar
      v-model:selected-categories="selectedCategories"
      v-model:selected-subjects="selectedSubjects"
      v-model:selected-time-range="selectedTimeRange"
      v-model:current-sort-option="currentSortOption"
    />
  </el-drawer>
  <ShowCards
    v-model:view="view"
    :pages="pages"
    :title="title"
    :loading="loading"
    :category_id="props.category_id"
    @scroll="handleScroll"
    @wheel="handleWheel"
  >
    <el-button type="primary" @click="drawerVisible = true">
      <el-icon> <Filter /> </el-icon><span>筛选</span>
    </el-button>
  </ShowCards>
</template>

<script setup lang="ts">
import { ref, watch, inject, computed } from 'vue'
import { user_key, type ViewMode } from '@/key'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/utils/useScrollFetch'
import { getPages } from '@/sdk'
import type { PageItem, PageGet, SortType } from '@/sdk'
import { isRequesting, lockRequest, unlockRequest } from '@/utils/useScrollFetch'
import SearchInput from '@/components/SearchInput.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'

const drawerVisible = ref(false)

const props = defineProps<{
  pageType: 'all' | 'daily' | 'site' | 'category'
  site_id?: string
  category_id?: string
  subject_id?: string
}>()

const user = inject(user_key)!

const searchKeyword = ref<string>('')
const pages = ref<PageItem[]>([])
const loading = ref(true)
const title = ref('')
const count = ref(50)

const filter_keyword = ref<boolean>(false)

// 筛选状态管理 - 集中在这个组件
const selectedCategories = ref<number[]>([])
const selectedSubjects = ref<number[]>([])
const selectedTimeRange = ref<number>(0)
const currentSortOption = ref<SortType>('time')
const view = ref<ViewMode>('card')

const Today = new Date()
Today.setHours(0, 0, 0, 0)

const time_start = computed<Date | null>(
  () => new Date(Today.getTime() - selectedTimeRange.value * 24 * 60 * 60 * 1000)
)

const related_subject_id = 0 // TODO

const request_body = computed<PageGet>(() => {
  const body: PageGet = {
    count: count.value,
    filter_user_keyword: filter_keyword.value,
    subscribe: 0,
    sort: currentSortOption.value,
    count_for_each_site: view.value == 'site'
  }
  if (time_start.value) body.time_start = time_start.value.toISOString()
  if (searchKeyword.value) {
    body.search_title = searchKeyword.value
    body.search_content = searchKeyword.value
  }
  if (selectedCategories.value && selectedCategories.value.length > 0)
    body.category = selectedCategories.value
  if (selectedSubjects.value && selectedSubjects.value.length > 0)
    body.subject = selectedSubjects.value
  else if (related_subject_id) body.subject = related_subject_id
  if (props.subject_id) body.subject = Number(props.subject_id)
  switch (props.pageType) {
    case 'daily':
      body.time_start = Today.toISOString()
      break
    case 'site':
      body.site = Number(props.site_id)
    case 'category':
      body.category = Number(props.category_id)
  }
  return body
})

function fetchPages() {
  if (!user.value?.group) return
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
