<template>
    <div class="card-container">
        <router-link :to="{ name: 'page', params: { page_id: page.id } }">
            <el-card class="small-card" shadow="hover">
                <h3 class="small-card-body">{{ page.title }}</h3>
                <!-- <div class="small-card-body">{{ page.content }}</div> -->
                <template #footer>
                    <div class="small-card-footer">
                        <!-- <el-link :href="page.source_url" target="_blank">Source</el-link> -->
                        <!-- <el-button type="success" :plain="!is_bookmarked(page)"
                        @click="toggle_bookmark(page)">书签</el-button> -->

                        <!-- <el-button>Open</el-button> -->
                        <p v-if="is_bookmarked(page)" style="color: rgb(240, 131, 0);">已设为书签</p>
                        <p>(todo: 发布时间)</p>
                    </div>
                </template>
            </el-card>
        </router-link>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { Page } from '@/interface'
import { is_bookmarked, toggle_bookmark } from '@/bookmark';
defineProps<{ page: Page }>();
</script>

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
    grid-template-rows: 1fr auto;
    width: 100%;
    /* 使卡片宽度填满网格单元 */
    height: 100%;
    /* 使卡片高度填满网格单元 */
    box-sizing: border-box;
    /* 确保padding不会影响卡片的实际尺寸 */
}

/* .small-card>* {
    padding: 0.5em;
} */

.small-card-body {
    overflow: ellipsis;
    font-weight: bold;
}

.small-card-footer {
    width: 100%;
    padding: 0.5em;
    box-sizing: border-box;
    align-self: end;
}
</style>