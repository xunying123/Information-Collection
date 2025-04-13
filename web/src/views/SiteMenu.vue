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
import { filter_subscribe_key, user_key } from '@/key'
import { getCategories } from '@/sdk'

interface CateSite {
  cate_id: number
  cate_name: string
  sites: SiteItem[]
}

let filter_subscribe = inject(filter_subscribe_key)!
const user = inject(user_key)!
const router = useRouter()

let sites = reactive<CateSite[]>([])

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

function handleSubMenuClick(index: string) {
  router.push(index)
}

watch(filter_subscribe, () => {
  loadSites()
})

onMounted(() => {
  loadSites()
  window.addEventListener('sidebarColorChanged', updateSidebarColor)
})

// 侧边栏颜色部分：从 localStorage 读取颜色，默认为 'blue'
const sidebarColor = ref(localStorage.getItem('sidebarColor') || 'blue')
const sidebarClass = computed(() => `full-${sidebarColor.value}`)

const updateSidebarColor = () => {
  sidebarColor.value = localStorage.getItem('sidebarColor') || 'blue'
}

onBeforeUnmount(() => {
  window.removeEventListener('sidebarColorChanged', updateSidebarColor)
})
</script>

<template>
  <!-- 绑定基础类 .full 与动态颜色类 -->
  <div :class="['full', sidebarClass]">
    <!-- <div class="full"> -->
    <router-link to="/">
      <img src="https://www.sjtu.edu.cn/resource/assets/img/LogoWhite.png" class="logo" />
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
        <el-menu-item index="/help">
          <HelpSVG class="menu-icon" />
          <span class="menu-top">帮助</span>
        </el-menu-item>
      </el-menu>
    </ElScrollbar>
    <div class="bottom-buttons">
      <router-link to="/user/subscriptions">
        <el-button plain type="primary">管理订阅源</el-button>
      </router-link>
      <router-link to="/user/keywords">
        <el-button plain type="primary">管理关键词</el-button>
      </router-link>
    </div>
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

.bottom-buttons {
  display: flex;
  margin: 0.5em;
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

/* 各预设颜色样式 */

/* 蓝色方案 */
.full-blue {
  --el-menu-bg-color: rgba(0, 64, 152, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgb(0, 0, 102), rgb(0, 64, 152), rgb(0, 104, 179));
  --el-menu-hover-bg-color: rgba(0, 134, 209, 1);
}

/* 黄色方案 */
.full-yellow {
  --el-menu-bg-color: rgba(253, 208, 0, 0);
  --el-menu-active-color: #ffffff;
  /* 渐变背景：上方采用深黄色，下方采用中性黄色，核心色不变 */
  background: linear-gradient(180deg, rgb(200, 160, 0), rgb(253, 208, 0), rgb(220, 180, 0));
  --el-menu-text-color: #ffffff;
  /* 悬停时采用稍深的色调 */
  --el-menu-hover-bg-color: rgb(210, 170, 0);
}

/* 红色方案 */
.full-red {
  --el-menu-bg-color: rgba(167, 32, 56, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgb(167, 0, 6), rgb(167, 32, 56), rgb(167, 72, 83));
  --el-menu-hover-bg-color: rgb(167, 102, 113);
}

/* 绿色方案 */
.full-green {
  --el-menu-bg-color: rgba(51, 141, 39, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgb(51, 77, 0), rgb(51, 141, 39), rgb(51, 181, 66));
  --el-menu-hover-bg-color: rgb(51, 211, 96);
}

/* 橙色方案 */
.full-orange {
  --el-menu-bg-color: rgba(240, 130, 0, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgb(180, 90, 0), rgb(240, 130, 0), rgb(255, 170, 40));
  --el-menu-hover-bg-color: rgb(255, 180, 70);
}
</style>
