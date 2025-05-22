<script setup lang="ts">
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/sdk'
import SearchInput from '@/components/SearchInput.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import { user_key, search_keyword_key, all_categories_key, all_subjects_key } from '@/key'
import { getCategories } from '@/sdk'

const props = defineProps<{
  pages: PageItem[]
  title: string
  loading: boolean
  category_id?: String
}>()
const searchKeyword = inject(search_keyword_key)!
const allCategories = inject(all_categories_key)!
const route = useRoute()

const user = inject(user_key)!
let subjects = inject(all_subjects_key)!

// 仅保留滚动事件
defineEmits(['scroll', 'wheel'])

// 视图模式管理 - 保留在ShowCards中，因为这是UI展示相关的
const view = ref<'card' | 'site' | 'list' | 'excerpt'>('card')
const options = computed(() => {
  const showSiteCard = route.path.match(/category|daliyupdate|bookmarks/) != null
  const base_options = [
    { label: '卡片', value: 'card' },
    { label: '列表', value: 'list' }
  ]
  return showSiteCard ? [{ label: '网站卡片', value: 'site' }, ...base_options] : base_options
})

watch(view, (newView) => {
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

const fetchCategories = async () => {
  if (!user!.value?.group) {
    return
  }
  const { data, error } = await getCategories()
  if (error) console.error('获取类别信息失败：', error)
  allCategories.value = data!
}
onMounted(fetchCategories)

const filterSidebarRef = ref<any>(null)
const openFilter = () => filterSidebarRef.value?.openDrawer?.()
</script>

<template>
  <el-container class="full-height">
    <FilterSidebar ref="filterSidebarRef" :allCategories="allCategories" :subjects="subjects" />
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-button type="primary" @click="openFilter"
          ><el-icon>
            <Filter /> </el-icon
          ><span>筛选</span></el-button
        >
        <SearchInput @update:searchQuery="searchKeyword = $event" style="width: 16em" />
        <el-segmented v-model="view" :options="options" class="spaced-segmented" />
      </div>
      <template v-if="props.pages && props.pages.length">
        <el-scrollbar
          v-if="view != 'site'"
          v-loading="props.loading"
          @scroll="$emit('scroll', $event)"
          @wheel="$emit('wheel', $event)"
        >
          <div v-if="view === 'card'" class="container-grid">
            <ArticleCard v-for="page in pages" :key="page.id" :page="page" />
          </div>
          <ArticleList
            :pages="pages"
            :showExcerpt="view == 'excerpt'"
            :category_id="props.category_id"
            v-else-if="view == 'list' || view == 'excerpt'"
          />
        </el-scrollbar>
        <SiteArticleCard v-else :pages="pages" :showExcerpt="true" />
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
