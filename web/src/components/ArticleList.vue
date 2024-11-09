<template>
  <div class="list-container">
    <ul class="list">
      <li v-for="page in pages" :key="page.id" :class="['list-item', { 'with-excerpt': props.showExcerpt }]">
        <router-link :to="{ name: `${String($route.matched[1].name)}-page`, params: { page_id: page.id } }">
          <div class="list-item-card">
            <div class="list-item-content">
              <div class="article-header">
                <router-link :to="`/site/` + page.site_id">
                  <el-button plain type="info" size="default" style="margin-right: 1em;">{{ page.site }}</el-button>
                </router-link>
                <span class="list-title">{{ page.title }}</span>
                <div class="article-time">
                  <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
                    <n-time :time="new Date(page.publish_time)" :type="timeType(page.publish_time)" />
                  </n-config-provider>
                </div>                
              </div>
              <p v-if="props.showExcerpt" class="list-excerpt" v-html="formatExcerpt(stripMarkdown(page.content))"></p>              
              <el-tooltip content="已加入书签" effect="light">
                <BookmarkSvg v-show="is_bookmarked(page.id)" fill="#FFD700" class="bookmark-icon"></BookmarkSvg>
              </el-tooltip>
            </div>
          </div>
          
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { PageItem } from '@/api_interface'
import { is_bookmarked } from '@/bookmark'
import { timeType } from '@/timeUtils'
import BookmarkSvg from './svg/BookmarkSvg.vue'
import { NTime, zhCN, dateZhCN, NConfigProvider } from 'naive-ui'

const props = defineProps<{ pages: PageItem[], showExcerpt: boolean }>()

function stripMarkdown(content: string): string {
  return content.replace(/[#`*]/g, '');
}

function formatExcerpt(content: string): string {
  return content.substring(0, 100).replace(/\n/g, '<br>') + '...';
}
</script>

<style scoped>
.list-container {
  /* padding: 5em; 减少容器内边距 */
  margin-left: 5em;
}

.list {
  list-style-type: none;
  /* 去掉列表项左上角的小黑点 */
  padding: 0;
  /* 去掉默认的内边距 */
  margin: 0;
  /* 去掉默认的外边距 */
}

.list-item {
  margin-bottom: 1em;
  /* 进一步减少项之间的间距 */
  padding: 4px 0;
  /* 减少项的内边距 */
  height: 4em;
  /* 固定项的高度 */
  width: 100%;
}

.list-item.with-excerpt {
  height: 10em;
  /* 自动调整高度以适应内容 */
}

.list-item-card {
  padding: 6px;
  /* 进一步减少卡片内边距 */
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  /* 进一步减少圆角半径 */
  background-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  /* 保持阴影 */
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  height: 100%;  
  /* 保持卡片高度 */
}

.list-item-card:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  /* 保持悬停时的阴影 */
  transform: translateY(-1px);
  /* 保持悬停时的位移 */
}

.list-item-content {
  display: grid;
  align-items: center;
  height: 100%;
}

.list-title {
  flex-grow: 1;
  font-weight: bold;
  color: #333;
  transition: color 0.3s ease;
}

.list-title:hover {
  color: #007bff;
}

.bookmark-icon {
  margin-left: 4px;
  /* 保持图标左边距 */
  transition: fill 0.3s ease;
}

.bookmark-icon:hover {
  fill: #FFD700;
}

.list-excerpt {
  margin-top: 4px;
  color: #666;
  font-size: 0.9em;
  line-height: 1.5em;
  /* 设置行高 */
  height: 6em;
  /* 固定高度 */
  width: 100%;
  /* 固定宽度，限制每行字符数 */
  overflow: hidden;
  /* 隐藏超出内容 */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  /* 限制行数 */
  white-space: pre-wrap;
  /* 保留换行符 */
}

.article-time {
  display: inline-block;
  font-size: 0.9em;
  color: #888;
  margin-left: 1em;
}
</style>