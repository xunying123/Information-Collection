<script setup lang="ts">
import { ref, defineProps, watch, onMounted, computed, reactive } from 'vue'
import { useRoute } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import { server } from '@/const'
import { reactify } from '@vueuse/core'
import type { List } from 'lodash'

const props = defineProps<{ pages: PageItem[]; title: string; loading: Boolean }>()
let searchKeyword = ref('')
let filteredPages = ref<PageItem[]>(props.pages)

watch(
  () => props.pages,
  (newPages) => {
    filteredPages.value = newPages
  }
)

watch(searchKeyword, (newKeyword) => {
  if (newKeyword) {
    // filteredPages.value = props.pages.filter(page => page.title.includes(newKeyword))
    let regex = new RegExp([...newKeyword].join('.*'), 'g')
    filteredPages.value = props.pages.filter((page) => regex.test(page.title))
  } else {
    filteredPages.value = props.pages
  }
})

const view = ref('card')

let options = computed(() => {
  if (route.path.includes("category"))
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
  if (!route.path.includes("category")) {
    localStorage.setItem('notCateView', newView)
  }
})


onMounted(() => {
  const savedView = localStorage.getItem('viewMode')
  const savedNotCateView = localStorage.getItem('notCateView')
  if (savedView) {
    view.value = savedView
  }
  if (!route.path.includes("category") && view.value === 'site') {
    view.value = savedNotCateView? savedNotCateView : 'card'
  }
})

</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ title }}</h1>
        <SearchInput @update:searchQuery="searchKeyword = $event"></SearchInput>
        <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
        <slot></slot>
      </div>
      <el-scrollbar v-if="pages && pages.length" v-loading="loading" @scroll="$emit('scroll', $event)">
        <div v-if="view === 'card'" class="container-grid">
          <ArticleCard v-for="page in filteredPages" :key="page.id" :page="page" />
        </div>
        <div v-else-if="view === 'list'">
          <ArticleList :pages="filteredPages" :showExcerpt="false" />
        </div>
        <div v-else-if="view === 'excerpt'">
          <ArticleList :pages="filteredPages" :showExcerpt="true" />
        </div>
        <div v-else-if="view === 'site'">
          <SiteArticleCard :pages="filteredPages" :showExcerpt="true" />
        </div>
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
  padding-right: 2em;
}

.header> :first-child {
  margin-right: auto;
}

.spaced-segmented {
  margin-left: 1em;
  width: 23em;
}
</style>
