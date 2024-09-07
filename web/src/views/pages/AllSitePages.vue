<template>
  <ShowCards :pages="pages" title="全部文章" :loading="loading"></ShowCards>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { PageItem } from '@/api_interface'
import { server } from '@/const'
import ShowCards from '@/components/ShowCards.vue'

let pages = ref<PageItem[]>([])
let loading = ref(true)
fetch(`${server}/page?count=1000`)
  .then((res) => res.json())
  .then((data) => {
    pages.value = data
    loading.value = false
  })
</script>
