<script setup lang="ts">
import { ref, computed, defineExpose } from 'vue'

const props = defineProps<{
  filterOptions: { selectedCategories: number[]; selectedTimeRange: string; selectedSortOption: string }
  allCategories: any[]
}>()
const emit = defineEmits<{
  (e: 'update:filterOptions', value: { selectedCategories: number[]; selectedTimeRange: string; selectedSortOption: string }): void
}>()

// computed 实现双向绑定
const selectedCategories = computed<number[]>({
  get: () => props.filterOptions.selectedCategories,
  set: val => emit('update:filterOptions', { ...props.filterOptions, selectedCategories: val })
})
const selectedTimeRange = computed<string>({
  get: () => props.filterOptions.selectedTimeRange,
  set: val => emit('update:filterOptions', { ...props.filterOptions, selectedTimeRange: val })
})
const selectedSortOption = computed<string>({
  get: () => props.filterOptions.selectedSortOption,
  set: val => emit('update:filterOptions', { ...props.filterOptions, selectedSortOption: val })
})

const timeOptions = [
  { label: '全部', value: 'all' },
  { label: '1天内', value: '1' },
  { label: '7天内', value: '7' },
  { label: '30天内', value: '30' },
  { label: '一年内', value: '365' }
]

const drawerVisible = ref(false)
const openDrawer = () => {
  drawerVisible.value = true
}
const closeDrawer = () => {
  drawerVisible.value = false
}

defineExpose({
  openDrawer,
  closeDrawer
})
</script>

<template>
  <el-drawer v-model="drawerVisible" title="筛选" size="40em">
    <div class="filter-content">
      <!-- 类别筛选 -->
      <div class="filter-group">
        <h3>类别</h3>
        <el-checkbox-group v-model="selectedCategories">
          <el-checkbox-button v-for="cate in allCategories" :key="cate.id" :label="cate.id">
            {{ cate.name }}
          </el-checkbox-button>
        </el-checkbox-group>
      </div>
      <!-- 时间范围筛选 -->
      <div class="filter-group">
        <h3>时间范围</h3>
        <el-segmented v-model="selectedTimeRange" :options="timeOptions" />
      </div>
      <!-- 排序方式 -->
      <div class="filter-group">
        <h3>排序方式</h3>
        <el-radio-group v-model="selectedSortOption">
          <el-radio-button label="time">按时间排序</el-radio-button>
          <el-radio-button label="score">按重要度排序</el-radio-button>
        </el-radio-group>
      </div>
    </div>
  </el-drawer>
</template>

<style scoped>
.filter-content {
  padding: 1em;
}
.filter-group {
  margin-bottom: 1.5em;
}
.filter-group h3 {
  margin-bottom: 0.5em;
  font-size: 1.1em;
  font-weight: 600;
}

</style>
