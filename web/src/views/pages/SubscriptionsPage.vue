<template>
  <div class="subscriptions-page">
    <h1>用户订阅 - 网站源管理</h1>
    <div class="section">
      <div class="source-header">
        <h2 style="display: inline-block; margin-right: 10px">网站源列表</h2>
        <div style="display: inline-block">
          <el-button type="info" size="small" round @click="exportSources"> 导出网站源 </el-button>
          <el-upload
            action=""
            :before-upload="importSources"
            :show-file-list="false"
            style="display: inline-block; margin-left: 10px; margin-right: 10px"
          >
            <el-button type="success" size="small" round> 导入网站源 </el-button>
          </el-upload>
          <el-popconfirm
            title="此操作将清空所有订阅的网站源，是否继续？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-question"
            @confirm="clearSubscriptions"
          >
            <template #reference>
              <el-button type="danger" size="small" round> 清空网站源 </el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
      <el-switch
        v-model="filter_subscribe"
        class="mb-2"
        active-text="仅显示订阅的网站"
        inactive-text="显示全部网站"
        @change="saveFilter"
      />
      <el-scrollbar class="source-scrollbar" height="24em" :always="true">
        <p v-for="source in sources" :key="source.id!" class="scrollbar-item">
          <strong>{{ source.name }}</strong>
          <!-- <a :href="source.url" target="_blank">{{ source.url }}</a> -->
        </p>
      </el-scrollbar>
    </div>
    <div class="section">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="添加网站源" name="add-source">
          <el-form ref="sourceForm" :model="newSource" label-width="120px">
            <el-form-item label="网站名称" prop="name" size="large">
              <el-autocomplete
                v-model="newSource.name"
                :fetch-suggestions="querySearch"
                placeholder="请输入网站名称"
                clearable
                @select="handleSelect"
              >
                <template #default="{ item }">
                  <div class="name">{{ item.cate_name }} - {{ item.name }}</div>
                </template>
              </el-autocomplete>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" @click="addSource"> 添加 </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="删除网站源" name="remove-source">
          <el-form :model="sourceToDelete" label-width="120px">
            <el-form-item label="网站名称" size="large">
              <el-autocomplete
                v-model="sourceToDelete.name"
                :fetch-suggestions="querySourceSearch"
                placeholder="输入要删除的网站名称"
                clearable
                @select="handleSourceSelect"
              >
                <template #default="{ item }">
                  <div class="name">
                    {{ item.name }}
                  </div>
                </template>
              </el-autocomplete>
            </el-form-item>
            <el-form-item>
              <el-button type="danger" size="large" @click="deleteSource"> 删除 </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
  <el-divider />
</template>

<script setup lang="ts">
import { ref, reactive, inject, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { filter_subscribe_key } from '@/key'
import type { SiteItem } from '@/sdk'
import { getCategories, getSubscribe, subscribe, unsubscribe } from '@/sdk'

const filter_subscribe = inject(filter_subscribe_key)!
const activeTab = ref('add-source')
const newSource = ref<SiteItem>({ id: 0, name: '', url: '', icon: '' })
const sourceToDelete = reactive({ name: '' })
const sources = ref<SiteItem[]>([])
const allSources = ref<SiteItem[]>([])

onMounted(() => {
  loadSources()
  loadSubscribedSources()
})

async function loadSources() {
  const { data, error } = await getCategories()
  if (error) {
    console.error(error)
    return
  }
  allSources.value = []
  for (let cate of data!) {
    for (let site of cate.sites!) {
      allSources.value.push(site)
    }
  }
}

async function loadSubscribedSources() {
  const { data, error } = await getSubscribe()
  if (error) {
    console.error(error)
    return
  }
  sources.value = data!
}

function saveFilter() {
  localStorage.setItem('filter_subscribe', filter_subscribe.value.toString())
}

async function addSource() {
  const sitesId = [newSource.value.id!]
  if (!Array.isArray(sitesId)) {
    console.error('invalid request: sites_id is not an array')
    return
  }
  for (const siteId of sitesId) {
    if (typeof siteId !== 'number') {
      console.error('invalid request: site_id is not a number')
      return
    }
  }
  const { data, error } = await subscribe({
    body: {
      sites_id: sitesId,
      keep_user_existed: true
    }
  })
  if (error || data.status !== 200) {
    ElNotification({
      title: '错误',
      message: '添加网站源失败: ' + (error ? error : data.message),
      type: 'error'
    })
    return
  }
  loadSubscribedSources()
  newSource.value = { id: 0, name: '', url: '', icon: '' }
  ElNotification({
    title: '成功',
    message: '网站源添加成功',
    type: 'success'
  })
}

async function deleteSource() {
  const site = sources.value.find((s) => s.name === sourceToDelete.name)
  if (site) {
    const { data, error } = await unsubscribe({ body: site.id! })
    if (error || data.status !== 200) {
      ElNotification({
        title: '错误',
        message: '删除网站源失败: ' + (error ? error : data.message),
        type: 'error'
      })
      return
    }
    loadSubscribedSources()
    sourceToDelete.name = ''
    ElNotification({
      title: '成功',
      message: '网站源删除成功',
      type: 'success'
    })
  }
}

async function importSources(file: File) {
  if (file) {
    const reader = new FileReader()
    reader.onload = async (e) => {
      const content = e.target?.result as string
      const sites = JSON.parse(content)
      const { data, error } = await subscribe({
        body: {
          sites_id: sites.map((site: any) => site.id),
          keep_user_existed: true
        }
      })
      if (error || data.status !== 200) {
        ElNotification({
          title: '错误',
          message: '导入网站源失败: ' + (error ? error : data.message),
          type: 'error'
        })
        return
      }
      loadSubscribedSources()
      ElNotification({
        title: '成功',
        message: '网站源导入成功',
        type: 'success'
      })
    }
    reader.readAsText(file)
  }
}

function exportSources() {
  const content = JSON.stringify(
    sources.value.map((source) => ({
      id: source.id,
      name: source.name,
      url: source.url
    }))
  )
  const blob = new Blob([content], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'subscriptions.json'
  a.click()
  URL.revokeObjectURL(url)
}

async function clearSubscriptions() {
  const { data, error } = await subscribe({
    body: {
      sites_id: [],
      keep_user_existed: false
    }
  })
  if (error || data.status !== 200) {
    ElNotification({
      title: '错误',
      message: '清空网站源失败: ' + (error ? error : data.message),
      type: 'error'
    })
    return
  }
  loadSubscribedSources()
  ElNotification({
    title: '成功',
    message: '网站源清空成功',
    type: 'success'
  })
}

function createFilter(queryString: string) {
  return (source: SiteItem) => source.name.toLowerCase().includes(queryString.toLowerCase())
}

function querySearch(queryString: string, cb: (results: SiteItem[]) => void) {
  const results = queryString
    ? allSources.value.filter(createFilter(queryString))
    : allSources.value
  cb(results)
}

function querySourceSearch(queryString: string, cb: (results: SiteItem[]) => void) {
  const results = queryString ? sources.value.filter(createFilter(queryString)) : sources.value
  cb(results)
}

function handleSelect(item: SiteItem) {
  newSource.value = item
}

function handleSourceSelect(item: SiteItem) {
  sourceToDelete.name = item.name
}
</script>

<style scoped>
.subscriptions-page {
  padding: 8px;
  background: rgba(255, 255, 255, 0.8);
  /* 半透明背景 */
  border-radius: 8px;
  /* 圆角 */
  max-width: 800px;
  /* 最大宽度 */
  margin: 10px auto;
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
</style>
