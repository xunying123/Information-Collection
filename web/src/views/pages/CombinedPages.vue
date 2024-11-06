<template>
    <ShowCards :pages="pages" :title="title" :loading="loading" @scroll="handleScroll" @wheel="handleWheel"></ShowCards>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import type { PageItem, Site } from '@/api_interface'
import { server } from '@/const'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'

const props = defineProps<{
    pageType: 'all' | 'daily' | 'site'
    site_id?: String
}>()


const EmptySite: Site = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [], icon: '' }

let pages = ref<PageItem[]>([])
let loading = ref(true)
let title = ref('')
let site = ref<Site>(EmptySite)

const fetchPages = (count: number) => {
    let endpoint = ''
    switch (props.pageType) {
        case 'all':
            endpoint = `${server}/page?count=${count}`
            title.value = '全部文章'
            break
        case 'daily':
            endpoint = `${server}/page?count=${count}&today=${true}`
            title.value = '每日更新'
            break
        case 'site':
            if (!props.site_id) return
            endpoint = `${server}/page?site=${props.site_id}&count=${count}`
            title.value = site.value.name
            break
    }

    try {
        if (props.pageType === 'site' && props.site_id) {
            fetch(`${server}/site/${props.site_id}`)
                .then((r) => r.json())
                .then((data) => {
                    data.pages = site.value.pages
                    site.value = data
                })
        }

        fetch(endpoint)
            .then((r) => r.json())
            .then((data) => {
                site.value.pages = data.pages
                pages.value = data.pages
                loading.value = false
            })
    } catch (error) {
        console.error('Error fetching data:', error)
    }
}

onMounted(() => {
    fetchPages(50)
})

watch(
  () => props.site_id,
  (newSiteId, oldSiteId) => {
    if (newSiteId) {
      fetchPages(50)
    }
  }
)
const { handleScroll, handleWheel } = useScrollFetch(fetchPages)
</script>