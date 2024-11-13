<template>
  <CombinedPages pageType="site" :site_id="props.site_id" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const props = defineProps({
  site_id: String
})
</script>
