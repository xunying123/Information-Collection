<template>
  <CombinedPages page-type="category" :category_id="props.category_id" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const props = defineProps({
  category_id: String
})
</script>
