<script setup lang="ts">
import { computed } from 'vue'
import type { PageItem } from '@/sdk'
import { is_bookmarked } from '@/bookmark'
import { showTime } from '@/utils/timeUtils'
// defineProps<{ page: PageItem }>()

import { zhCN, dateZhCN, NConfigProvider } from 'naive-ui'
import BookmarkSvg from './svg/BookmarkSvg.vue'

const props = defineProps<{ page: PageItem }>()

const computedShowTime = computed(() => showTime(props.page.publish_time))
</script>

<template>
  <div class="card-container">
    <router-link
      :to="{ name: `${String($route.matched[1].name)}-page`, params: { page_id: page.id } }"
    >
      <el-card class="small-card" shadow="hover">
        <template #header>
          <div class="small-card-header">
            <el-avatar v-if="page.site_icon" size="small" :src="page.site_icon" class="right-gap" />
            <span>{{ page.site }}</span>
            <el-tooltip content="已加入书签" effect="light">
              <BookmarkSvg v-show="is_bookmarked(page.id)" fill="#FFD700" />
            </el-tooltip>
            <NConfigProvider :locale="zhCN" :date-locale="dateZhCN">
              {{ computedShowTime }}
            </NConfigProvider>
          </div>
        </template>
        <h3 class="small-card-body">
          {{ page.title }}
        </h3>
      </el-card>
    </router-link>
  </div>
</template>

<style scoped>
.card-container {
  display: grid;
  /* 定义网格布局 */
  grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
  /* 自动填充列，最小宽度为20em，最大宽度为1fr */
  grid-auto-rows: 12em;
}

@media (max-width: 768px) {
  .card-container {
    grid-auto-rows: 12em;
  }
}

.small-card {
  display: grid;
  grid-template-rows: 40px 1fr 50px;
  width: 100%;
  /* 使卡片宽度填满网格单元 */
  height: 100%;
  /* 使卡片高度填满网格单元 */
  box-sizing: border-box;
  /* 确保padding不会影响卡片的实际尺寸 */
  border-radius: 15px; /* 添加这一行，你可以根据需要调整这个值 */
  background-color: rgba(255, 255, 255, 1); /* 设置背景颜色为半透明的白色 */
}

.small-card-header {
  font-size: 1.1em;
  box-sizing: border-box;
  height: 100%;
  /* 保持与父容器一致的高度 */
  display: flex;
  align-items: center;
  justify-content: left;
  margin-left: -0.5em;
}
.small-card-header > :nth-child(3) {
  margin-left: auto;
}

.small-card-body {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-weight: bold;
  font-size: 15px;
}

.small-card-footer {
  width: 100%;
  box-sizing: border-box;
  align-self: end;
  display: flex;
}

.right-gap {
  margin-right: 0.3em;
}

.infinite-list {
  height: 400px;
  padding: 0;
  margin: 0;
  list-style: none;
}
</style>
