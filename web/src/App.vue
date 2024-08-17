<script lang="ts" setup>
import { server } from '@/const'
import { reactive } from 'vue'
import { RouterView } from 'vue-router'

interface Site {
  id: number
  name: string
  url: string
  cate_id: number
  category: string
}

interface CateSite {
  cate_id: number
  cate_name: string
  sites: Site[]
}

let sites = reactive<CateSite[]>([])

fetch(`${server}/site`)
  .then((r) => r.json())
  .then((data) => {
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
  <div class="common-layout full-height">
    <el-container>
      <el-aside width="20em" style="background-color: blue" class="full-height">
        <el-menu class="el-menu-vertical-demo" :router="true">
          <el-sub-menu v-for:="cate in sites" :index="cate.cate_name">
            <template #title>
              <el-icon>
              </el-icon>
              <span>{{ cate.cate_name }}</span>
            </template>
            <el-menu-item v-for:="site in cate.sites" :index="`/site/` + site.id">{{ site.name }}</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <el-main class="full-height">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.full-height {
  height: 100vh;
}
</style>
