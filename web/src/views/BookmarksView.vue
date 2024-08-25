<script setup lang="ts">
import { bookmarks } from '@/bookmark'
function reset_bookmarks() {
  bookmarks.splice(0, bookmarks.length)
}
</script>

<template>
  <el-container class="full-height">
    <el-main class="full-height TD">
      <div class="header">
        <h1 class="site-name">Bookmarks</h1>
        <el-button @click="reset_bookmarks">重置 Bookmarks</el-button>
      </div>
      <el-scrollbar>
        <div class="container-grid">
          <ArticleCard v-for:="page in bookmarks" :page="page"></ArticleCard>
        </div>
      </el-scrollbar>
    </el-main>
    <router-view />
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

.site-name {
  margin: 1em;
  font-weight: bold;
  font-size: 1.5em;
}

.TD {
  display: grid;
  grid-template-rows: min-content 1fr;
  align-content: start;
  padding: 0;
}
</style>
