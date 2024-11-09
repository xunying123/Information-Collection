<script lang="ts" setup>
import { inject, onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router';
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'
import { ElScrollbar } from 'element-plus'
import UserCard from '@/components/UserCard.vue'
import UpdateSVG from '@/components/svg/UpdateSVG.vue'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import FolderPlusSVG from '@/components/svg/FolderPlusSVG.vue'
import LayersSVG from '@/components/svg/LayersSVG.vue'
import { filter_subscribe_key, user_key } from '@/key'

interface CateSite {
  cate_id: number
  cate_name: string
  sites: SiteItem[]
}

let filter_subscribe = inject(filter_subscribe_key)!;
const user = inject(user_key)!
const router = useRouter();

let sites = reactive<CateSite[]>([])

function loadSites() {
  fetch(`${server}/site?subscribe=${filter_subscribe.value ? "true" : "false"}`)
    .then((r) => r.json())
    .then((data: SiteItem[]) => {
      let tmp_sites: CateSite[] = []
      let cateSites: CateSite = { cate_id: 0, cate_name: '', sites: [] }
      for (let site of data) {
        if (site.cate_id != cateSites.cate_id) {
          if (cateSites.cate_id != 0) tmp_sites.push(cateSites)
          cateSites = { cate_id: site.cate_id, cate_name: site.category, sites: [] }
        }
        cateSites.sites.push(site)
      }
      if (cateSites.cate_id != 0) tmp_sites.push(cateSites)
      sites.splice(0, sites.length)
      sites.push(...tmp_sites)
    })
}

function handleSubMenuClick(index: string) {
  router.push(index)
}

watch(filter_subscribe, () => {
  loadSites()
})
onMounted(() => {
  loadSites()
})
</script>

<template>
  <div class="full">
    <el-scrollbar>
      <router-link to="/">
        <img src="https://www.sjtu.edu.cn/resource/assets/img/LogoWhite.png" class="logo" />
      </router-link>
      <router-link to="/user">
        <UserCard />
      </router-link>
      <el-menu class="el-menu-vertical-demo" :router="true" @open="handleSubMenuClick" @close="handleSubMenuClick">
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
        <el-menu-item index="/managesites" v-if="user?.is_admin">
          <FolderPlusSVG class="menu-icon" />
          <span class="menu-top">增删网站</span>
        </el-menu-item>
        <el-sub-menu v-for:="cate in sites" :index="`/category/` + String(cate.cate_id)">
          <template #title>
            <el-icon>
              <Location />
            </el-icon>
            <span>{{ cate.cate_name }}</span>
          </template>
          <el-menu-item v-for:="site in cate.sites" :index="`/site/` + site.id" style="margin-left: 2em;">{{
            site.name
            }}</el-menu-item>
        </el-sub-menu>
        <el-menu-item>
          <div style="margin-bottom: 1.2em; margin-left: 0.5em;">
            <router-link to="/user/subscriptions">
              <el-button plain type="primary">管理订阅源</el-button>
            </router-link>
            <router-link to="/user/keywords">
              <el-button plain type="primary">管理关键词</el-button>
            </router-link>
          </div>
        </el-menu-item>
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
  pointer-events: none;
  /* 添加这一行 */
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
  margin-right: 4px;
  /* 或者你需要的间隔大小 */
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
