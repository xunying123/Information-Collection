<template>
  <div class="keywords-page">
    <h1>用户订阅 - 关键词管理</h1>
    <div class="section">
      <div class="keyword-header">
        <h2 style="display: inline-block; margin-right: 10px">关键词列表</h2>
        <div style="display: inline-block">
          <el-button type="info" @click="exportKeywords" size="small" round>导出关键词</el-button>
          <el-upload
            action=""
            :before-upload="importKeywords"
            :show-file-list="false"
            style="display: inline-block; margin-left: 10px; margin-right: 10px"
          >
            <el-button type="success" size="small" round>导入关键词</el-button>
          </el-upload>
          <el-popconfirm
            title="此操作将清空所有关键词，是否继续？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-question"
            @confirm="clearKeywords"
          >
            <template #reference>
              <el-button type="danger" size="small" round>清空关键词</el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
      <el-switch
        v-model="filter_keyword"
        class="mb-2"
        active-text="仅显示订阅关键词相关的文章"
        inactive-text="显示全部文章"
        @change="saveFilter"
      />
      <KeywordList :keywords="keywords" closable :handleClose="handleClose"></KeywordList>
    </div>
    <div class="section">
      <el-tabs v-model="activeKeywordTab">
        <el-tab-pane label="添加关键词" name="add-keyword">
          <el-form :model="newKeyword" ref="keywordForm" label-width="120px">
            <el-form-item label="关键词" prop="word" size="large">
              <el-autocomplete
                v-model="newKeyword.word"
                :fetch-suggestions="queryKeywordSearchAdd"
                placeholder="请输入新关键词或选择已有关键词"
                @select="handleAllKeywordleSelect"
                clearable
              >
                <template #default="{ item }">
                  <div class="name">{{ item.word }}</div>
                </template>
              </el-autocomplete>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addKeyword_" size="large">添加</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="删除关键词" name="remove-keyword">
          <el-form :model="keywordToDelete" label-width="120px">
            <el-form-item label="关键词" size="large">
              <el-autocomplete
                v-model="keywordToDelete.word"
                :fetch-suggestions="queryKeywordSearchDelete"
                placeholder="输入要删除的关键词"
                @select="handleKeywordSelect"
                clearable
              >
                <template #default="{ item }">
                  <div class="name">{{ item.word }}</div>
                </template>
              </el-autocomplete>
            </el-form-item>
            <el-form-item>
              <el-button type="danger" size="large" @click="handelDeleteKeyword">删除</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
  <el-divider></el-divider>
</template>

<script setup lang="ts">
import { ref, reactive, inject, onMounted, type Ref } from 'vue'
import { ElNotification } from 'element-plus'
import { filter_keyword_key } from '@/key'
import type { Keyword } from '@/sdk'
import KeywordList from '@/components/KeywordList.vue'
import { getKeyword, addKeyword, deleteKeyword } from '@/sdk'

const filter_keyword = inject(filter_keyword_key)!
const activeKeywordTab = ref('add-keyword')
const newKeyword = reactive({ word: '' })
const keywordToDelete = reactive({ word: '' })
const keywords: Ref<Keyword[]> = ref([])
const allKeywords: Ref<Keyword[]> = ref([])

onMounted(() => {
  loadAllKeywords()
  loadKeywords()
})

async function loadAllKeywords() {
  const { data, error } = await getKeyword({ query: { personal: false } })
  if (error) {
    console.error(error)
    return
  }
  allKeywords.value = data
}

async function loadKeywords() {
  const { data, error } = await getKeyword({ query: { personal: true } })
  if (error) {
    console.error(error)
    return
  }
  keywords.value = data
}

function saveFilter() {
  localStorage.setItem('filter_keyword', filter_keyword.value.toString())
}

async function addKeyword_() {
  const trimmedKeyword = newKeyword.word.trim()
  if (trimmedKeyword) {
    const { data, error } = await addKeyword({
      body: {
        add_for_user: true,
        keep_user_existed: true,
        words: [trimmedKeyword]
      }
    })
    if (error || data.status !== 200) {
      ElNotification({
        title: '错误',
        message: '添加关键词失败: ' + (error ? error : data.message),
        type: 'error'
      })
      return
    }
    loadKeywords()
    newKeyword.word = ''
    ElNotification({
      title: '成功',
      message: '关键词添加成功',
      type: 'success'
    })
  }
}

async function clearKeywords() {
  const { data, error } = await addKeyword({
    body: {
      add_for_user: true,
      keep_user_existed: false,
      words: []
    }
  })
  if (error || data.status !== 200) {
    ElNotification({
      title: '错误',
      message: '清空关键词失败: ' + (error ? error : data.message),
      type: 'error'
    })
    return
  }
  keywords.value = []
  ElNotification({
    title: '成功',
    message: '关键词已清空',
    type: 'success'
  })
}

async function deleteKeyword_(keyword: Keyword) {
  if (keyword) {
    const { data, error } = await deleteKeyword({ body: { keyword_id: keyword.id } })
    if (error || data.status !== 200) {
      ElNotification({
        title: '错误',
        message: '删除关键词失败: ' + (error ? error : data.message),
        type: 'error'
      })
      return
    }
    loadKeywords()
    ElNotification({
      title: '成功',
      message: '关键词删除成功',
      type: 'success'
    })
  }
}

function handelDeleteKeyword() {
  const keyword = keywords.value.find((k) => k.word === keywordToDelete.word)
  if (keyword) deleteKeyword_(keyword)
}

function handleClose(keyword: Keyword) {
  deleteKeyword_(keyword)
}

async function importKeywords(file: File) {
  if (file) {
    const reader = new FileReader()
    reader.onload = async (e) => {
      const content = e.target?.result as string
      const words = JSON.parse(content)

      const { data, error } = await addKeyword({
        body: {
          add_for_user: true,
          keep_user_existed: true,
          words: words
        }
      })
      if (error || data.status !== 200) {
        ElNotification({
          title: '错误',
          message: '导入关键词失败: ' + (error ? error : data.message),
          type: 'error'
        })
        return
      }
      loadKeywords()
      ElNotification({
        title: '成功',
        message: '关键词导入成功',
        type: 'success'
      })
    }
    reader.readAsText(file)
  }
}

function exportKeywords() {
  const content = JSON.stringify(keywords.value.map((keyword) => keyword.word))
  const blob = new Blob([content], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'keywords.json'
  a.click()
  URL.revokeObjectURL(url)
}

function createFilter(queryString: string) {
  return (keyword: Keyword) => keyword.word.toLowerCase().includes(queryString.toLowerCase())
}

function queryKeywordSearchAdd(queryString: string, cb: (results: Keyword[]) => void) {
  let results = queryString
    ? allKeywords.value.filter(createFilter(queryString))
    : allKeywords.value
  results = results.filter((keyword) => !keywords.value.some((k) => k.id == keyword.id))
  cb(results)
}

function queryKeywordSearchDelete(queryString: string, cb: (results: Keyword[]) => void) {
  const results = queryString ? keywords.value.filter(createFilter(queryString)) : keywords.value
  cb(results)
}

function handleAllKeywordleSelect(item: Keyword) {
  newKeyword.word = item.word
}

function handleKeywordSelect(item: Keyword) {
  keywordToDelete.word = item.word
}
</script>

<style scoped>
.keywords-page {
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

.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}
</style>
