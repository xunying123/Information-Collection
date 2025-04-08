<template>
  <ShowCards
    :pages="pages"
    :title="title"
    :loading="loading"
    @scroll="handleScroll"
    @wheel="handleWheel"
  ></ShowCards>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject, provide } from 'vue'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'
import { filter_subscribe_key, filter_keyword_key, search_keyword_key } from '@/key'
import { getPages, getSite, getCategory, type PageItem, type Site, type PageGet } from '@/sdk'
const props = defineProps<{
  pageType: 'all' | 'daily' | 'site' | 'category'
  site_id?: String
  category_id?: String
}>()

const EmptySite: Site = { id: 0, name: '', url: '', pages: [], icon: '' }

let searchKeyword = ref('')
provide(search_keyword_key, searchKeyword)

let pages = ref<PageItem[]>([])
let loading = ref(true)
let title = ref('')
let site = ref<Site>(EmptySite)
let count = ref(props.pageType === 'all' || props.pageType === 'site' ? 50 : 10)

let filter_subscribe = inject(filter_subscribe_key)!
let filter_keyword = inject(filter_keyword_key)!

const fetchPages = (count: number) => {
  let done = false
  setTimeout(() => {
    if (!done) {
      loading.value = true
    }
  }, 200)
  let body: PageGet = {
    count: count,
    keyword: filter_keyword.value,
    subscribe: filter_subscribe.value
  }
  if (searchKeyword.value) {
    body.search_title = searchKeyword.value
    body.search_content = searchKeyword.value
  }
  switch (props.pageType) {
    case 'all':
      title.value = '全部文章'
      break
    case 'daily':
      body.today = true
      title.value = '每日更新'
      break
    case 'site':
      if (!props.site_id) return
      body.site = Number(props.site_id)
      break
    case 'category':
      if (!props.category_id) return
      body.category = Number(props.category_id)
      break
  }
  getPages({ body: body })
    .then((res) => res.data)
    .then((data) => {
      pages.value = data!.data!
      done = true
      loading.value = false
    })
    .catch((err) => {
      console.error('Error fetching data:', err)
    })
}

async function updateSite() {
  const { data, error } = await getSite({ path: { site_id: Number(props.site_id) } })
  if (error) {
    console.error(error)
    return
  }
  console.log(data)
  data.pages = site.value.pages
  site.value = data
  title.value = site.value.name
}

async function updateCategory() {
  const { data, error } = await getCategory({ path: { cate_id: Number(props.category_id) } })
  if (error) {
    console.error(error)
    return
  }
  title.value = data.name
}

onMounted(() => {
  fetchPages(count.value)
  if (props.pageType === 'site' && props.site_id) {
    updateSite()
  }
  if (props.pageType === 'category' && props.category_id) {
    updateCategory()
  }
})

watch(searchKeyword, () => {
  fetchPages(count.value)
})

watch([() => props.site_id, () => props.category_id], ([newSiteId, newCategoryId]) => {
  if (newSiteId || newCategoryId) {
    fetchPages(count.value)
    if (props.pageType === 'site' && newSiteId) {
      updateSite()
    }
    if (props.pageType === 'category' && newCategoryId) {
      updateCategory()
    }
  }
})
const { handleScroll, handleWheel } = useScrollFetch(fetchPages, count.value)
</script>
