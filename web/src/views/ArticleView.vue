<script setup lang="ts">
import { computed, defineProps, ref, watch } from 'vue'
import type { Page } from '@/interface'
import { server } from '@/const'

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
</script>

<template>
    <el-aside class="details-area">
        <!-- 独立功能区 -->
        <div class="top-bar">
            <router-link :to="{ name: 'site-home' }" class="close-button">✕</router-link>
        </div>
        <!-- 文章内容区域 -->
        <div class="article-content">
            <h2>{{ article.title }}</h2>
            <div v-html="content"></div>
        </div>
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
    overflow: hidden;
    height: calc(100vh - 5em); /* 高度略短于页面 */
    margin: 1.5em; /* 调整为较小的外边距 */
    display: flex;
    flex-direction: column; /* 使内容上下排列 */
}

.top-bar {
    background-color: #fefefe;
    padding: 8px 15px; /* 上下的 padding 变小，左右保持 */
    border-bottom: 1px solid #ccc; /* 分隔线 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 轻微阴影效果 */
    flex-shrink: 0; /* 防止压缩 */
    display: flex;
    justify-content: flex-end;
}

.close-button {
    cursor: pointer;
    font-size: 20px; /* 调整字体大小，使其与缩短的 bar 匹配 */
    color: #666;
    transition: color 0.3s ease;
}

.close-button:hover {
    color: #ff5f5f; /* 鼠标悬停时改变颜色 */
}

.article-content {
    padding: 25px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #444;
    line-height: 1.6;
    overflow-y: auto; /* 增加垂直滚动条 */
    flex-grow: 1; /* 占据剩余空间 */
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
</style>
