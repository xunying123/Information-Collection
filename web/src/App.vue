<script lang="ts" setup>
import SiteMenu from '@/views/SiteMenu.vue'
import { useRoute } from 'vue-router'

let route = useRoute()
route.query

import { NLayout, NLayoutSider, NLayoutContent } from 'naive-ui'
</script>
<template>
  <n-layout has-sider class="full-height">
    <n-layout-sider class="sidebar" collapse-mode="transform" :collapsed-width="0" width="20em" show-trigger="bar" bordered>
      <SiteMenu class="full-height" />
    </n-layout-sider>
    <n-layout-content class="content overlay">
      <RouterView />
    </n-layout-content>
  </n-layout>
</template>

<style scoped>
@media (max-width: 768px) {
  .sidebar {
    width: 9em !important;
  }
  .sidebar .full-height {
    padding-left: 10em;
  }
  .content {
    width: 80% !important;
  }
}

.content.overlay {
  background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('https://mc.sjtu.cn/wp-content/uploads/2022/10/%E5%A4%9C%E6%99%9A%E4%B8%9C%E5%A4%A7%E9%97%A8-1024x659.jpg');
  background-size: cover;
  background-position: center;
}
</style>