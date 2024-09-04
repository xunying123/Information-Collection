<script lang="ts" setup>
import SiteMenu from '@/views/SiteMenu.vue'
import { useRoute } from 'vue-router'

let route = useRoute();
route.query

import { NLayout, NLayoutSider, NLayoutContent } from 'naive-ui'

</script>
<template>
  <n-layout has-sider class="full-height">
    <n-layout-sider class="sidebar" collapse-mode="transform" :collapsed-width="0" width="20em" show-trigger="bar" bordered>
      <SiteMenu class="full-height" />
    </n-layout-sider>
    <n-layout-content class="content">
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
</style>