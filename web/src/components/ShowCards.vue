<script setup lang="ts">
import { ref, defineProps, watch } from 'vue'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import { server } from '@/const'

const props = defineProps<{ pages: PageItem[]; title: string; loading: Boolean }>()
let searchKeyword = ref('')
let filteredPages = ref<PageItem[]>(props.pages)

watch(() => props.pages, (newPages) => {
  filteredPages.value = newPages
})

watch(searchKeyword, (newKeyword) => {
  if (newKeyword) {
    // filteredPages.value = props.pages.filter(page => page.title.includes(newKeyword))
    let regex = new RegExp([...newKeyword].join('.*'), 'g')
    filteredPages.value = props.pages.filter(page => regex.test(page.title))
  } else {
    filteredPages.value = props.pages
  }
})

</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ title }}</h1>
        <SearchInput @update:searchQuery="searchKeyword = $event"></SearchInput>
        <!-- <SearchInput v-model="searchKeyword"></SearchInput> -->
        <slot></slot>
      </div>
      <el-scrollbar v-if="pages && pages.length" v-loading="loading" @scroll="$emit('scroll', $event)">
        <div class="container-grid">
          <ArticleCard v-for:="page in filteredPages" :page="page"></ArticleCard>
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
  justify-content: left;
  align-items: center;
}
</style>
