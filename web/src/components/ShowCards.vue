<script setup lang="ts">
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import { search_keyword_key, all_categories_key } from '@/key'
import { getCategories } from '@/sdk'

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
const searchKeyword = inject(search_keyword_key)!
const allCategories = inject(all_categories_key)!
const route = useRoute()

const filterOptions = ref({
  selectedCategories: [] as number[],
  selectedTimeRange: 'all',
  selectedSortOption: 'time'
})

const filteredPages = ref<PageItem[]>(props.pages)

function filterPages() {
  filteredPages.value = [...props.pages]
  const now = new Date()
  
  if (filterOptions.value.selectedTimeRange !== 'all') {
    const days = parseInt(filterOptions.value.selectedTimeRange)
    let startTime: Date
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
      startTime = yesterday
    } else {
      startTime = new Date(now)
      startTime.setDate(now.getDate() - days)
      startTime.setHours(0, 0, 0, 0)
    }
    filteredPages.value = filteredPages.value.filter(page => {
      const publishTime = new Date(page.publish_time)
      return publishTime >= startTime && publishTime <= now
    })
  }

  if (filterOptions.value.selectedSortOption === 'score') {
    filteredPages.value.sort((a, b) => b.score - a.score)
  } else {
    filteredPages.value.sort(
      (a, b) => new Date(b.publish_time).getTime() - new Date(a.publish_time).getTime()
    )
  }
}

watch(() => props.pages, newPages => {
  filteredPages.value = newPages
  filterPages()
})

watch(() => filterOptions.value.selectedTimeRange, filterPages)
watch(() => filterOptions.value.selectedSortOption, newSortOption => {
  localStorage.setItem('selectedSortOption', newSortOption)
  filterPages()
})

watch(() => filterOptions.value.selectedCategories, newCategories => {
  localStorage.setItem('selectedCategories', JSON.stringify(newCategories))
  window.dispatchEvent(new Event('selectedCategoriesUpdated'))
}, { deep: true })

const view = ref('card')
const options = computed(() => {
  const showSiteCard = route.path.includes('category') || 
                      route.path.includes('daliyupdate') || 
                      route.path.includes('bookmarks')
  return showSiteCard ? [
    { label: '网站卡片', value: 'site' },
    { label: '卡片', value: 'card' },
    { label: '标题列表', value: 'list' },
    { label: '摘要列表', value: 'excerpt' }
  ] : [
    { label: '卡片', value: 'card' },
    { label: '标题列表', value: 'list' },
    { label: '摘要列表', value: 'excerpt' }
  ]
})

watch(view, newView => {
  localStorage.setItem('viewMode', newView)
  if (!(route.path.includes('category') || 
       route.path.includes('daliyupdate') || 
       route.path.includes('bookmarks'))) {
    localStorage.setItem('notCateView', newView)
  }
})

onMounted(() => {
  const savedView = localStorage.getItem('viewMode')
  const savedNotCateView = localStorage.getItem('notCateView')
  const savedSortOption = localStorage.getItem('selectedSortOption')
  if (savedView) view.value = savedView
  if (!(route.path.includes('category') || 
      route.path.includes('daliyupdate') || 
      route.path.includes('bookmarks')) &&
      view.value === 'site') {
    view.value = savedNotCateView ? savedNotCateView : 'card'
  }
  if (savedSortOption) filterOptions.value.selectedSortOption = savedSortOption
  const fetchCategories = async () => {
    const { data, error } = await getCategories()
    if (error) console.error('获取类别信息失败：', error)
    allCategories.value = data!
  }
  const storedCategories = localStorage.getItem('selectedCategories')
  if (storedCategories) filterOptions.value.selectedCategories = JSON.parse(storedCategories)
  fetchCategories()
})

const filterSidebarRef = ref<any>(null)
const openFilter = () => filterSidebarRef.value?.openDrawer?.()
</script>

<template>
  <el-container class="full-height">
    <FilterSidebar ref="filterSidebarRef" v-model:filterOptions="filterOptions" :allCategories="allCategories" />
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <div class="header-right">
          <el-button type="primary" @click="openFilter" style="margin-right:10px; line-height:normal;">
            <el-icon><Filter /></el-icon>
            <span>筛选</span>
          </el-button>
          <SearchInput @update:searchQuery="searchKeyword = $event" />
          <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
        </div>
      </div>
      <el-scrollbar
        v-if="props.pages && props.pages.length"
        v-loading="props.loading"
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
/* 恢复原有样式 */
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

/* 新增调整 */
.el-main {
  padding: 0 !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-scrollbar {
  height: calc(100vh - 120px); /* 保持原有滚动区域高度 */
}
</style>