<script lang="ts" setup>
import { inject, onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'
import { ElScrollbar } from 'element-plus'
import UserCard from '@/components/UserCard.vue'
import UpdateSVG from '@/components/svg/UpdateSVG.vue'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import FolderPlusSVG from '@/components/svg/FolderPlusSVG.vue'
import LayersSVG from '@/components/svg/LayersSVG.vue'
import HelpSVG from '@/components/svg/HelpSVG.vue'
import { filter_subscribe_key, user_key } from '@/key'

interface CateSite {
  cate_id: number
  cate_name: string
  sites: SiteItem[]
}

let filter_subscribe = inject(filter_subscribe_key)!
const user = inject(user_key)!
const router = useRouter()

let sites = reactive<CateSite[]>([])

function loadSites() {
  fetch(`${server}/site?subscribe=${filter_subscribe.value ? 'true' : 'false'}`)
    .then((r) => r.json())
    .then((data: SiteItem[]) => {
      let tmp_sites: CateSite[] = []
      let cateSites: CateSite = { cate_id: 0, cate_name: '', sites: [] }
      for (let site of data) {
        if (site.cate_id != cateSites.cate_id) {
          if (cateSites.cate_id != 0) tmp_sites.push(cateSites)
          cateSites = { cate_id: site.cate_id, cate_name: site.category, sites: [] }
        }
        if (site.name == '上海交通大学')
          // push to the front
          cateSites.sites.unshift(site)
        else cateSites.sites.push(site)
      }
      if (cateSites.cate_id != 0) tmp_sites.unshift(cateSites)
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
    <router-link to="/">
      <img src="https://www.sjtu.edu.cn/resource/assets/img/LogoWhite.png" class="logo" />
    </router-link>
    <router-link to="/user">
      <UserCard />
    </router-link>
    <ElScrollbar class="scrach-height">
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
          <el-menu-item
            v-for:="site in cate.sites"
            :index="`/site/` + site.id"
            style="margin-left: 2em"
            >{{ site.name }}</el-menu-item
          >
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
}

.full {
  display: flex;
  flex-direction: column;
}

.scrach-height {
  flex-grow: 1;
  overflow: auto;
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
  height: auto;
  margin-left: 20px;
  margin-top: 0.2em;
}

.bottom-buttons {
  display: flex;
  margin: 0.5em;
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
