<script lang="ts" setup>
import { server } from '@/const'
import { reactive } from 'vue'
import type { SiteItem } from '@/api_interface'
import { ElScrollbar } from 'element-plus'

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
    <el-scrollbar height="100vh">
      <el-menu class="el-menu-vertical-demo" :router="true">
        <el-menu-item index="/">
          <el-icon class="el-icon-menu"></el-icon>
          <span class="menu-top">全部</span>
        </el-menu-item>
        <el-menu-item index="/bookmarks">
          <el-icon class="el-icon-menu"></el-icon>
          <span class="menu-top">书签列表</span>
        </el-menu-item>
        <el-sub-menu v-for:="cate in sites" :index="cate.cate_name">
          <template #title>
            <el-icon> </el-icon>
            <span>{{ cate.cate_name }}</span>
          </template>
          <el-menu-item v-for:="site in cate.sites" :index="`/site/` + site.id">{{ site.name }}</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.full {
  width: 100%;
  height: 100%;
  --el-menu-bg-color: rgba(200, 22, 30, 0);
  --el-menu-active-color: #ffffff;
  background: linear-gradient(180deg, #960018, rgb(167, 32, 56), #953232);
  --el-menu-text-color: #ffffff;
  --el-menu-hover-bg-color: rgba(200, 22, 30, 1);
  --el-menu-item-font-size: 1.1em;
}

.el-menu-item:hover {
  background-color: rgb(200, 22, 30);
  color: #fff;
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
</style>
