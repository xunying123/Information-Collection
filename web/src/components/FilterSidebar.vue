<script setup lang="ts">
import { ref, defineExpose } from 'vue'

defineProps<{
  selectedCategories: number[]
  selectedTimeRange: string
  selectedSortOption: string
  selectedSubjects: number[]
  allCategories: any[]
  subjects: any[]
}>()

const emit = defineEmits<{
  (e: 'update:selectedCategories', value: number[]): void
  (e: 'update:selectedTimeRange', value: string): void
  (e: 'update:selectedSortOption', value: string): void
  (e: 'update:selectedSubjects', value: number[]): void
}>()

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
      <!-- 关键词分类筛选 -->
      <div class="filter-group">
        <h3>关键词分类</h3>
        <el-checkbox-group 
          :model-value="selectedSubjects" 
          @update:model-value="emit('update:selectedSubjects', $event)"
        >
          <el-checkbox-button v-for="cat in subjects" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </el-checkbox-button>
        </el-checkbox-group>
      </div>

      <!-- 原有类别筛选 -->
      <div class="filter-group">
        <h3>网站类别</h3>
        <el-checkbox-group 
          :model-value="selectedCategories" 
          @update:model-value="emit('update:selectedCategories', $event)"
        >
          <el-checkbox-button v-for="cate in allCategories" :key="cate.id" :value="cate.id">
            {{ cate.name }}
          </el-checkbox-button>
        </el-checkbox-group>
      </div>

      <!-- 时间范围筛选 -->
      <div class="filter-group">
        <h3>时间范围</h3>
        <el-segmented 
          :model-value="selectedTimeRange" 
          @update:model-value="emit('update:selectedTimeRange', $event)" 
          :options="timeOptions" 
        />
      </div>

      <!-- 排序方式 -->
      <div class="filter-group">
        <h3>排序方式</h3>
        <el-radio-group 
          :model-value="selectedSortOption" 
          @update:model-value="emit('update:selectedSortOption', $event)"
        >
          <el-radio-button value="time">按时间排序</el-radio-button>
          <el-radio-button value="score">按重要度排序</el-radio-button>
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