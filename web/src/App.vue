<script lang="ts" setup>
import SiteMenu from '@/views/SiteMenu.vue'

</script>
<template>
  <div class="common-layout full-height">
    <el-container>
      <el-aside width="16em" class="full-height gray-bg">
        <SiteMenu />
      </el-aside>
      <el-main class="full-height no-padding">
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.gray-bg {
  --el-menu-bg-color: #fcfcfc;
  background-color: var(--el-menu-bg-color);
}
</style>
