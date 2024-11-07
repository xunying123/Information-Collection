<template>
    <div class="site-article-container">
      <div v-for="(pages, site) in groupedPages" :key="site" class="site-card">
        <el-card shadow="hover" class="site-el-card">
          <template #header>
            <div class="site-card-header">
              <el-avatar size="small" :src="pages[0].site_icon" v-if="pages[0].site_icon" class="right-gap" />
              <span>{{ site }}</span>
            </div>
          </template>
          <el-scrollbar height="300px">
            <div v-for="page in pages" :key="page.id" class="article-item">
              <router-link
                :to="{ name: `${String($route.matched[1].name)}-page`, params: { page_id: page.id } }"
                class="article-title"
              >
                {{ page.title }}
              </router-link>
              <div class="article-time">
                <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
                  <n-time :time="new Date(page.publish_time)" :type="timeType(page.publish_time)" />
                </n-config-provider>
              </div>
            </div>
          </el-scrollbar>
        </el-card>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps, computed } from 'vue'
  import { NTime, zhCN, dateZhCN, NConfigProvider } from 'naive-ui'
  import { ElAvatar, ElCard, ElScrollbar } from 'element-plus'
  import type { PageItem } from '@/api_interface'
  
  const props = defineProps<{ pages: PageItem[] }>()
  
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
  
  const timeType = (date: string) => {
    const now = new Date()
    const diff = now.getTime() - new Date(date).getTime()
    const diffHours = diff / 1000 / 60 / 60
    return diffHours < 24 ? 'relative' : 'date'
  }
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