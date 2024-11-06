<template>
    <ShowCards :pages="pages" :title="title" :loading="loading" @scroll="handleScroll" @wheel="handleWheel"></ShowCards>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject, nextTick } from 'vue'
import type { PageItem, Site } from '@/api_interface'
import { server } from '@/const'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'
import { filter_subscribe_key, filter_keyword_key } from '@/key'

const props = defineProps<{
    pageType: 'all' | 'daily' | 'site'
    site_id?: String
}>()


const EmptySite: Site = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [], icon: '' }

let pages = ref<PageItem[]>([])
let loading = ref(true)
let title = ref('')
let site = ref<Site>(EmptySite)

let filter_subscribe = inject(filter_subscribe_key)!;
let filter_keyword = inject(filter_keyword_key)!;

const fetchPages = (count: number) => {
    let endpoint = ''
    switch (props.pageType) {
        case 'all':
            endpoint = `${server}/page?count=${count}&subscribe=${filter_subscribe.value ? 'true' : 'false'}&keyword=${filter_keyword.value}`
            title.value = '全部文章'
            break
        case 'daily':
            endpoint = `${server}/page?count=${count}&today=${true}&subscribe=${filter_subscribe.value ? 'true' : 'false'}&keyword=${filter_keyword.value}`
            title.value = '每日更新'
            break
        case 'site':
            if (!props.site_id) return
            endpoint = `${server}/page?site=${props.site_id}&count=${count}&keyword=${filter_keyword.value}`
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
            title.value = site.value.name
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
watch(site, async (newSite) => {
  title.value = newSite.name
  await nextTick()
  console.log('Title updated:', title.value)
})
const { handleScroll, handleWheel } = useScrollFetch(fetchPages)
</script>