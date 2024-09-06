<script lang="ts" setup>
import { reactive } from 'vue'
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'
import { ElScrollbar } from 'element-plus'
import UserCard from '@/components/UserCard.vue'
import UpdateSVG from '@/components/svg/UpdateSVG.vue'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import FolderPlusSVG from '@/components/svg/FolderPlusSVG.vue'
import LayersSVG from '@/components/svg/LayersSVG.vue'

interface CateSite {
  cate_id: number
  cate_name: string
  sites: SiteItem[]
}

let sites = reactive<CateSite[]>([])

fetch(`${server}/site`)
  .then((r) => r.json())
  .then((data: SiteItem[]) => {
    let cateSites: CateSite = { cate_id: 0, cate_name: '', sites: [] }
    for (let site of data) {
      if (site.cate_id != cateSites.cate_id) {
        if (cateSites.cate_id != 0) sites.push(cateSites)
        cateSites = { cate_id: site.cate_id, cate_name: site.category, sites: [] }
      }
      cateSites.sites.push(site)
    }
    if (cateSites.cate_id != 0) sites.push(cateSites)
  })
</script>

<template>
  <div class="full">
    <el-scrollbar>
      <img src="https://www.sjtu.edu.cn/resource/assets/img/LogoWhite.png" class="logo" />
      <UserCard />
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
        <el-menu-item index="/managesites">
          <FolderPlusSVG class="menu-icon" />
          <span class="menu-top">增删网站</span>
        </el-menu-item>
        <el-sub-menu v-for:="cate in sites" :index="cate.cate_name">
          <template #title>
            <el-icon> </el-icon>
            <span>{{ cate.cate_name }}</span>
          </template>
          <el-menu-item v-for:="site in cate.sites" :index="`/site/` + site.id">{{
            site.name
          }}</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
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
  pointer-events: none; /* 添加这一行 */
}

.overlay-image {
  width: 100%;
  height: auto;
  opacity: 0.1;
  /* 设置透明度，你可以根据需要调整这个值 */
}

.full {
  width: 100%;
  height: 100%;
  --el-menu-bg-color: rgba(200, 22, 30, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, rgba(0, 0, 102, 0.7), rgb(0, 64, 152), rgb(0, 104, 179));
  --el-menu-text-color: #ffffff;
  --el-menu-hover-bg-color: rgba(0, 134, 209, 1);
  --el-menu-item-font-size: 1.1em;
}

.menu-icon {
  margin-right: 4px; /* 或者你需要的间隔大小 */
}

.el-menu-item:hover {
  background-color: rgb(0, 134, 209);
  color: #fff;
}

.logo {
  width: 75%;
  /* Adjust as needed */
  height: auto;
  /* Adjust as needed */
  margin: 20px;
  /* Adjust as needed */
}
</style>

<style>
.el-sub-menu__title {
  font-size: 1.2em !important;
  /* font-weight: bold !important; */
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
