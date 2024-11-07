<template>
    <div class="user-page">
        <h1>用户订阅</h1>
        <div class="section">
            <div class="source-header">
                <h2 style="display: inline-block; margin-right: 10px;">网站源列表</h2>
                <div style="display: inline-block;">
                    <el-button type="info" @click="exportSources" size="small" round>导出网站源</el-button>
                    <el-upload action="" :before-upload="importSources" :show-file-list="false"
                        style="display: inline-block; margin-left: 10px;">
                        <el-button type="success" size="small" round>导入网站源</el-button>
                    </el-upload>
                </div>
            </div>
            <el-switch v-model="filter_subscribe" class="mb-2" active-text="仅显示订阅的网站" inactive-text="显示全部网站"
                @change="saveFilter" />
            <el-scrollbar class="source-scrollbar" height="180px" :always="true">
                <p v-for="source in sources" :key="source.id" class="scrollbar-item">
                    <strong>{{ source.category }}</strong> - {{ source.name }} - <a :href="source.url"
                        target="_blank">{{ source.url }}</a>
                </p>
            </el-scrollbar>
        </div>
        <div class="section">
            <el-tabs v-model="activeTab">
                <el-tab-pane label="添加网站源" name="add-source">
                    <el-form :model="newSource" ref="sourceForm" label-width="120px">
                        <el-form-item label="网站名称" prop="name" size="large">
                            <el-autocomplete v-model="newSource.name" :fetch-suggestions="querySearch"
                                placeholder="请输入网站名称" @select="handleSelect" clearable>
                                <template #default="{ item }">
                                    <div class="name">{{ item.name }}</div>
                                </template>
                            </el-autocomplete>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="addSource" size="large">添加</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <el-tab-pane label="删除网站源" name="remove-source">
                    <el-form :model="sourceToDelete" label-width="120px">
                        <el-form-item label="网站名称" size="large">
                            <el-autocomplete v-model="sourceToDelete.name" :fetch-suggestions="querySourceSearch"
                                placeholder="输入要删除的网站名称" @select="handleSourceSelect" clearable>
                                <template #default="{ item }">
                                    <div class="name">{{ item.name }}</div>
                                </template>
                            </el-autocomplete>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="danger" size="large" @click="deleteSource">删除</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
            </el-tabs>


        </div>
        <el-divider></el-divider>
        <div class="section">
            <div class="keyword-header">
                <h2 style="display: inline-block; margin-right: 10px;">关键词列表</h2>
                <div style="display: inline-block;">
                    <el-button type="info" @click="exportKeywords" size="small" round>导出关键词</el-button>
                    <el-upload action="" :before-upload="importKeywords" :show-file-list="false"
                        style="display: inline-block; margin-left: 10px; margin-right: 10px;">
                        <el-button type="success" size="small" round>导入关键词</el-button>
                    </el-upload>
                    <!-- <el-button type="danger" @click="clearKeywords" size="small" round>清空关键词</el-button> -->
                    <el-popconfirm title="此操作将清空所有关键词，是否继续？" confirm-button-text="确定" cancel-button-text="取消"
                        icon="el-icon-question" @confirm="clearKeywords">
                        <template #reference>
                            <el-button type="danger" size="small" round>清空关键词</el-button>
                        </template>
                    </el-popconfirm>
                </div>
            </div>
            <el-switch v-model="filter_keyword" class="mb-2" active-text="仅显示订阅关键词相关的文章" inactive-text="显示全部文章"
                @change="saveFilter" />
            <div class="keyword-tags">
                <el-tag v-for="keyword in keywords" :key="keyword.id" round :type="getRandomTagType()" size="large">
                    {{ keyword.name }}
                </el-tag>
            </div>
        </div>
        <div class="section">
            <el-tabs v-model="activeKeywordTab">
                <el-tab-pane label="添加关键词" name="add-keyword">
                    <el-form :model="newKeyword" ref="keywordForm" label-width="120px">
                        <el-form-item label="关键词" prop="name" size="large">
                            <el-autocomplete v-model="newKeyword.name" :fetch-suggestions="queryAllKeywordSearch"
                                placeholder="请输入关键词" @select="handAllKeywordleSelect" clearable>
                                <template #default="{ item }">
                                    <div class="name">{{ item.name }}</div>
                                </template>
                            </el-autocomplete>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="addKeyword" size="large">添加</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <el-tab-pane label="删除关键词" name="remove-keyword">
                    <el-form :model="keywordToDelete" label-width="120px">
                        <el-form-item label="关键词" size="large">
                            <el-autocomplete v-model="keywordToDelete.name" :fetch-suggestions="queryKeywordSearch"
                                placeholder="输入要删除的关键词" @select="handleKeywordSelect" clearable>
                                <template #default="{ item }">
                                    <div class="name">{{ item.name }}</div>
                                </template>
                            </el-autocomplete>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="danger" size="large" @click="deleteKeyword">删除</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
            </el-tabs>
            <el-divider></el-divider>
        </div>

        <div class="section">
            <el-popconfirm title="确定退出登录吗？" confirm-button-text="确定" cancel-button-text="取消" icon="el-icon-question"
                @confirm="logout">
                <template #reference>
                    <div class="button-container">
                        <el-button size="large" type="danger">退出登录</el-button>
                    </div>
                </template>
            </el-popconfirm>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, inject, onMounted, type Ref } from 'vue'
