<script lang="ts" setup>
import { server } from '@/const'
import { reactive } from 'vue'
import type { CateSite } from '@/interface'
import { ElLoading } from 'element-plus';

let sites = reactive<CateSite[]>([])

// let loading = ElLoading.service({
//     lock: true,
//     text: 'Loading',
//     background: 'rgba(0, 0, 0, 0.7)',
// })

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
        // loading.close()
    })
</script>

<template>
    <div class="full">

        <el-menu class="el-menu-vertical-demo" :router="true">
            <router-link :to="{ name: 'home' }">
            <el-menu-item>
                    <el-icon class="el-icon-menu"></el-icon>
                    <span class="menu-top">全部</span>
                </el-menu-item>
            </router-link>
            <router-link :to="{ name: 'bookmarks' }">
            <el-menu-item>
                    <el-icon class="el-icon-menu"></el-icon>
                    <span class="menu-top">书签列表</span>
                </el-menu-item>
            </router-link>
            <el-sub-menu v-for:="cate in sites" :index="cate.cate_name">
                <template #title>
                    <el-icon>
                    </el-icon>
                    <span>{{ cate.cate_name }}</span>
                </template>
                <el-menu-item v-for:="site in cate.sites" :index="`/site/` + site.id">{{ site.name }}</el-menu-item>
            </el-sub-menu>
        </el-menu>
    </div>
</template>

<style scoped>
.full {
    width: 100%;
    height: 100%;
    --el-menu-bg-color: rgba(200, 22, 30, 0);
    --el-menu-active-color: #ffffff;
    background: linear-gradient(180deg, #960018, rgb(167, 32, 56), #632121);
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