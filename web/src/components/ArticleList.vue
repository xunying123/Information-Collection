<template>
  <div class="list-container">
    <!-- <ul v-infinite-scroll="load" :infinite-scroll-distance="2" class="infinite-list"> -->
    <ul
      v-infinite-scroll="load"
      :infinite-scroll-disabled="loading || noMore"
      :infinite-scroll-distance="2"
      class="infinite-list"
    >
      <li
        v-for="page in pages"
        :key="page.id"
        :class="['list-item', { 'with-excerpt': showExcerpt }]"
      >
        <router-link
          :to="{ name: `${String($route.matched[1].name)}-page`, params: { page_id: page.id } }"
          class="block"
        >
          <div class="list-item-card">
            <div class="list-item-content">
              <div class="article-header">
                <span class="list-title">{{ page.title }}</span>
                <router-link
                  :to="`/category/${category_id}/site/${page.site_id}`"
                  class="site-link"
                >
                  {{ page.site }}
                </router-link>
                <div class="article-time">
                  <NConfigProvider :locale="zhCN" :date-locale="dateZhCN">
                    {{ showTime(page.publish_time) }}
                  </NConfigProvider>
                </div>
              </div>
              <el-tooltip content="已加入书签" effect="light">
                <BookmarkSvg v-show="is_bookmarked(page.id)" fill="#FFD700" class="bookmark-icon" />
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
import { useInfiniteScroll } from '@/utils/useInfiniteScroll'
import BookmarkSvg from './svg/BookmarkSvg.vue'
import { zhCN, dateZhCN, NConfigProvider } from 'naive-ui'

const { load, loading, noMore } = useInfiniteScroll(10)

const {
  pages,
  showExcerpt,
  category_id = 0
} = defineProps<{
  pages: PageItem[]
  showExcerpt: boolean
  category_id?: number
}>()
</script>

<style scoped>
.list-container {
  margin-top: 2em;
  margin-left: 3em;
  margin-right: 3em;
}

.list-item {
  margin-bottom: 0;
  padding: 0;
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
  border: 0.2px solid #d9ecff;
  border-top: 0;
  border-left: 0;
  border-right: 0;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition:
    box-shadow 0.3s ease,
    transform 0.3s ease;
  height: 100%;
}

.list-item-content {
  display: grid;
  align-items: center;
  height: 100%;
}

.list-title {
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

/* 主要修改：article-header 使用 grid, 三列：标题 站点 时间 */
.article-header {
  display: grid;
  grid-template-columns: 1fr auto 64px;
  align-items: center;
  height: 1.8em;
  gap: 0.5em;
}

/* 站点在第二列，右对齐 */
.site-link {
  grid-column: 2;
  justify-self: end;
  white-space: nowrap;
  color: #337ecc;
  text-decoration: none;
}

/* 时间在第三列，固定宽度并右对齐 */
.article-time {
  grid-column: 3;
  justify-self: end;
  width: 64px;
  text-align: right;
  font-size: 0.9em;
  color: #888;
  margin-right: 0.2em;
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

.infinite-list {
  height: auto;
  padding: 0;
  margin: 0;
  list-style: none;
  border-radius: 6px;
  background-color: #fff;
  max-width: 56em;
  padding-top: 0.8em;
}

@media screen and (max-width: 768px) {
  .list-container {
    margin-left: 0.5em;
    margin-right: 0.5em;
  }
  .infinite-list {
    width: calc(100vw - 1em);
  }
}
</style>
