<template>
  <ShowCards :title="site.name" :pages="site.pages" :loading="site.id == 0" @scroll="handleScroll" @wheel="handleWheel"></ShowCards>
</template>

<script setup lang="ts">
import { server } from '@/const'
import { ref, watch } from 'vue'
import type { Site } from '@/api_interface'
import ShowCards from '@/components/ShowCards.vue'
import useScrollFetch from '@/useScrollFetch'

const props = defineProps({
  site_id: String
})

const EmptySite: Site = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [], icon: '' }

let site = ref<Site>(EmptySite)

// async function updatePages(count: number) {
//   site.value = EmptySite
//   if (!props.site_id) return
//   site.value = await fetch(`${server}/site/${props.site_id}?count=${count}`).then((r) => r.json())
// }

const updatePages = (count: number) => {
  // site.value = EmptySite
  if (!props.site_id) return
  fetch(`${server}/site/${props.site_id}?count=${count}`)
    .then((r) => r.json())
    .then((data) => {
      console.log('data', data.length)
      if (site.value.id == 0) {
        site.value = data
      } else {
        site.value = data
      }
    })
}

watch(
  () => props.site_id,
  (newSiteId, oldSiteId) => {
    if (newSiteId) {
      updatePages(50)
    }
  }
)

const { handleScroll, handleWheel } = useScrollFetch(updatePages)
</script>
