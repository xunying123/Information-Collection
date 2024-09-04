<template>
    <el-tabs v-model="activeTab">
        <!-- 增加网站的 Tab -->
        <el-tab-pane label="增加网站" name="add-site" size="large">
            <el-form :model="newSite" ref="siteForm" label-width="120px">
                <el-form-item label="网站类别" prop="category" size="large">
                    <!-- <el-input v-model="newSite.category" placeholder="请输入类别"></el-input> -->
                    <el-autocomplete v-model="newSite.category" :fetch-suggestions="queryClassSearch"
                        popper-class="my-autocomplete" placeholder="请输入类别" @select="handleSelect" clearable>
                        <template #default="{ item }">
                            <div class="name">{{ item }}</div>
                        </template>
                    </el-autocomplete>
                </el-form-item>
                <el-form-item label="网站名称" prop="name" size="large">
                    <el-input v-model="newSite.name" placeholder="请输入网站名称"></el-input>
                </el-form-item>
                <el-form-item label="网站链接" prop="url" size="large">
                    <el-input v-model="newSite.url" placeholder="请输入链接"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="addSite" size="large"
                        :disabled="!(newSite.category && newSite.name && newSite.url)">提交</el-button>
                    <el-button @click="resetForm" size="large">重置</el-button>
                </el-form-item>
            </el-form>
        </el-tab-pane>

        <!-- 删除网站的 Tab -->
        <el-tab-pane label="删除网站" name="remove-site">
            <el-form :model="siteToDelete" label-width="120px">
                <el-form-item label="网站名称" size="large">
                    <el-autocomplete v-model="siteToDelete.name" :fetch-suggestions="querySearch"
                        popper-class="my-autocomplete" placeholder="输入要删除的网站名称" @select="handleSelect" clearable>
                        <template #default="{ item }">
                            <div class="name">{{ item.name }}</div>
                            <span class="link">{{ item.url }}</span>
                        </template>
                    </el-autocomplete>
                </el-form-item>
                <el-form-item>
                    <el-popconfirm width="280" title="确认删除该网站吗？" @cancel="onCancel" @confirm="deleteSite">
                        <template #reference>
                            <el-button type="danger" size="large">删除</el-button>
                        </template>
                        <template #actions="{ confirm, cancel }">
                            <el-button size="small" @click="cancel">取消</el-button>
                            <el-button type="danger" size="small" :disabled="!clicked" @click="confirm">
                                确认
                            </el-button>
                        </template>
                    </el-popconfirm>
                </el-form-item>
            </el-form>
        </el-tab-pane>
    </el-tabs>
</template>

<script lang="ts" setup>
import { onMounted, ref, reactive } from 'vue'
import { ElNotification } from 'element-plus'
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'

// Active tab
const activeTab = ref('add-site')

// New site form model
const newSite = reactive({
    category: '',
    name: '',
    url: ''
})

// Site to delete form model
const siteToDelete = reactive({
    name: ''
})

// interface SiteItem {
//     name: string
//     link: string
// }

const Sites = ref<SiteItem[]>([])
const categories = ['科教要闻', '院校动态', '国际视野']

const queryClassSearch = (queryString: string, cb: any) => {
    const results = categories.filter(category => category.includes(queryString))
    cb(results)
}

// Fetch site suggestions from server (dummy for now)
const querySearch = (queryString: string, cb: any) => {
    const results = queryString
        ? Sites.value.filter(createFilter(queryString))
        : Sites.value
    // call callback function to return suggestions
    cb(results)
}

const createFilter = (queryString: string) => {
    return (site: SiteItem) => {
        return (
            site.name.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        )
    }
}

const handleSelect = (item: string | SiteItem) => {
    if (typeof item === 'string') {
        newSite.category = item
    } else {
        siteToDelete.name = item.name
    }
}

onMounted(async () => {
    Sites.value = await loadAll()
})

const clicked = ref(false)
function onCancel() {
    clicked.value = true
}

// Add site function
const addSite = async () => {
    if (!newSite.category || !newSite.name || !newSite.url) {
        ElNotification({
            title: '添加失败',
            message: '请填写完整信息!',
            type: 'error'
        });
        return
    }

    const response = await fetch(`${server}/site/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: newSite.name,
            url: newSite.url,
            cate_id: categories.indexOf(newSite.category) + 1,
            icon: ""
        })
    })

    if (response.ok) {
        ElNotification({
            title: '添加成功',
            message: `网站 ${newSite.name} 已添加!`,
            type: 'success'
        });
        resetForm()
        location.reload(); 
    } else {
        ElNotification({
            title: '添加失败',
            message: '服务器错误!',
            type: 'error'
        });
    }
}

// Delete site function
const deleteSite = async () => {
    if (!siteToDelete.name) {
        ElNotification({
            title: '删除失败',
            message: '请填写网站名称!',
            type: 'error'
        });
        return
    }
    const site = Sites.value.find(s => s.name === siteToDelete.name)
    if (!site) {
        ElNotification({
            title: '删除失败',
            message: '找不到网站!',
            type: 'error'
        });
        return
    }
    const response = await fetch(`${server}/site/remove`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: site.id,
            force: true
        })
    })

    if (response.ok) {
        ElNotification({
            title: '删除成功',
            message: `网站 ${siteToDelete.name} 已删除!`,
            type: 'success'
        });
        siteToDelete.name = ''
        location.reload(); 
    } else {
        ElNotification({
            title: '删除失败',
            message: '服务器错误!',
            type: 'error'
        });
    }
}

// Reset form function
const resetForm = () => {
    newSite.category = ''
    newSite.name = ''
    newSite.url = ''
}

const loadAll = async (): Promise<SiteItem[]> => {
    return fetch(`${server}/site`)
        .then((r) => r.json())
        .then((data: SiteItem[]) => {
            let sites: SiteItem[] = []
            for (let site of data) {
                sites.push(site)
            }
            return sites
        })
}


</script>

<style scoped>
.el-tabs {
    margin: 20px;
}

.el-form {
    max-width: 600px;
}

.el-form-item {
    margin-bottom: 15px;
}

.el-button {
    margin-right: 10px;
}

.my-autocomplete .name {
    font-weight: bold;
    color: #333;
}

.my-autocomplete .link {
    font-size: 0.8em;
    color: #999;
}

.my-autocomplete li {
    line-height: normal;
    padding: 7px;
}

.my-autocomplete li .name {
    text-overflow: ellipsis;
    overflow: hidden;
}

.my-autocomplete li .addr {
    font-size: 12px;
    color: #b4b4b4;
}

.my-autocomplete li .highlighted .addr {
    color: #ddd;
}
</style>