<script lang="ts" setup>
import { inject, ref } from 'vue'
import { ElScrollbar } from 'element-plus'
import { Location } from '@element-plus/icons-vue'
import UserCard from '@/components/UserCard.vue'
import UpdateSVG from '@/components/svg/UpdateSVG.vue'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import FolderPlusSVG from '@/components/svg/FolderPlusSVG.vue'
import LayersSVG from '@/components/svg/LayersSVG.vue'
import HelpSVG from '@/components/svg/HelpSVG.vue'
import {
  user_key,
  all_subjects_key,
  all_categories_key,
  type SideBarMode,
  type SideBarColor
} from '@/key'
import SettingSVG from '@/components/svg/SettingSVG.vue'

const user = inject(user_key)!

const categories = inject(all_categories_key)!
const subjects = inject(all_subjects_key)!

const sidebarMode = ref<SideBarMode>(
  (localStorage.getItem('sidebarShowMode') ||
    user!.value!.group?.sidebar_show_mode ||
    'category') as SideBarMode
)
const sidebarColor = ref<SideBarColor>(
  (localStorage.getItem('sidebarColor') || 'blue') as SideBarColor
)
</script>

<template>
  <div :class="['full', `full-${sidebarColor}`]">
    <router-link to="/">
      <img :src="user!.group?.logo!" class="logo" />
    </router-link>
    <router-link to="/user">
      <UserCard />
    </router-link>
    <ElScrollbar class="scratch-height">
      <el-menu class="el-menu-vertical-demo" :router="true">
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
        <el-menu-item v-if="user?.is_admin" index="/manage">
          <FolderPlusSVG class="menu-icon" />
          <span class="menu-top">管理组织</span>
        </el-menu-item>

        <el-divider v-if="user?.group" class="divider" />
        <div v-if="user?.group" class="menu-middle">专属新闻</div>
        <!-- 按文章分类显示 -->
        <template v-if="sidebarMode === 'subject' || sidebarMode === 'both'">
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

        <el-divider v-if="sidebarMode === 'both'" class="divider" />

        <!-- 按网站分类显示 -->
        <template v-if="sidebarMode === 'category' || sidebarMode === 'both'">
          <el-sub-menu v-for="cate in categories" :key="cate.id" :index="`/category/${cate.id}`">
            <template #title>
              <el-icon>
                <Location />
              </el-icon>
              <span>{{ cate.name }}</span>
            </template>
            <el-menu-item
              v-for="site in cate.sites"
              :key="site.id"
              :index="`/category/${cate.id}/site/${site.id}`"
              style="margin-left: 2em"
            >
              {{ site.name }}
            </el-menu-item>
          </el-sub-menu>
        </template>

        <el-divider class="divider" />
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
  --el-menu-item-height: 3em !important;
  font-size: 14px;
  display: flex;
  flex-direction: column;
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

.divider {
  margin: 0.3em 0;
  width: 90%;
  margin-left: 5%;
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
  margin-top: 1em;
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

.menu-middle {
  font-size: 0.9em;
  margin-left: 1.2em;
  margin-top: 1.2em;
  color: #ffffff;
}

div.full {
  color: #fff;
}
</style>