import { ElPopconfirm, ElNotification } from 'element-plus'
import { filter_subscribe_key, filter_keyword_key, user_key } from '@/key'
import { server, jaccount_client_id } from '@/const'
import type { Keyword, SiteItem } from '@/api_interface'

let filter_subscribe = inject(filter_subscribe_key)!;
let filter_keyword = inject(filter_keyword_key)!;

const user = inject(user_key)!

const activeTab = ref('add-source')
const activeKeywordTab = ref('add-keyword')

const newSource = ref<SiteItem>({ id: 0, cate_id: 0, category: '', name: '', url: '', icon: '' })
const sourceToDelete = reactive({ name: '' })
const newKeyword = reactive({ name: '' })
const keywordToDelete = reactive({ name: '' })

const sources = ref<SiteItem[]>([])
const allSources = ref<SiteItem[]>([])

const keywords: Ref<Keyword[]> = ref([])
const allKeywords: Ref<Keyword[]> = ref([])

const tagTypes = ['primary', 'success', 'warning', 'danger']

const loadSources = () => {
    try {
        fetch(`${server}/site`)
            .then((r) => r.json())
            .then((data: SiteItem[]) => {
                allSources.value = data
            })
    } catch (error) {
        console.error('Error fetching sources:', error)
    }
}

const loadSubscribedSources = () => {
    try {
        fetch(`${server}/subscribe`)
            .then((r) => r.json())
            .then((data) => {
                sources.value = data.sites
            })
    } catch (error) {
        console.error('Error fetching subscribed sources:', error)
    }
}

const loadAllKeywords = () => {
    try {
        fetch(`${server}/keyword?personal=false`)
            .then((r) => r.json())
            .then((data) => {
                allKeywords.value = data.map((item: any) => ({ id: item.id, name: item.word }))
            })
    } catch (error) {
        console.error('Error fetching keywords:', error)
    }
}

const loadKeywords = () => {
    try {
        fetch(`${server}/keyword?personal=true`)
            .then((r) => r.json())
            .then((data) => {
                keywords.value = data.map((item: any) => ({ id: item.id, name: item.word }))
            })
    } catch (error) {
        console.error('Error fetching keywords:', error)
    }
}

onMounted(() => {
    loadSources()
    loadSubscribedSources()
    loadAllKeywords()
    loadKeywords()
})

function saveFilter() {
    localStorage.setItem("filter_subscribe", filter_subscribe.value.toString())
    localStorage.setItem("filter_keyword", filter_keyword.value.toString())
}

