<template>
  <div id="content" @scroll="handleScroll" @wheel="handleWheel">
    <ShowCards :pages="pages" title="今日更新" :loading="loading"></ShowCards>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { PageItem } from '@/api_interface'
import { server } from '@/const'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'

let pages = ref<PageItem[]>([])
let loading = ref(true)

const fetchPages = (count: number) => {
  fetch(`${server}/page?count=${count}`)
    .then((res) => res.json())
    .then((data: PageItem[]) => {
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      const filteredData = data.filter((page: PageItem) => {
        const publishDate = new Date(page.publish_time)
        publishDate.setHours(0, 0, 0, 0)
        return publishDate.getTime() === today.getTime()
      })

      pages.value = filteredData
      loading.value = false
    })
}

onMounted(() => {
  fetchPages(50)
})
const { handleScroll, handleWheel } = useScrollFetch(fetchPages)
</script>
