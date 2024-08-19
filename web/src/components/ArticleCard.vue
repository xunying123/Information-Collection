<template>
    <el-card class="small-card" shadow="hover">
        <template v-slot:header>
            <h3 class="small-card-header">{{ page.title }}</h3>
        </template>
        <div class="small-card-body">{{ page.content }}</div>
        <template v-slot:footer>
            <el-link :href="page.source_url" target="_blank">Source</el-link>
        </template>
    </el-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { Page } from '@/interface'
defineProps<{ page: Page }>();
</script>

<style scoped>
.small-card {
    height: 10em;
}

.small-card > * {
    padding: 0.5em;
}

.small-card-body {
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    overflow: hidden;
}

.small-card-header {
    height: 2em;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
</style>