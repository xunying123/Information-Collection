<script setup lang="ts">
import { server } from '@/const';
import { ref, watch } from 'vue';

const props = defineProps({
    site_id: String
})

interface Page {
    id: number
    title: string
    content: string,
    source_url: string

    site_id: number
    site: string
    cate_id: number
    category: string
}

let pages = ref<Page[]>([])
async function updatePages() {
    pages.value = [];
    pages.value = await fetch(`${server}/site/${props.site_id}`)
        .then((r) => r.json())
}
watch(props, updatePages)
updatePages()

</script>

<template>
    {{ site_id }}
    {{ pages }}
    <el-card v-for:="page in pages">
        <template v-slot:header>
            <div class="clearfix">
                <span>{{ page.title }}</span>
            </div>
        </template>
        {{ page.content }}
        <div>
            <el-link :href="page.source_url" target="_blank">Source</el-link>
        </div>
    </el-card>
</template>
