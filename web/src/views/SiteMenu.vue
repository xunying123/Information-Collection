<script lang="ts" setup>
import { inject, onMounted, reactive, watch, ref, computed, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import type { SiteItem } from '@/api_interface'
import { ElScrollbar } from 'element-plus'
import { Location } from '@element-plus/icons-vue'
import UserCard from '@/components/UserCard.vue'
import UpdateSVG from '@/components/svg/UpdateSVG.vue'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import FolderPlusSVG from '@/components/svg/FolderPlusSVG.vue'
import LayersSVG from '@/components/svg/LayersSVG.vue'
import HelpSVG from '@/components/svg/HelpSVG.vue'
import { filter_subscribe_key, user_key, all_subjects_key } from '@/key'
import { getCategories, getSubjects } from '@/sdk'
import SettingSVG from '@/components/svg/SettingSVG.vue'

interface CateSite {
  cate_id: number
  cate_name: string
  sites: SiteItem[]
}

let filter_subscribe = inject(filter_subscribe_key)!
const user = inject(user_key)!
const router = useRouter()

let sites = reactive<CateSite[]>([])
let subjects = inject(all_subjects_key)!

// 侧边栏显示模式
const sidebarMode = ref(
  localStorage.getItem('sidebarMode') || user!.value!.group!.sidebar_show_mode || 'category'
)

async function loadSites() {
  const { data, error } = await getCategories()
  if (error) {
    console.error(error)
    return
  }
  // data: list of categories, each category has a list of sites
  // clear the sites array
  sites.splice(0, sites.length)
  for (let cate of data!) {
    let cateSites: CateSite = { cate_id: cate.id!, cate_name: cate.name, sites: [] }
    for (let site of cate.sites!) {
      if (site.name === '上海交通大学') {
        // 放前面显示
        cateSites.sites.unshift(site)
      } else {
        cateSites.sites.push(site)
      }
    }
    sites.push(cateSites)
  }
}

async function loadSubjects() {
  try {
    const { data, error } = await getSubjects()
    if (error) {
      console.error(error)
      return
    }
    // 清空主题数组
    subjects.value.splice(0, subjects.value.length)
    // 添加新的主题数据
    if (data) {
      for (let subject of data) {
        subjects.value.push(subject)
      }
    }
    // console.log('主题数据:', subjects.value)
  } catch (error) {
    console.error('加载主题失败:', error)
  }
}

function loadSidebarData() {
  loadSites()
  loadSubjects()
}

function handleSubMenuClick(index: string) {
  router.push(index)
}

watch(filter_subscribe, () => {
  loadSidebarData()
})

watch(sidebarMode, () => {
  loadSidebarData()
})

// 侧边栏显示模式变更监听
const updateSidebarMode = () => {
  sidebarMode.value = localStorage.getItem('sidebarMode') || 'category'
}

onMounted(() => {
  loadSidebarData()
  window.addEventListener('sidebarColorChanged', updateSidebarColor)
  window.addEventListener('sidebarModeChanged', updateSidebarMode)
})

// 侧边栏颜色部分：从 localStorage 读取颜色，默认为 'blue'
const sidebarColor = ref(localStorage.getItem('sidebarColor') || 'blue')
const sidebarClass = computed(() => `full-${sidebarColor.value}`)

const updateSidebarColor = () => {
  sidebarColor.value = localStorage.getItem('sidebarColor') || 'blue'
}

onBeforeUnmount(() => {
  window.removeEventListener('sidebarColorChanged', updateSidebarColor)
  window.removeEventListener('sidebarModeChanged', updateSidebarMode)
})
</script>

<template>
  <!-- 绑定基础类 .full 与动态颜色类 -->
  <div :class="['full', sidebarClass]">
    <router-link to="/">
      <img :src="user!.group!.logo!" class="logo" />
    </router-link>
    <router-link to="/user">
      <UserCard />
    </router-link>
    <ElScrollbar class="scratch-height">
      <el-menu
        class="el-menu-vertical-demo"
        :router="true"
        @open="handleSubMenuClick"
        @close="handleSubMenuClick"
      >
        <el-menu-item index="/">
          <LayersSVG class="menu-icon" />
          <span class="menu-top">全部</span>
        </el-menu-item>
        <el-menu-item index="/daliyupdate">
          <UpdateSVG class="menu-icon" />
          <span class="menu-top">今日更新</span>
        </el-menu-item>
        <el-menu-item index="/bookmarks">
          <BookmarkSvg fill="none" class="menu-icon" />
          <span class="menu-top">书签列表</span>
        </el-menu-item>
        <el-menu-item index="/manage" v-if="user?.is_admin">
          <FolderPlusSVG class="menu-icon" />
          <span class="menu-top">管理组织</span>
        </el-menu-item>

        <!-- 按网站分类显示 -->
        <template v-if="sidebarMode === 'category'">
          <el-sub-menu
            v-for="cate in sites"
            :key="cate.cate_id"
            :index="`/category/` + String(cate.cate_id)"
          >
            <template #title>
              <el-icon>
                <Location />
              </el-icon>
              <span>{{ cate.cate_name }}</span>
            </template>
            <el-menu-item
              v-for="site in cate.sites"
              :key="site.id"
              :index="`/site/` + site.id"
              style="margin-left: 2em"
            >
              {{ site.name }}
            </el-menu-item>
          </el-sub-menu>
        </template>

        <!-- 按文章分类显示 -->
        <template v-else>
          <el-menu-item
            v-for="subject in subjects"
            :key="subject.id"
            :index="`/subject/` + subject.id"
          >
            <el-icon>
              <Location />
            </el-icon>
            <span>{{ subject.name }}</span>
          </el-menu-item>
        </template>
        <el-menu-item index="/user">
          <SettingSVG class="menu-icon" />
          <span class="menu-top">设置</span>
        </el-menu-item>
        <el-menu-item index="/help">
          <HelpSVG class="menu-icon" />
          <span class="menu-top">帮助</span>
        </el-menu-item>
      </el-menu>
    </ElScrollbar>
    <div class="overlay">
      <img src="/static/image_21_1-1.png" class="overlay-image" />
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: auto;
  pointer-events: none;
}

.overlay-image {
  width: 100%;
  height: auto;
  opacity: 0.1;
}

/* 基础侧边栏样式 */
.full {
  width: 100%;
  height: 100%;
  --el-menu-bg-color: rgba(200, 22, 30, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgba(0, 0, 102, 0.7), rgb(0, 64, 152), rgb(0, 104, 179));
  --el-menu-text-color: #ffffff;
  --el-menu-hover-bg-color: rgba(0, 134, 209, 1);
  --el-menu-item-font-size: 1.1em;
  font-size: 14px;
  display: flex;
  flex-direction: column;
}

.el-menu-item:hover {
  color: #fff;
}

.scratch-height {
  flex-grow: 1;
  overflow: auto;
}

.menu-icon {
  margin-right: 4px;
}

.logo {
  width: 75%;
  height: auto;
  margin-left: 20px;
  margin-top: 0.2em;
}

.el-sub-menu__title {
  font-size: 1.2em !important;
  color: #fff;
}

.menu-top {
  font-size: 1.1em !important;
  font-weight: bold !important;
  color: #fff;
}

div.full {
  color: #fff;
}
</style>
