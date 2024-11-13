<script setup lang="ts">
import { ref, defineProps, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'

import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
let searchKeyword = ref('')
let filteredPages = ref<PageItem[]>(props.pages)
let selectedCategories = ref<string[]>([])

function filterPages() {
  if (searchKeyword.value) {
    let regex = new RegExp([...searchKeyword.value].join('.*'), 'g')
    filteredPages.value = props.pages.filter((page) => regex.test(page.title))
  } else {
    filteredPages.value = props.pages
  }
  if (selectedCategories.value.length > 0) {
    filteredPages.value = filteredPages.value.filter((page) =>
      selectedCategories.value.includes(page.category)
    )
  }
}

watch(
  () => props.pages,
  (newPages) => {
    filteredPages.value = newPages
    filterPages()
  }
)

watch(searchKeyword, filterPages)
watch(selectedCategories, filterPages)

const allCategories = computed(() => {
  let categories = new Set<string>()
  props.pages.forEach((page) => {
    categories.add(page.category)
  })
  return categories
})
const showChooseCate = computed(() => allCategories.value.size > 1)

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
})
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ title }}</h1>
        <el-checkbox-group
          v-model="selectedCategories"
          v-if="showChooseCate"
          style="margin-right: 20px"
        >
          <el-checkbox-button v-for="cate in allCategories" :key="cate" :label="cate">
            {{ cate }}
          </el-checkbox-button>
        </el-checkbox-group>
        <SearchInput @update:searchQuery="searchKeyword = $event"></SearchInput>
        <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
        <slot></slot>
      </div>
      <el-scrollbar
        v-if="pages && pages.length"
        v-loading="loading"
        @scroll="$emit('scroll', $event)"
      >
        <div v-if="view === 'card'" class="container-grid">
          <article-card v-for="page in filteredPages" :key="page.id" :page="page" />
        </div>
        <article-list :pages="filteredPages" :showExcerpt="false" v-else-if="view === 'list'" />
        <article-list :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'excerpt'" />
        <site-article-card :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'site'" />
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
