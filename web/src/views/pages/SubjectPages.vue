<template>
  <CombinedPages page-type="subject" :subject_id="Number(subject_id)" />
</template>

<script setup lang="ts">
import CombinedPages from '@/views/pages/CombinedPages.vue'

const { subject_id } = defineProps<{
  subject_id: string
}>()
</script>
