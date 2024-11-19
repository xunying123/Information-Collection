<script setup lang="ts">
import { defineProps } from 'vue'
import type { Keyword } from '@/api_interface'

defineProps<{
  keywords: Keyword[]
  closable?: boolean
  handleClose: (keyword: Keyword) => void
}>()

const tagTypes = ['primary', 'success', 'warning', 'danger']
function getRandomTagType() {
  const randomIndex = Math.floor(Math.random() * tagTypes.length)
  return tagTypes[randomIndex]
}
</script>

<template>
  <div class="keyword-tags">
    <el-tag
      v-for="keyword in keywords"
      :key="keyword.id"
      round
      :type="getRandomTagType()"
      size="large"
      :closable="closable"
      @close="handleClose(keyword)"
    >
      {{ keyword.word }}
    </el-tag>
  </div>
</template>
