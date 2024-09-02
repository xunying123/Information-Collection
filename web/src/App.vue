<script lang="ts" setup>
import SiteMenu from '@/views/SiteMenu.vue'
import { useRoute } from 'vue-router'

let route = useRoute()
route.query

import { NLayout, NLayoutSider, NLayoutContent } from 'naive-ui'
</script>
<template>
  <n-layout has-sider class="full-height">
    <n-layout-sider
      collapse-mode="transform"
      :collapsed-width="0"
      width="20em"
      show-trigger="bar"
      bordered
    >
      <SiteMenu class="full-height" />
    </n-layout-sider>
    <n-layout-content>
      <RouterView />
    </n-layout-content>
  </n-layout>
</template>
