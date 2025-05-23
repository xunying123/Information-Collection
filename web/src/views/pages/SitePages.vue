<template>
  <CombinedPages page-type="site" :site_id="Number(site_id)" :category_id="Number(category_id)" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const { category_id, site_id } = defineProps<{
  category_id: string
  site_id: string
}>()
</script>
