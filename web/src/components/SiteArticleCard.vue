<template>
  <div class="site-article-container">
    <div v-for="(site_pages, site) in groupedPages" :key="site" class="site-card">
      <ElCard shadow="hover" class="site-el-card">
        <template #header>
          <div class="site-card-header">
            <ElAvatar
              v-if="site_pages[0].site_icon"
              size="small"
              :src="site_pages[0].site_icon"
              class="right-gap"
            />
            <span>{{ site }}</span>
          </div>
        </template>
        <ElScrollbar height="300px">
          <ul v-infinite-scroll="load" :infinite-scroll-distance="2" class="infinite-list">
            <div v-for="page in site_pages" :key="page.id" class="article-item">
              <router-link
                :to="{
                  name: `${String($route.matched[1].name)}-page`,
                  params: { page_id: page.id }
                }"
                class="article-title"
              >
                {{ page.title }}
              </router-link>
              <div class="article-time">
                <NConfigProvider :locale="zhCN" :date-locale="dateZhCN">
                  {{ showTime(page.publish_time) }}
                </NConfigProvider>
              </div>
            </div>
          </ul>
        </ElScrollbar>
      </ElCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { zhCN, dateZhCN, NConfigProvider } from 'naive-ui'
import { ElAvatar, ElCard, ElScrollbar } from 'element-plus'
import type { PageItem } from '@/sdk'
import { showTime } from '@/utils/timeUtils'
import { useInfiniteScroll } from '@/utils/useInfiniteScroll'

const props = defineProps<{ pages: PageItem[] }>()

const { load } = useInfiniteScroll(10)

const groupedPages = computed(() => {
  const groups: Record<string, PageItem[]> = {}
  props.pages.forEach((page) => {
    if (!groups[page.site]) {
      groups[page.site] = []
    }
    groups[page.site].push(page)
  })
  return groups
})
</script>

<style scoped>
.site-article-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1em;
  padding: 1em;
}

.site-card {
  width: 300px;
}

.site-el-card {
  height: 400px; /* 与 ArticleCard.vue 一致的高度 */
  border-radius: 15px; /* 设置圆角 */
  background-color: rgba(255, 255, 255, 0.7); /* 设置背景颜色为半透明的白色 */
}

.site-card-header {
  font-size: 1.2em;
  display: inline-flex;
  align-items: center;
}

.right-gap {
  margin-right: 0.5em;
}

.article-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5em 0;
  border-bottom: 1px solid #f0f0f0;
}

.article-title {
  font-weight: bold;
  color: #000;
  text-decoration: none;
}

.article-time {
  font-size: 0.9em;
  color: #888;
}
</style>
