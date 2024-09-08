<template>
  <ShowCards
    :pages="pages"
    title="全部文章"
    :loading="loading"
    @scroll="handleScroll"
    @wheel="handleWheel"
  ></ShowCards>
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
    .then((data) => {
      console.log('data', data.length)
      pages.value = data
      loading.value = false
    })
}

onMounted(() => {
  fetchPages(50)
})
const { handleScroll, handleWheel } = useScrollFetch(fetchPages)
</script>
