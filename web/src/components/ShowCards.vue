<script setup lang="ts">
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import { user_key, search_keyword_key, all_categories_key, all_subjects_key } from '@/key'
import { getCategories } from '@/sdk'

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
const searchKeyword = inject(search_keyword_key)!
const allCategories = inject(all_categories_key)!
const route = useRoute()

const user = inject(user_key)!
let subjects = inject(all_subjects_key)!

// 仅保留滚动事件
const emit = defineEmits(['scroll', 'wheel'])
emit

// 视图模式管理 - 保留在ShowCards中，因为这是UI展示相关的
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
        { label: '列表', value: 'list' }
      ]
    : [
        { label: '卡片', value: 'card' },
        { label: '列表', value: 'list' }
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

  const fetchCategories = async () => {
    if (!user!.value?.group) {
      return
    }
    const { data, error } = await getCategories()
    if (error) console.error('获取类别信息失败：', error)
    allCategories.value = data!
  }
  fetchCategories()
})

const filterSidebarRef = ref<any>(null)
const openFilter = () => filterSidebarRef.value?.openDrawer?.()
</script>

<template>
  <el-container class="full-height">
    <FilterSidebar
      ref="filterSidebarRef"
      :allCategories="allCategories"
      :subjects="subjects"
    />
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-button
          type="primary"
          @click="openFilter"
          style="
            margin-right: 0.8em;
            line-height: normal;
            --el-button-bg-color: #79bbff;
            --el-button-border-color: #79bbff;
          "
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
        @wheel="$emit('wheel', $event)"
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
  --el-button-bg-color: #79bbff !important;
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

.el-main {
  display: flex;
  flex-direction: column;
  padding: 0;
}
</style>