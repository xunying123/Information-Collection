<script setup lang="ts">
import { all_categories_key, all_subjects_key } from '@/key'
import type { SortType } from '@/sdk'
import { inject } from 'vue'

const all_categories = inject(all_categories_key)!
const all_subjects = inject(all_subjects_key)!

const selectedCategories = defineModel<number[]>('selectedCategories', { default: [] })
const selectedSubjects = defineModel<number[]>('selectedSubjects', { default: [] })
const selectedTimeRange = defineModel<number>('selectedTimeRange', { default: 0 })
const currentSortOption = defineModel<SortType>('currentSortOption', { default: 'time' })

const timeOptions = [
  { label: '全部', value: 0 },
  { label: '1天内', value: 1 },
  { label: '7天内', value: 7 },
  { label: '30天内', value: 30 },
  { label: '365天内', value: 365 }
]
</script>

<template>
  <div class="filter-content">
    <!-- 关键词分类筛选 -->
    <div class="filter-group">
      <h3>关键词分类</h3>
      <el-checkbox-group v-model="selectedSubjects">
        <el-checkbox-button v-for="cat in all_subjects" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </el-checkbox-button>
      </el-checkbox-group>
    </div>

    <!-- 原有类别筛选 -->
    <div class="filter-group">
      <h3>网站类别</h3>
      <el-checkbox-group v-model="selectedCategories">
        <el-checkbox-button v-for="cate in all_categories" :key="cate.id" :value="cate.id">
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
      <el-radio-group v-model="currentSortOption">
        <el-radio-button value="time">按时间排序</el-radio-button>
        <el-radio-button value="score">按重要度排序</el-radio-button>
      </el-radio-group>
    </div>
  </div>
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
