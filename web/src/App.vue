<script lang="ts" setup>
import SiteMenu from '@/views/SiteMenu.vue'
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

</script>
<template>  
  <el-container class="common-layout full-height">
    <splitpanes vertical>
      <pane max-size="15">
          <SiteMenu />
      </pane>
      <pane>
        <el-main class="full-height no-padding main">
          <RouterView />
        </el-main>
      </pane>
    </splitpanes>
  </el-container>
</template>

<style scoped>

.gray-bg {
  --el-menu-bg-color: #fcfcfc;
  background-color: var(--el-menu-bg-color);
}
.splitpanes {
  /* background: linear-gradient(-45deg, rgba(200, 22, 30, 1), rgba(200, 22, 30, 0.9), rgba(200, 22, 30, 0.8), rgba(200, 22, 30, 1)); */
  /* background: linear-gradient(-45deg, rgba(200, 22, 30, 0.6), rgba(200, 22, 30, 0.5)); */
  background: linear-gradient(180deg, #F2F2F2, #FFFFFF);
}

.splitpanes__pane {
  box-shadow: 0 0 5px rgba(0, 0, 0, .2) inset;
    
}
</style>
