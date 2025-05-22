<template>
  <div class="list-container">
    <ul class="list">
      <li
        v-for="page in pages"
        :key="page.id"
        :class="['list-item', { 'with-excerpt': props.showExcerpt }]"
      >
        <router-link
          :to="{ name: `${String($route.matched[1].name)}-page`, params: { page_id: page.id } }"
          class="block"
        >
          <div class="list-item-card">
            <div class="list-item-content">
              <div class="article-header">
                <span class="list-title">{{ page.title }}</span>
                <div class="article-time">
                  <NConfigProvider :locale="zhCN" :date-locale="dateZhCN">
                    {{ showTime(page.publish_time) }}
                  </NConfigProvider>
                </div>
                <router-link
                  :to="`/category/` + String(props.category_id) + `/site/` + page.site_id"
                  class="site-link"
                >
                  {{ page.site }}
                </router-link>
              </div>
              <p
                v-if="props.showExcerpt"
                class="list-excerpt"
                v-html="formatExcerpt(stripMarkdown(page.content))"
              ></p>
              <el-tooltip content="已加入书签" effect="light">
                <BookmarkSvg
                  v-show="is_bookmarked(page.id)"
                  fill="#FFD700"
                  class="bookmark-icon"
                ></BookmarkSvg>
              </el-tooltip>
            </div>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { PageItem } from '@/sdk'
import { is_bookmarked } from '@/bookmark'
import { showTime } from '@/utils/timeUtils'
import BookmarkSvg from './svg/BookmarkSvg.vue'
import { zhCN, dateZhCN, NConfigProvider } from 'naive-ui'

const props = defineProps<{ pages: PageItem[]; showExcerpt: boolean; category_id?: String }>()

function stripMarkdown(content: string): string {
  return content.replace(/[#`*]/g, '')
}

function formatExcerpt(content: string): string {
  return content.substring(0, 100).replace(/\n/g, '<br>') + '...'
}
</script>

<style scoped>
.list-container {
  margin-top: 2em;
  margin-left: 3em;
  margin-right: 3em;
}

.list {
  list-style-type: none;
  /* 去掉列表项左上角的小黑点 */
  padding: 0;
  /* 去掉默认的内边距 */
  margin: 0;
  /* 去掉默认的外边距 */
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 1);
  max-width: 56em;
  padding-top: 0.8em;
}

.list-item {
  margin-bottom: 0em;
  padding: 0px 0;
  width: 100%;
  max-width: 56em;
}

.list-item:not(.with-excerpt) .list-item-card {
  display: flex;
  align-items: center;
}

.list-item:not(.with-excerpt) .list-item-content {
  width: 100%;
}

.list-item-card {
  padding: 6px;
  /* 进一步减少卡片内边距 */
  border: 0.2px solid #d9ecff;
  border-top: 0;
  border-left: 0;
  border-right: 0;
  /* border-radius: 4px; */
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  /* 保持阴影 */
  transition:
    box-shadow 0.3s ease,
    transform 0.3s ease;
  height: 100%;
  /* 保持卡片高度 */
}

.list-item-content {
  display: grid;
  align-items: center;
  height: 100%;
}

.list-title {
  grid-column: 1;
  font-weight: bold;
  color: #333;
  transition: color 0.3s ease;
  margin-left: 1em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 100%;
}

.list-title:hover {
  color: #007bff;
}

.article-header {
  display: grid;
  grid-template-columns: minmax(0, 4fr) minmax(0, 1fr) auto;
  align-items: center;
  height: 1.8em;
  container-type: inline-size;
}

.site-link {
  grid-column: 3;
  padding-right: 1em;
  color: #337ecc;
}

.bookmark-icon {
  margin-left: 4px;
  transition: fill 0.3s ease;
}

.bookmark-icon:hover {
  fill: #ffd700;
}

.list-excerpt {
  margin-top: 4px;
  color: #666;
  font-size: 0.9em;
  line-height: 1.5em;
  max-height: 6em;
  width: 100%;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  white-space: pre-wrap;
}

.article-time {
  display: inline-block;
  font-size: 0.9em;
  color: #888;
  /* margin-left: 1em; */
  justify-self: end;
  grid-column: 2;
  padding-right: 1em;
}

.block {
  display: block;
  max-height: 100%;
}

@container (max-width: 360px) {
  .article-time {
    display: none;
  }
}

@container (max-width: 160px) {
  .site-link {
    display: none;
  }
}
</style>