function getRandomTagType() {
    const randomIndex = Math.floor(Math.random() * tagTypes.length)
    return tagTypes[randomIndex]
}

function addSource() {
    const sitesId = [newSource.value.id];
    const keepUserExisted = true;

    if (!Array.isArray(sitesId)) {
        console.error("invalid request: sites_id is not an array");
        return;
    }

    for (const siteId of sitesId) {
        if (typeof siteId !== 'number') {
            console.error("invalid request: site_id is not a number");
            return;
        }
    }
    fetch(`${server}/subscribe`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sites_id: sitesId,
            keep_user_existed: keepUserExisted
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.code === 0) {
                console.log("Subscription added successfully");
                loadSubscribedSources();
                newSource.value = { id: 0, cate_id: 0, category: '', name: '', url: '', icon: '' };
                ElNotification({
                    title: '成功',
                    message: '网站源添加成功',
                    type: 'success',
                });
            } else {
                console.error(`Error: ${data.msg}`);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            ElNotification({
                title: '错误',
                message: '添加网站源失败: ' + error,
                type: 'error',
            });
        });
}

function deleteSource() {
    const site = sources.value.find(s => s.name === sourceToDelete.name)
    if (site) {
        fetch(`${server}/subscribe`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                site_id: site.id
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {
                    loadSubscribedSources()
                    sourceToDelete.name = ''
                    ElNotification({
                        title: '成功',
                        message: '网站源删除成功',
                        type: 'success',
                    })
                } else {
                    throw new Error(data.msg)
                }
            })
            .catch(error => {
                ElNotification({
                    title: '错误',
                    message: '删除网站源失败: ' + error,
                    type: 'error',
                })
            })
    }
}

function importSources(file: File) {
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target?.result as string;
            const sites = JSON.parse(content);
            console.log(sites);
            fetch(`${server}/subscribe`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sites_id: sites.map((site: any) => site.id),
                    keep_user_existed: true
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.code === 0) {
                        loadSubscribedSources()
                        ElNotification({
                            title: '成功',
                            message: '网站源导入成功',
                            type: 'success',
                        });
                    } else {
                        throw new Error(data.msg);
                    }
                })
                .catch(error => {
                    ElNotification({
                        title: '错误',
                        message: '导入网站源失败: ' + error,
                        type: 'error',
                    });
                });
        };
        reader.readAsText(file);
    }
}

function exportSources() {
    const content = JSON.stringify(sources.value.map(source => ({
        id: source.id,
        category: source.category,
        name: source.name,
        url: source.url
    })));
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'subscriptions.json';
    a.click();
    URL.revokeObjectURL(url);
}

function addKeyword() {
    const trimmedKeyword = newKeyword.name.trim();
    if (trimmedKeyword) {
        fetch(`${server}/keyword`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                words: [trimmedKeyword],
                add_for_user: true
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {
                    loadKeywords()
                    newKeyword.name = ''
                    ElNotification({
                        title: '成功',
                        message: '关键词添加成功',
                        type: 'success',
                    })
                } else {
                    throw new Error(data.msg)
                }
            })
            .catch(error => {
                ElNotification({
                    title: '错误',
                    message: '添加关键词失败: ' + error,
                    type: 'error',
                })
            })
    }
}

function clearKeywords() {
    fetch(`${server}/keyword`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            words: [],
            add_for_user: true,
            keep_user_existed: false
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.code === 0) {
                keywords.value = []
                ElNotification({
                    title: '成功',
                    message: '关键词已清空',
                    type: 'success',
                })
            } else {
                throw new Error(data.msg)
            }
        })
        .catch(error => {
            ElNotification({
                title: '错误',
                message: '清空关键词失败: ' + error,
                type: 'error',
            })
        })
}

