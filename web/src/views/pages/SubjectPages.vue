<template>
  <CombinedPages page-type="all" :subject_id="props.subject_id" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const props = defineProps({
  subject_id: String
})
</script>
