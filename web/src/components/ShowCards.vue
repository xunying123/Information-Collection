<script setup lang="ts">
import { defineProps } from 'vue'
import type { PageItem } from '@/api_interface'
defineProps<{ pages: PageItem[]; title: string; loading: Boolean }>()
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ title }}</h1>
        <slot></slot>
      </div>
      <el-scrollbar v-if="pages && pages.length" v-loading="loading">
        <div class="container-grid">
          <ArticleCard v-for:="page in pages" :page="page"></ArticleCard>
        </div>
      </el-scrollbar>
      <el-empty v-else :image-size="200" />
    </el-main>
    <RouterView />
  </el-container>
</template>

<style scoped>
.container-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 20em);
  gap: 2em;
  padding: 2em;
  justify-content: left;
}

h1 {
  margin: 1em;
  font-weight: bold;
  font-size: 1.5em;
}

.top-down {
  display: grid;
  grid-template-rows: min-content 1fr;
  align-content: start;
  padding: 0;
}

.header {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;
}
</style>