function deleteKeyword() {
    const keyword = keywords.value.find(k => k.name === keywordToDelete.name)
    if (keyword) {
        fetch(`${server}/keyword`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword_id: keyword.id
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.code === 0) {
                    loadKeywords()
                    keywordToDelete.name = ''
                    ElNotification({
                        title: '成功',
                        message: '关键词删除成功',
                        type: 'success',
                    })
                } else {
                    throw new Error(data.msg)
                }
            })
            .catch(error => {
                ElNotification({
                    title: '错误',
                    message: '删除关键词失败: ' + error,
                    type: 'error',
                })
            })
    }
}

function importKeywords(file: File) {
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target?.result as string;
            const words = JSON.parse(content);
            console.log(words);
            fetch(`${server}/keyword`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    words: words,
                    add_for_user: true,
                    keep_user_existed: true
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.code === 0) {
                        loadKeywords()
                        ElNotification({
                            title: '成功',
                            message: '关键词导入成功',
                            type: 'success',
                        });
                    } else {
                        throw new Error(data.msg);
                    }
                })
                .catch(error => {
                    ElNotification({
                        title: '错误',
                        message: '导入关键词失败: ' + error,
                        type: 'error',
                    });
                });
        };
        reader.readAsText(file);
    }
}

function exportKeywords() {
    const content = JSON.stringify(keywords.value.map(keyword => keyword.name));
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keywords.json';
    a.click();
    URL.revokeObjectURL(url);
}

function createFilter(queryString: string) {
    return (source: SiteItem | Keyword) => source.name.toLowerCase().includes(queryString.toLowerCase())
}

const querySearch = (queryString: string, cb: (results: SiteItem[]) => void) => {
    const results = queryString ? allSources.value.filter(createFilter(queryString)) : allSources.value
    cb(results)
}

function querySourceSearch(queryString: string, cb: (results: SiteItem[]) => void) {
    const results = queryString ? sources.value.filter(createFilter(queryString)) : sources.value
    cb(results)
}

function queryAllKeywordSearch(queryString: string, cb: (results: Keyword[]) => void) {
    const results = queryString ? allKeywords.value.filter(createFilter(queryString)) : allKeywords.value
    cb(results)
}

function queryKeywordSearch(queryString: string, cb: (results: Keyword[]) => void) {
    const results = queryString ? keywords.value.filter(createFilter(queryString)) : keywords.value
    cb(results)
}

const handleSelect = (item: SiteItem) => {
    newSource.value = item
}

function handleSourceSelect(item: SiteItem) {
    sourceToDelete.name = item.name
}

function handAllKeywordleSelect(item: Keyword) {
    newKeyword.name = item.name
}

function handleKeywordSelect(item: Keyword) {
    keywordToDelete.name = item.name
}

const logout = async () => {
    if (!user)
        // impossible path ?
        return
    fetch(`${server}/logout`, { method: 'POST' })
        .then((r) => r.json())
        .then((d) => {
            if (d.code == 0)
                ElNotification({
                    title: '成功',
                    message: '退出登录成功',
                    type: 'success',
                    duration: 2000,
                    onClose: () => {
                        user.value = null
                        location.reload()
                        window.location.href = `http://jaccount.sjtu.edu.cn/oauth2/logout?client_id=${jaccount_client_id}&post_logout_redirect_uri=${encodeURIComponent(window.location.href)}`
                    }
                })
            else throw new Error(d.msg)
        })
        .catch((e) => {
            ElNotification({
                title: '错误',
                message: '退出登录失败: ' + e,
                type: 'error',
            })
        })
}
</script>

<style scoped>
.user-page {
    padding: 16px;
    background: rgba(255, 255, 255, 0.8);
    /* 半透明背景 */
    border-radius: 8px;
    /* 圆角 */
    max-width: 800px;
    /* 最大宽度 */
    margin: 40px auto;
    /* 垂直居中，顶部有间距 */
}

.section {
    margin-bottom: 24px;
}

.el-tabs {
    margin-bottom: 20px;
}

.el-divider {
    margin: 20px 0;
}

.scrollbar-item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    margin: 12px;
    text-align: center;
    border-radius: 4px;
    background: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
}

.keyword-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
}

.button-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>