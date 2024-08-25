<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'
import type { Page } from '@/interface'
import { server } from '@/const'
import { is_bookmarked, toggle_bookmark } from '@/bookmark';
import { useClipboard } from '@vueuse/core'
import { ElNotification } from 'element-plus';

let props = defineProps({ page_id: Number });

const empty_article: Page = {
    id: 0,
    title: '',
    content: '',
    source_url: '',
    site_id: 0,
    site: '',
    cate_id: 0,
    category: ''
};

let article = ref<Page>(empty_article);

function update(prop: typeof props) {
    article.value = empty_article;
    if (!prop.page_id) return;
    fetch(`${server}/page/${prop.page_id}`)
        .then((r) => r.json())
        .then((data) => {
            article.value = data;
        });
}

watch(props, update);
update(props);

let content = computed(() => {
    return article.value.content.split('\n').join('<br>');
});


const { copy } = useClipboard({ legacy: !navigator.clipboard });


function copyLink() {
    const sourceUrl = article.value.source_url;
    copy(sourceUrl)
        .then(() => {
            ElNotification({
                title: '复制成功',
                message: '成功复制了文章的链接',
                type: 'success',
                duration: 0,
            })
        })
        .catch(() => {
            ElNotification({
                title: '复制失败',
                message: '复制文章链接失败，请重试',
                type: 'error',
            })
        });
}

</script>

<template>
    <el-aside class="details-area">
        <!-- 独立功能区 -->
        <div class="top-bar">
            <div class="button-group">
                <router-link :to="{ name: $route.matched[0].name }" class="close-button">
                    <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd"
                            d="M19.207 6.207a1 1 0 0 0-1.414-1.414L12 10.586 6.207 4.793a1 1 0 0 0-1.414 1.414L10.586 12l-5.793 5.793a1 1 0 1 0 1.414 1.414L12 13.414l5.793 5.793a1 1 0 0 0 1.414-1.414L13.414 12l5.793-5.793z"
                            fill="#000000" />
                    </svg>
                </router-link>
                <el-tooltip content="复制链接" effect="light">
                    <button @click="copyLink" class="copy-button" tag="复制链接">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" shape-rendering="geometricPrecision"
                            class="h-6 w-6 stroke-[#95959d] dark:stroke-[#959699]">
                            <path stroke-linecap="round" stroke-linejoin="round" shape-rendering="geometricPrecision"
                                d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244">
                            </path>
                        </svg>
                    </button>
                </el-tooltip>
                <el-tooltip content="标记书签" effect="light">
                    <button @click="toggle_bookmark(article)" class="bookmark-button" tag="书签">
                        <svg v-if="is_bookmarked(article)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                            fill="#FFD700" class="h-6 w-6">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="h-6 w-6">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
                        </svg>
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
                <div v-html="content"></div>
                <div class="bottom-functions">
                    <!-- <el-button @click="redirectToArticle" class="glowing-button redirect-article-button"
                    block>点击跳转原文</el-button> -->
                </div>
            </div>
        </el-scrollbar>
    </el-aside>
</template>

<style scoped>
.details-area {
    width: 50em;
    background-color: #ffffff;
    position: relative;
    border: 1px solid #ddd;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: auto;
    height: calc(100vh - 5em);
    /* 高度略短于页面 */
    margin: 1.5em;
    /* 调整为较小的外边距 */
    display: grid;
    grid-template-rows: min-content 1fr;
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
    transition: color 0.3s ease, border-color 0.3s ease;
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
    box-shadow: 0 0 15px rgba(167, 32, 56, 0.4), 0 0 20px rgba(240, 131, 0, 0.4), 0 0 25px rgba(253, 208, 0, 0.4);
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
    fill: #FFD700;
    /* 选中状态填充黄色 */
}

.flex-right {
    margin-left: auto;
}
</style>
