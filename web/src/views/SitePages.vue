<script setup lang="ts">
import { server } from '@/const';
import { ref, watch } from 'vue';
import ArticleCard from '@/components/ArticleCard.vue';
import type { SiteQuery } from '@/interface';
const props = defineProps({
    site_id: String
})


let site = ref<SiteQuery>({
    id: 0,
    name: '',
    url: '',
    category: '',
    cate_id: 0,
    pages: []
})
async function updatePages() {
    site.value = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [] }
    if (!props.site_id) return;
    site.value = await fetch(`${server}/site/${props.site_id}`)
        .then((r) => r.json())
}
watch(props, updatePages)
updatePages()

</script>

<template>
    <el-container class="full-height">
        <el-main class="full-height">
            <h1>{{ site.name }}</h1>
            <div class="container-grid">
                <router-link v-for:="page in site.pages" :to="{ name: 'page', params: { page_id: page.id } }">
                    <ArticleCard :page="page"></ArticleCard>
                </router-link>
            </div>
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
</style>
