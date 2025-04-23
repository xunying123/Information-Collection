<script setup lang="ts">
import { ref, inject, toRef } from 'vue'

const props = defineProps<{
  allCategories: any[]
  subjects: any[]
}>()
props

// 使用inject接收筛选状态和更新方法
const filterState = inject('filterState') as {
  selectedCategories: number[]
  selectedSubjects: number[]
  selectedTimeRange: string
  currentSortOption: string
  updateCategories: (categories: number[]) => void
  updateSubjects: (subjects: number[]) => void
  updateTimeRange: (timeRange: string) => void
  updateSortOption: (sortOption: string) => void
}

const selectedCategories = toRef(filterState, 'selectedCategories')
const selectedSubjects = toRef(filterState, 'selectedSubjects')
const selectedTimeRange = toRef(filterState, 'selectedTimeRange')
const currentSortOption = toRef(filterState, 'currentSortOption')

const timeOptions = [
  { label: '全部', value: 'all' },
  { label: '1天内', value: '1' },
  { label: '7天内', value: '7' },
  { label: '30天内', value: '30' },
  { label: '一年内', value: '365' }
]

// 抽屉控制
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
          v-model="selectedSubjects"
          @change="filterState.updateSubjects(selectedSubjects)"
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
          v-model="selectedCategories"
          @change="filterState.updateCategories(selectedCategories)"
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
          v-model="selectedTimeRange"
          @change="filterState.updateTimeRange(selectedTimeRange)"
          :options="timeOptions"
        />
      </div>

      <!-- 排序方式 -->
      <div class="filter-group">
        <h3>排序方式</h3>
        <el-radio-group
          v-model="currentSortOption"
          @change="filterState.updateSortOption(currentSortOption)"
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