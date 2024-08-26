<template>
  <ShowCards :title="site.name" :pages="site.pages" :v-loading="site.id == 0"></ShowCards>
</template>

<script setup lang="ts">
import { server } from '@/const'
import { ref, watch } from 'vue'
import type { Site } from '@/api_interface'
import ShowCards from '@/components/ShowCards.vue'

const props = defineProps({
  site_id: String
})

const EmptySite: Site = { id: 0, name: '', url: '', category: '', cate_id: 0, pages: [], icon: '' }

let site = ref<Site>(EmptySite)

async function updatePages() {
  site.value = EmptySite;
  if (!props.site_id) return
  site.value = await fetch(`${server}/site/${props.site_id}`).then((r) => r.json())
}

watch(props, updatePages)
updatePages()
</script>
