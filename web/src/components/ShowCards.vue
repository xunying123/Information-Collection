<script setup lang="ts">
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import { search_keyword_key, all_categories_key, all_subjects_key } from '@/key'
import { getCategories } from '@/sdk'

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
const searchKeyword = inject(search_keyword_key)!
const allCategories = inject(all_categories_key)!
const route = useRoute()

let subjects = inject(all_subjects_key)!

// 拆分为独立响应式属性
const selectedCategories = ref<number[]>([])
const selectedTimeRange = ref('all')
const selectedSortOption = ref('time')
const selectedSubjects = ref<number[]>([])

const emit = defineEmits(['sortOptionChanged', 'scroll', 'timeRangeChanged'])

watch(selectedTimeRange, (newTimeRange) => {
  localStorage.setItem('selectedTimeRange', newTimeRange)

  // 计算时间范围并发送到后端
  const now = new Date()
  let timeStart: string | null = null

  if (newTimeRange !== 'all') {
    const days = parseInt(newTimeRange)
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
      timeStart = yesterday.toISOString()
    } else {
      // 其他天数范围
      const startTime = new Date(now)
      startTime.setDate(now.getDate() - days)
      startTime.setHours(0, 0, 0, 0)
      timeStart = startTime.toISOString()
    }
  }

  emit('timeRangeChanged', timeStart)
})

watch(selectedSortOption, (newSortOption) => {
  localStorage.setItem('selectedSortOption', newSortOption)
  emit('sortOptionChanged', newSortOption)
})

watch(selectedCategories, (newCategories) => {
  localStorage.setItem('selectedCategories', JSON.stringify(newCategories))
  window.dispatchEvent(new Event('selectedCategoriesUpdated'))
})

watch(selectedSubjects, (newSubjects) => {
  localStorage.setItem('selectedKeywordCategories', JSON.stringify(newSubjects))
  window.dispatchEvent(new Event('selectedSubjectsUpdated'))
})

const view = ref('card')
const options = computed(() => {
  const showSiteCard =
    route.path.includes('category') ||
    route.path.includes('daliyupdate') ||
    route.path.includes('bookmarks')
  return showSiteCard
    ? [
        { label: '网站卡片', value: 'site' },
        { label: '卡片', value: 'card' },
        { label: '标题列表', value: 'list' }
        // { label: '摘要列表', value: 'excerpt' }
      ]
    : [
        { label: '卡片', value: 'card' },
        { label: '标题列表', value: 'list' }
        // { label: '摘要列表', value: 'excerpt' }
      ]
})

watch(view, (newView) => {
  localStorage.setItem('viewMode', newView)
  if (
    !(
      route.path.includes('category') ||
      route.path.includes('daliyupdate') ||
      route.path.includes('bookmarks')
    )
  ) {
    localStorage.setItem('notCateView', newView)
  }
})

onMounted(() => {
  const savedView = localStorage.getItem('viewMode')
  const savedNotCateView = localStorage.getItem('notCateView')
  const savedSortOption = localStorage.getItem('selectedSortOption')
  const savedTimeRange = localStorage.getItem('selectedTimeRange')

  if (savedView) view.value = savedView
  if (
    !(
      route.path.includes('category') ||
      route.path.includes('daliyupdate') ||
      route.path.includes('bookmarks')
    ) &&
    view.value === 'site'
  ) {
    view.value = savedNotCateView ? savedNotCateView : 'card'
  }
  if (savedSortOption) {
    selectedSortOption.value = savedSortOption
    emit('sortOptionChanged', savedSortOption)
  }

  if (savedTimeRange) {
    selectedTimeRange.value = savedTimeRange

    // 初始化时也触发时间范围变更事件
    const now = new Date()
    let timeStart: string | null = null

    if (savedTimeRange !== 'all') {
      const days = parseInt(savedTimeRange)
      if (days === 1) {
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
        timeStart = yesterday.toISOString()
      } else {
        const startTime = new Date(now)
        startTime.setDate(now.getDate() - days)
        startTime.setHours(0, 0, 0, 0)
        timeStart = startTime.toISOString()
      }
    }

    emit('timeRangeChanged', timeStart)
  }

  const storedKeywordCategories = localStorage.getItem('selectedKeywordCategories')
  if (storedKeywordCategories) {
    selectedSubjects.value = JSON.parse(storedKeywordCategories)
  }

  const fetchCategories = async () => {
    const { data, error } = await getCategories()
    if (error) console.error('获取类别信息失败：', error)
    allCategories.value = data!
  }
  const storedCategories = localStorage.getItem('selectedCategories')
  if (storedCategories) selectedCategories.value = JSON.parse(storedCategories)
  fetchCategories()
})

const filterSidebarRef = ref<any>(null)
const openFilter = () => filterSidebarRef.value?.openDrawer?.()
</script>

<template>
  <el-container class="full-height">
    <FilterSidebar
      ref="filterSidebarRef"
      v-model:selectedCategories="selectedCategories"
      v-model:selectedTimeRange="selectedTimeRange"
      v-model:selectedSortOption="selectedSortOption"
      v-model:selectedSubjects="selectedSubjects"
      :allCategories="allCategories"
      :subjects="subjects"
    />
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-button
          type="primary"
          @click="openFilter"
          style="margin-right: 0.8em; line-height: normal"
        >
          <el-icon><Filter /></el-icon>
          <span>筛选</span>
        </el-button>
        <SearchInput @update:searchQuery="searchKeyword = $event" style="width: 16em" />
        <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
      </div>
      <el-scrollbar
        v-if="props.pages && props.pages.length"
        v-loading="props.loading"
        @scroll="$emit('scroll', $event)"
      >
        <div v-if="view === 'card'" class="container-grid">
          <ArticleCard v-for="page in pages" :key="page.id" :page="page" />
        </div>
        <ArticleList :pages="pages" :showExcerpt="false" v-else-if="view === 'list'" />
        <ArticleList :pages="pages" :showExcerpt="true" v-else-if="view === 'excerpt'" />
        <SiteArticleCard :pages="pages" :showExcerpt="true" v-else-if="view === 'site'" />
      </el-scrollbar>
      <el-empty v-else :image-size="200" />
    </el-main>
    <RouterView />
  </el-container>
</template>

<style scoped>
.full-height {
  height: 100vh;
}

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
  justify-content: flex-start;
  align-items: center;
  padding: 1em;
  padding-right: 2em;
  flex-wrap: wrap;
  gap: 12px;
}

.header > :first-child {
  margin-right: auto;
}

.spaced-segmented {
  margin-left: 0.8em;
  width: 12em;
  --el-segmented-item-selected-bg-color: #79bbff;
  --el-border-radius-base: 16px;
}

.header > h1 {
  margin: 0.2em;
}

/* .el-scrollbar {
  height: calc(100vh - 120px);
} */

.el-main {
  display: flex;
  flex-direction: column;
  padding: 0;
}
</style>
