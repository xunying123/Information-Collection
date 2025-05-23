<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import type { Page } from '@/sdk'
import { is_bookmarked, toggle_bookmark } from '@/bookmark'
import { useClipboard } from '@vueuse/core'
import { ElNotification } from 'element-plus'
import BookmarkSvg from '@/components/svg/BookmarkSvg.vue'
import CloseSVG from '@/components/svg/CloseSVG.vue'
import CopySVG from '@/components/svg/CopySVG.vue'
import { NTime } from 'naive-ui'
import KeywordList from '@/components/KeywordList.vue'
import { getPage } from '@/sdk'

let props = defineProps<{ page_id: string }>()

const empty_article: Page = {
  id: 0,
  title: '',
  content: '',
  full_content: '',
  source_url: '',
  site_id: 0,
  site: '',
  publish_time: '',
  site_icon: '',
  keywords: [],
  score: 0
}

const slide_value = ref(128)
const content_width = computed(() => 178 - slide_value.value)
const isResizing = ref(false)

let article = ref<Page>(empty_article)

async function update(prop: typeof props) {
  article.value = empty_article
  if (!prop.page_id) return
  const { data, error } = await getPage({ path: { page_id: Number(prop.page_id) } })
  if (error) {
    console.error(error)
    return
  }
  article.value = data
}

watch(props, update)
update(props)

let content = computed(() => {
  return article.value.content.split('\n').join('<br>').replace(/[#`*]/g, '')
})

let full_content = computed(() => {
  return article.value.full_content.split('\n').join('<br>').replace(/[#`*]/g, '')
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

// 改进的拖拽调整宽度功能
function handleResizeStart(_event: MouseEvent) {
  isResizing.value = true
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', handleResizeEnd)
  // 防止文本选择
  document.body.style.userSelect = 'none'
}

function handleResize(event: MouseEvent) {
  if (!isResizing.value) return

  // 获取窗口宽度和鼠标位置
  const windowWidth = window.innerWidth
  const mouseX = event.clientX

  // 计算鼠标到窗口右边缘的距离
  const distanceToRight = windowWidth - mouseX + 50

  // 将距离转换为em单位的宽度值 (这里需要调整比例系数来匹配理想的敏感度)
  // 假设1em大约等于16px (标准情况下)，使用一个系数来调整
  const emFactor = 0.06 // 调整此值以改变敏感度
  let emWidth = distanceToRight * emFactor

  // 确保宽度在合理范围内
  emWidth = Math.max(50, Math.min(128, emWidth))

  // 设置slide_value为新的计算值
  slide_value.value = 178 - emWidth
}

function handleResizeEnd() {
  isResizing.value = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', handleResizeEnd)
  document.body.style.userSelect = ''
}

// 组件生命周期钩子
onMounted(() => {
  window.addEventListener('resize', () => {
    // 窗口大小变化时不调整slide_value，只有拖拽时才调整
  })
})

onUnmounted(() => {
  // window.removeEventListener('resize', handleResize)
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', handleResizeEnd)
})
</script>

<template>
  <div class="article-container">
    <div class="resizer" :class="{ active: isResizing }" @mousedown="handleResizeStart">
      <div class="resizer-handle" />
    </div>
    <el-aside class="details-area" :style="{ width: content_width + 'em' }">
      <!-- 独立功能区 -->
      <div class="top-bar">
        <div class="button-group">
          <router-link
            :to="{ name: $route.matched[$route.matched.length - 2].name }"
            class="close-button"
          >
            <CloseSVG />
          </router-link>
          <el-tooltip content="复制链接" effect="light">
            <button class="copy-button" tag="复制链接" @click="copyLink">
              <CopySVG />
            </button>
          </el-tooltip>
          <el-tooltip :content="is_bookmarked(article.id) ? '移除书签' : '加入书签'" effect="light">
            <button class="bookmark-button" tag="书签" @click="toggle_bookmark(article)">
              <BookmarkSvg :fill="is_bookmarked(article.id) ? '#FFD700' : 'none'" />
            </button>
          </el-tooltip>
          <a :href="article.source_url" target="_blank" noopener opreferrer class="flex-right">
            <el-button class="glowing-button" type="primary">查看原文</el-button>
          </a>
        </div>
      </div>
      <!-- 文章内容区域 -->
      <el-scrollbar @wheel.stop>
        <div v-loading="article.id == 0" class="article-content">
          <h2 class="article-title">
            {{ article.title }}
          </h2>
          <KeywordList :keywords="article.keywords" :closable="false" :handle-close="() => {}" />
          <el-divider content-position="center">
            <NTime
              v-if="article.publish_time"
              :time="new Date(article.publish_time)"
              format="yyyy年MM月dd日 HH时mm分"
            />
          </el-divider>
          <!-- <span>{{ article.publish_time }}</span> -->
          <div class="article-view">
            <div class="section">
              <h3 class="section-title">【摘要】</h3>
              <div class="section-content" v-html="content" />
            </div>
            <hr class="divider" />
            <div class="section">
              <h3 class="section-title">【正文】</h3>
              <div class="section-content" v-html="full_content" />
            </div>
          </div>
        </div>
      </el-scrollbar>
    </el-aside>
  </div>
</template>

<style scoped>
.article-container {
  position: relative;
  display: flex;
  height: 100%;
}

@media (max-width: 768px) {
  .details-area {
    width: 100% !important;
    margin-left: 0 !important;
  }

  .article-content {
    overflow-x: auto;
  }

  .article-content img {
    max-width: 100%;
  }

  .resizer,
  .resizer-handle {
    display: none;
  }
}

.resizer {
  position: absolute;
  left: 0;
  top: 0;
  width: 16px;
  height: 100%;
  cursor: ew-resize;
  z-index: 100;
}

.resizer-handle {
  position: absolute;
  left: 6px;
  top: 0;
  width: 4px;
  height: 100%;
  background-color: #d6e6f9;
  transition: background-color 0.2s;
}

.resizer:hover .resizer-handle,
.resizer.active .resizer-handle {
  background-color: #c0cee0;
}

.details-area {
  background-color: #ffffff;
  position: relative;
  border: 1px solid #ddd;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: auto;
  margin: 1.5em 1.5em 1.5em 16px; /* 增加左边距，为拖拽区域留出空间 */
  grid-template-rows: min-content 1fr;
  background-color: rgba(255, 255, 255, 1);
  display: flex;
  flex-direction: column;
  transition: width 0.01s linear; /* 过渡时间极短，确保移动更平滑 */
}

.top-bar {
  background-color: #fefefe;
  padding: 8px 15px;
  border-bottom: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
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

.section-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.article-content {
  padding: 25px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #444;
  line-height: 1.6;
  overflow-y: auto;
  flex-grow: 1;
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
}

.redirect-article-button {
  width: 100vw;
  margin-top: 20px;
  position: relative;
}

.glowing-button {
  background: linear-gradient(45deg, #79bbff, #a0cfff);
  background-size: 200% 200%;
  animation: glowing 3s ease infinite;
  border: none;
  color: rgb(255, 255, 255);
  font-weight: bold;
  text-transform: uppercase;
  position: relative;
}

.divider {
  margin-bottom: 20px;
  margin-top: 20px;
  border: none;
  height: 0.15em;
  background-color: #d9ecff;
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
}

.flex-right {
  margin-left: auto;
}

.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}
</style>
