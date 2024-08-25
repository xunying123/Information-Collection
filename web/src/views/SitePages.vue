<script setup lang="ts">
import { server } from '@/const'
import { ref, watch } from 'vue'
import ArticleCard from '@/components/ArticleCard.vue'
import type { SiteQuery } from '@/interface'
import { useRoute } from 'vue-router'
import { bookmarks } from '@/bookmark'

const props = defineProps({
  site_id: String
})

let site = ref<SiteQuery>({
  id: 0,
  name: '',
  url: '',
  category: '',
  cate_id: 0,
  pages: []
})

async function updatePages() {
  site.value = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [] }
  if (!props.site_id) return
  site.value = await fetch(`${server}/site/${props.site_id}`).then((r) => r.json())
  // load.close()
}
watch(props, updatePages)
updatePages()

function reset_bookmarks() {
  localStorage.clear()
}

const route = useRoute()
const showBookmarks = ref(route.name == 'bookmarks')
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height TD" v-loading="site.id == 0">
      <div class="header">
        <h1 class="site-name">{{ site.name }}</h1>
      </div>
      <el-scrollbar>
        <div class="container-grid">
          <ArticleCard v-for:="page in site.pages" :page="page"></ArticleCard>
        </div>
      </el-scrollbar>
    </el-main>
    <router-view />
  </el-container>
</template>

<style scoped>
.container-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 20em);
  gap: 2em;
  padding: 2em;
  justify-content: left;
}

.site-name {
  margin: 1em;
  font-weight: bold;
  font-size: 1.5em;
}

.TD {
  display: grid;
  grid-template-rows: min-content 1fr;
  align-content: start;
  padding: 0;
}
</style>
