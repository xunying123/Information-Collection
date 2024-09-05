<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'
import type { Page } from '@/api_interface'
import { server } from '@/const'
import { is_bookmarked, toggle_bookmark } from '@/bookmark'
import { useClipboard } from '@vueuse/core'
import { ElNotification } from 'element-plus'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import CloseSVG from '@/components/svg/CloseSVG.vue'
import CopySVG from '@/components/svg/CopySVG.vue'
import { NTime } from 'naive-ui'

let props = defineProps({ page_id: String })

const empty_article: Page = {
  id: 0,
  title: '',
  content: '',
  source_url: '',
  site_id: 0,
  site: '',
  cate_id: 0,
  category: '',
  publish_time: '',
  site_icon: ''
}

let article = ref<Page>(empty_article)

function update(prop: typeof props) {
  article.value = empty_article
  if (!prop.page_id) return
  fetch(`${server}/page/${prop.page_id}`)
    .then((r) => r.json())
    .then((data) => {
      article.value = data
    })
}

watch(props, update)
update(props)

let content = computed(() => {
  return article.value.content.split('\n').join('<br>')
})

const { copy } = useClipboard({ legacy: !navigator.clipboard })

function copyLink() {
  const sourceUrl = article.value.source_url
  copy(sourceUrl)
    .then(() => {
      ElNotification({
        title: '复制成功',
        message: '成功复制了文章的链接',
        type: 'success'
      })
    })
    .catch(() => {
      ElNotification({
        title: '复制失败',
        message: '复制文章链接失败，请重试',
        type: 'error'
      })
    })
}
</script>

<template>
  <el-aside class="details-area">
    <!-- 独立功能区 -->
    <div class="top-bar">
      <div class="button-group">
        <router-link :to="{ name: $route.matched[0].name }" class="close-button">
          <CloseSVG />
        </router-link>
        <el-tooltip content="复制链接" effect="light">
          <button @click="copyLink" class="copy-button" tag="复制链接">
            <CopySVG />
          </button>
        </el-tooltip>
        <el-tooltip :content="is_bookmarked(article.id) ? '移除书签' : '加入书签'" effect="light">
          <button @click="toggle_bookmark(article)" class="bookmark-button" tag="书签">
            <BookmarkSvg :fill="is_bookmarked(article.id) ? '#FFD700' : 'none'" />
          </button>
        </el-tooltip>
        <a :href="article.source_url" target="_blank" noopener opreferrer class="flex-right">
          <el-button class="glowing-button" type="primary">查看原文</el-button>
        </a>
      </div>
    </div>
    <!-- 文章内容区域 -->
    <el-scrollbar>
      <div class="article-content" v-loading="article.id == 0">
        <h2 class="article-title">{{ article.title }}</h2>
        <el-divider content-position="center">
          <n-time
            v-if="article.publish_time"
            :time="new Date(article.publish_time)"
            format="yyyy年MM月dd日 hh时mm分"
          />
        </el-divider>
        <div v-html="content"></div>
      </div>
    </el-scrollbar>
  </el-aside>
</template>

<style scoped>
@media (max-width: 768px) {
  .details-area {
    width: 100% !important; /* Adjust as needed */
  }
  .article-content {
    overflow-x: auto; /* Add this line */
  }

  .article-content img {
    max-width: 100%; /* Add this line */
  }
}

.details-area {
  width: 50em;
  background-color: #ffffff;
  position: relative;
  border: 1px solid #ddd;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: auto;
  margin: 1.5em 1.5em 1.5em 0;
  display: grid;
  grid-template-rows: min-content 1fr;
  background-color: rgba(255, 255, 255, 0.7); /* 设置背景颜色为半透明的白色 */
}

.top-bar {
  background-color: #fefefe;
  padding: 8px 15px;
  /* 上下的 padding 变小，左右保持 */
  border-bottom: 1px solid #ccc;
  /* 分隔线 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
  flex-shrink: 0;
  /* 防止压缩 */
  position: sticky;
  top: 0;
  display: flex;
  justify-content: flex-start;
}

.button-group {
  display: flex;
  align-items: center;
  width: 100%;
}

.close-button,
.copy-button,
.bookmark-button {
  margin-right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  color: #222;
  font-size: 24px;
  /* 调整关闭按钮的大小 */
}

.close-button svg,
.copy-button svg,
.bookmark-button svg {
  width: 24px;
  height: 24px;
}

.close-button:hover {
  fill: #f00;
}

.article-content {
  padding: 25px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #444;
  line-height: 1.6;
  overflow-y: auto;
  /* 增加垂直滚动条 */
  flex-grow: 1;
  /* 占据剩余空间 */
}

.article-content h2 {
  font-size: 28px;
  margin-bottom: 25px;
  color: #222;
}

.article-content p {
  font-size: 18px;
  margin-bottom: 20px;
}

.article-content a {
  color: #0056b3;
  text-decoration: none;
  font-weight: 500;
  border-bottom: 2px solid #0056b3;
  padding-bottom: 2px;
  transition:
    color 0.3s ease,
    border-color 0.3s ease;
}

.article-content a:hover {
  color: #003d82;
  border-color: #003d82;
}

.article-title {
  font-weight: bold;
  /* 加粗标题 */
}

.redirect-article-button {
  width: 100vw;
  /* bottom: 0;
    left: 0;
    right: 0; */
  margin-top: 20px;
  position: relative;
}

.glowing-button {
  background: linear-gradient(45deg, rgba(253, 208, 0, 0.8), rgba(240, 131, 0, 0.8));
  background-size: 200% 200%;
  animation: glowing 3s ease infinite;
  border: none;
  color: black;
  font-weight: bold;
  text-transform: uppercase;
  box-shadow:
    0 0 15px rgba(167, 32, 56, 0.4),
    0 0 20px rgba(240, 131, 0, 0.4),
    0 0 25px rgba(253, 208, 0, 0.4);
  position: relative;
}

.bottom-functions {
  display: flex;
  justify-content: center;
  align-items: center;
}

@keyframes glowing {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.bookmark-button svg.filled {
  fill: #ffd700;
  /* 选中状态填充黄色 */
}

.flex-right {
  margin-left: auto;
}
</style>
