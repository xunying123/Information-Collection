<template>
  <div class="search-container">
    <!-- 搜索按钮，手动添加图标 -->
    <el-button @click="toggleSearch" class="search-btn" :icon="Search"> </el-button>

    <!-- 搜索输入框 -->
    <transition name="slide">
      <el-input
        v-show="isSearchVisible"
        v-model="searchQuery"
        placeholder="请输入内容"
        class="search-input"
        clearable
        @blur="toggleSearch"
      ></el-input>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue' // 引入图标
import { watch, defineEmits } from 'vue'

let emit = defineEmits(['update:searchQuery'])
let searchQuery = ref('')
const isSearchVisible = ref(false)

const toggleSearch = () => {
  isSearchVisible.value = !isSearchVisible.value
}

watch(searchQuery, (newQuery) => {
  emit('update:searchQuery', newQuery)
})
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  position: relative;
}

.search-btn {
  z-index: 1;
  position: relative;
}

/* 定义滑动效果 */
.slide-enter-active,
.slide-leave-active {
  transition:
    width 0.4s ease,
    opacity 0.4s ease;
}

.slide-enter-from,
.slide-leave-to {
  width: 0;
  opacity: 0;
}

/* 设置搜索框初始状态 */
.search-input {
  width: 250px;
  size: 'large';
}
</style>
