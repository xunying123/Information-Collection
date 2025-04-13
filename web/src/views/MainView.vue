<script lang="ts" setup>
import { filter_subscribe_key, filter_keyword_key, all_categories_key } from '@/key'
import SiteMenu from '@/views/SiteMenu.vue'
import { NLayout, NLayoutSider, NLayoutContent } from 'naive-ui'
import { provide, ref, computed } from 'vue'
import type { Category } from '@/sdk'

let filter_subscribe = ref(localStorage.getItem('filter_subscribe') === 'true')
provide(filter_subscribe_key, filter_subscribe)

let filter_keyword = ref(localStorage.getItem('filter_keyword') === 'true')
provide(filter_keyword_key, filter_keyword)

let allCategories = ref<Category[]>([])
provide(all_categories_key, allCategories)

// 初始化背景图片 URL，从 localStorage 获取，如果没有则使用默认值
const bgUrl = ref(
  localStorage.getItem('bgUrl') ||
    'https://mc.sjtu.cn/wp-content/uploads/2022/10/%E5%A4%9C%E6%99%9A%E4%B8%9C%E5%A4%A7%E9%97%A8-1024x659.jpg'
)

// 监听自定义事件更新背景图片 URL
window.addEventListener('bgUrlChanged', () => {
  bgUrl.value = localStorage.getItem('bgUrl') || bgUrl.value
})

const bgStyle = computed(() => {
  return `linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('${bgUrl.value}')`
})
</script>
<template>
  <NLayout has-sider class="full-height">
    <NLayoutSider
      class="sidebar"
      collapse-mode="transform"
      :collapsed-width="0"
      width="20em"
      show-trigger="bar"
      bordered
    >
      <SiteMenu class="site-menu" />
    </NLayoutSider>
    <!-- <NLayoutContent class="content overlay"> -->
    <NLayoutContent class="content overlay" :style="{ 'background-image': bgStyle }">
      <RouterView />
    </NLayoutContent>
  </NLayout>
</template>

<style scoped>
@media (max-width: 768px) {
  .sidebar {
    width: 9em !important;
  }
  .site-menu {
    padding-left: 10em;
  }
  .content {
    width: 80% !important;
  }
}

.content.overlay {
  background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)),
    url('https://mc.sjtu.cn/wp-content/uploads/2022/10/%E5%A4%9C%E6%99%9A%E4%B8%9C%E5%A4%A7%E9%97%A8-1024x659.jpg');
  background-size: cover;
  background-position: center;
}
</style>
