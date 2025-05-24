<script setup lang="ts">
import { watch, onMounted, computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/sdk'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import { useInfiniteScroll } from '@/utils/useInfiniteScroll'
import type { ViewMode } from '@/key'

const props = defineProps<{
  pages: PageItem[]
  title: string
  loading: boolean
  category_id?: number
}>()
const route = useRoute()

// 视图模式管理 - 保留在ShowCards中，因为这是UI展示相关的
const view = defineModel<ViewMode>('view', { default: 'card' })
const options = computed(() => {
  const showSiteCard =
    route.path.match(/category|daliyupdate|bookmarks/) != null && !route.path.includes('site')
  const base_options = [
    { label: '卡片', value: 'card' },
    { label: '列表', value: 'list' }
  ]
  return showSiteCard ? [{ label: '网站卡片', value: 'site' }, ...base_options] : base_options
})

const { load, count } = useInfiniteScroll(10)

watch(view, (newView) => {
  if (!newView) return
  localStorage.setItem('viewMode', newView)
  if (route.path.match(/category|daliyupdate|bookmarks/))
    localStorage.setItem('notCateView', newView)
})

onMounted(() => {
  const savedView = localStorage.getItem('viewMode') as typeof view.value
  const savedNotCateView = localStorage.getItem('notCateView') as typeof view.value
  view.value =
    savedView ||
    (route.path.match(/category|daliyupdate|bookmarks/) ? 'site' : null) ||
    savedNotCateView ||
    'card'
})
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-segmented v-model="view" :options="options" class="spaced-segmented" />
        <slot />
      </div>
      <template v-if="props.pages && props.pages.length">
        <el-scrollbar v-if="view != 'site'" v-loading="props.loading">
          <div
            v-if="view === 'card'"
            v-infinite-scroll="load"
            class="container-grid"
            :infinite-scroll-distance="2"
          >
            <ArticleCard v-for="page in pages" :key="page.id" :page="page" />
          </div>
          <ArticleList
            v-else-if="view == 'list' || view == 'excerpt'"
            v-model:count="count"
            :pages="pages"
            :show-excerpt="view == 'excerpt'"
            :category_id="props.category_id"
          />
        </el-scrollbar>
        <SiteArticleCard v-else v-model:count="count" :pages="pages" :show-excerpt="true" />
      </template>
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
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap;
  padding: 1em;
  padding-right: 2em;
  gap: 12px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  --el-button-bg-color: #79bbff !important;
}

.header > h1:first-child {
  margin: 0.2em;
  margin-right: auto;
}

.spaced-segmented {
  margin-left: 0.8em;
  --el-segmented-item-selected-bg-color: #79bbff;
  --el-border-radius-base: 16px;
}

.el-main {
  display: flex;
  flex-direction: column;
  padding: 0;
}
</style>
