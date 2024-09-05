<script setup lang="ts">
import { defineProps } from 'vue'
import type { PageItem } from '@/api_interface'
import { is_bookmarked } from '@/bookmark'
defineProps<{ page: PageItem }>()

import { NTime, zhCN, dateZhCN, NConfigProvider } from 'naive-ui'
import BookmarkSvg from './svg/BookmarkSvg.vue'
</script>

<template>
  <div class="card-container">
    <router-link
      :to="{ name: `${String($route.matched[0].name)}-page`, params: { page_id: page.id } }"
    >
      <el-card class="small-card" shadow="hover">
        <template #header>
          <div class="small-card-header">
            <el-avatar size="small" :src="page.site_icon" v-if="page.site_icon" class="right-gap" />
            <span>{{ page.site }}</span>
            <el-tooltip content="已加入书签" effect="light">
              <BookmarkSvg v-show="is_bookmarked(page.id)" fill="#FFD700"></BookmarkSvg>
            </el-tooltip>
          </div>
        </template>
        <h3 class="small-card-body">{{ page.title }}</h3>
        <template #footer>
          <div class="small-card-footer">
            <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
              <n-time :time="new Date(page.publish_time)" type="relative" />
            </n-config-provider>
          </div>
        </template>
      </el-card>
    </router-link>
  </div>
</template>

<style scoped>
.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20em, 1fr));
  /* 固定卡片宽度为30em */
  grid-auto-rows: 15em;
  /* 固定卡片高度为15em */
  gap: 2em;
  /* 控制卡片之间的间距 */
  padding: 1em;
  /* 增加容器内边距 */
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
  background-color: rgba(255, 255, 255, 0.7); /* 设置背景颜色为半透明的白色 */
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
</style>
