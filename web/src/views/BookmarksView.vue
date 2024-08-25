<script setup lang="ts">
import { bookmarks } from '@/bookmark';
</script>

<template>
    <el-table :data="bookmarks" style="width: 100%">
        <el-table-column prop="category" label="类别"></el-table-column>
        <el-table-column prop="site" label="来源">
            <template #default="scope">
                <RouterLink :to="`/site/${scope.row.site_id}`">{{ scope.row.site }}</RouterLink>
            </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" show-overflow-tooltip>
            <template #default="scope">
                <RouterLink :to="{ name: 'page', params: { site_id: scope.row.site_id, page_id: scope.row.id } }">
                    {{ scope.row.title }}
                </RouterLink>
            </template>
        </el-table-column>
        <el-table-column label="发布时间">
            <!-- <template #default="scope">{{ scope.row.site_id }}</template> -->
            <template #default>TODO</template>
        </el-table-column>
    </el-table>
    {{ bookmarks }}
</template>