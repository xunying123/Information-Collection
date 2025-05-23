<template>
  <CombinedPages page-type="category" :category_id="Number(category_id)" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const { category_id } = defineProps<{
  category_id: string
}>()
</script>
