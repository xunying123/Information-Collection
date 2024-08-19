<script lang="ts" setup>
import { server } from '@/const'
import { reactive } from 'vue'
import type { CateSite } from '@/interface'

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
</template>
