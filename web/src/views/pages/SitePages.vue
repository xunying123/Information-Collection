<template>
  <CombinedPages pageType="site" :site_id="props.site_id" :category_id="props.category_id" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const props = defineProps({
  category_id: String,
  site_id: String
})
</script>
