<script lang="ts" setup>
import {
  user_key,
  filter_subscribe_key,
  filter_keyword_key,
  all_categories_key,
  all_subjects_key
} from '@/key'
import SiteMenu from '@/views/SiteMenu.vue'
import { NLayout, NLayoutSider, NLayoutContent } from 'naive-ui'
import { provide, ref, inject } from 'vue'
import { getCategories, getSubjects, type Category, type Subject } from '@/sdk'

let allCategories = ref<Category[]>([])
getCategories().then((value) => (allCategories.value = value.data!))
provide(all_categories_key, allCategories)

let subjects = ref<Subject[]>([])
getSubjects().then((value) => (subjects.value = value.data!))
provide(all_subjects_key, subjects)

const user = inject(user_key)!
const bgUrl = ref(
  localStorage.getItem('bgUrl') ||
    user.value?.group?.background ||
    'https://mc.sjtu.cn/wp-content/uploads/2022/10/%E5%A4%9C%E6%99%9A%E4%B8%9C%E5%A4%A7%E9%97%A8.jpg'
)

window.addEventListener('bgUrlChanged', () => {
  bgUrl.value = localStorage.getItem('bgUrl') || bgUrl.value
})
</script>
<template>
  <NLayout has-sider class="full-height">
    <NLayoutSider
      class="sidebar"
      collapse-mode="transform"
      :collapsed-width="0"
      width="20em"
      show-trigger="bar"
      bordered
    >
      <SiteMenu class="site-menu" />
    </NLayoutSider>
    <!-- <NLayoutContent class="content overlay"> -->
    <NLayoutContent class="content overlay" :style="{ 'background-image': bgUrl }">
      <RouterView />
    </NLayoutContent>
  </NLayout>
</template>

<style scoped>
@media (max-width: 768px) {
  .sidebar {
    width: 9em !important;
  }

  .site-menu {
    padding-left: 10em;
  }

  .content {
    width: 80% !important;
  }
}

.content.overlay {
  background-size: cover;
  background-position: center;
}
</style>
