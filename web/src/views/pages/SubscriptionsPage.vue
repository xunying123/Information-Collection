<template>
  <div class="subscriptions-page">
    <h1>用户订阅 - 网站源管理</h1>
    <div class="section">
      <div class="source-header">
        <h2 style="display: inline-block; margin-right: 10px">网站源列表</h2>
        <div style="display: inline-block">
          <el-button type="info" @click="exportSources" size="small" round>导出网站源</el-button>
          <el-upload
            action=""
            :before-upload="importSources"
            :show-file-list="false"
            style="display: inline-block; margin-left: 10px"
          >
            <el-button type="success" size="small" round>导入网站源</el-button>
          </el-upload>
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
        <p v-for="source in sources" :key="source.id" class="scrollbar-item">
          <strong>{{ source.category }}</strong> - {{ source.name }} -
          <a :href="source.url" target="_blank">{{ source.url }}</a>
        </p>
      </el-scrollbar>
    </div>
    <div class="section">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="添加网站源" name="add-source">
          <el-form :model="newSource" ref="sourceForm" label-width="120px">
            <el-form-item label="网站名称" prop="name" size="large">
              <el-autocomplete
                v-model="newSource.name"
                :fetch-suggestions="querySearch"
                placeholder="请输入网站名称"
                @select="handleSelect"
                clearable
              >
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
              <el-autocomplete
                v-model="sourceToDelete.name"
                :fetch-suggestions="querySourceSearch"
                placeholder="输入要删除的网站名称"
                @select="handleSourceSelect"
                clearable
              >
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
  </div>
  <el-divider></el-divider>
</template>

<script setup lang="ts">
import { ref, reactive, inject, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { filter_subscribe_key } from '@/key'
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'

const filter_subscribe = inject(filter_subscribe_key)!
const activeTab = ref('add-source')
const newSource = ref<SiteItem>({ id: 0, cate_id: 0, category: '', name: '', url: '', icon: '' })
const sourceToDelete = reactive({ name: '' })
const sources = ref<SiteItem[]>([])
const allSources = ref<SiteItem[]>([])

onMounted(() => {
  loadSources()
  loadSubscribedSources()
})

function loadSources() {
  fetch(`${server}/site`)
    .then((r) => r.json())
    .then((data: SiteItem[]) => {
      allSources.value = data
    })
    .catch((error) => {
      console.error('Error fetching sources:', error)
    })
}

function loadSubscribedSources() {
  fetch(`${server}/subscribe`)
    .then((r) => r.json())
    .then((data) => {
      sources.value = data.sites
    })
    .catch((error) => {
      console.error('Error fetching subscribed sources:', error)
    })
}

function saveFilter() {
  localStorage.setItem('filter_subscribe', filter_subscribe.value.toString())
}

function addSource() {
  const sitesId = [newSource.value.id]
  const keepUserExisted = true

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
    .then((response) => response.json())
    .then((data) => {
      if (data.code === 0) {
        console.log('Subscription added successfully')
        loadSubscribedSources()
        newSource.value = { id: 0, cate_id: 0, category: '', name: '', url: '', icon: '' }
        ElNotification({
          title: '成功',
          message: '网站源添加成功',
          type: 'success'
        })
      } else {
        console.error(`Error: ${data.msg}`)
      }
    })
    .catch((error) => {
      console.error('Error:', error)
      ElNotification({
        title: '错误',
        message: '添加网站源失败: ' + error,
        type: 'error'
      })
    })
}

function deleteSource() {
  const site = sources.value.find((s) => s.name === sourceToDelete.name)
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
      .then((response) => response.json())
      .then((data) => {
        if (data.code === 0) {
          loadSubscribedSources()
          sourceToDelete.name = ''
          ElNotification({
            title: '成功',
            message: '网站源删除成功',
            type: 'success'
          })
        } else {
          throw new Error(data.msg)
        }
      })
      .catch((error) => {
        ElNotification({
          title: '错误',
          message: '删除网站源失败: ' + error,
          type: 'error'
        })
      })
  }
}

function importSources(file: File) {
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const content = e.target?.result as string
      const sites = JSON.parse(content)
      console.log(sites)
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
        .then((response) => response.json())
        .then((data) => {
          if (data.code === 0) {
            loadSubscribedSources()
            ElNotification({
              title: '成功',
              message: '网站源导入成功',
              type: 'success'
            })
          } else {
            throw new Error(data.msg)
          }
        })
        .catch((error) => {
          ElNotification({
            title: '错误',
            message: '导入网站源失败: ' + error,
            type: 'error'
          })
        })
    }
    reader.readAsText(file)
  }
}

function exportSources() {
  const content = JSON.stringify(
    sources.value.map((source) => ({
      id: source.id,
      category: source.category,
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
