<template>
    <div class="user-page">
      <h1>用户订阅</h1>
      <div class="section">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="添加网站源" name="add-source">
            <el-form :model="newSource" ref="sourceForm" label-width="120px">
              <el-form-item label="网站类别" prop="category" size="large">
                <el-input v-model="newSource.category" placeholder="请输入网站类别"></el-input>
              </el-form-item>
              <el-form-item label="网站名称" prop="name" size="large">
                <el-input v-model="newSource.name" placeholder="请输入网站名称"></el-input>
              </el-form-item>
              <el-form-item label="网站链接" prop="link" size="large">
                <el-input v-model="newSource.link" placeholder="请输入网站链接"></el-input>
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
        <el-divider></el-divider>
        <h2>网站源列表</h2>
        <el-scrollbar class="source-scrollbar" height="150px">
          <p v-for="source in sources" :key="source.id" class="scrollbar-item">
            <strong>{{ source.category }}</strong> - {{ source.name }} - <a :href="source.link" target="_blank">{{ source.link }}</a>            
        </p>
        </el-scrollbar>
      </div>
  
      <div class="section">
        <el-tabs v-model="activeKeywordTab">
          <el-tab-pane label="添加关键词" name="add-keyword">
            <el-form :model="newKeyword" ref="keywordForm" label-width="120px">
              <el-form-item label="关键词" prop="name" size="large">
                <el-input v-model="newKeyword.name" placeholder="请输入关键词"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="addKeyword" size="large">添加</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="删除关键词" name="remove-keyword">
            <el-form :model="keywordToDelete" label-width="120px">
              <el-form-item label="关键词" size="large">
                <el-autocomplete
                  v-model="keywordToDelete.name"
                  :fetch-suggestions="queryKeywordSearch"
                  placeholder="输入要删除的关键词"
                  @select="handleKeywordSelect"
                  clearable
                >
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
        <h2>关键词列表</h2>
        <!-- <el-scrollbar height="150px">
          <p v-for="keyword in keywords" :key="keyword.id" class="scrollbar-item">{{ keyword.name }}</p>
        </el-scrollbar> -->
        <!-- <el-tag v-for="keyword in keywords" :key="keyword.id" closable @close="deleteKeyword">{{ keyword.name }}</el-tag> -->
        <div class="keyword-tags">
          <el-tag
            v-for="keyword in keywords"
            :key="keyword.id"
            round
            :type="getRandomTagType()"
            size="large"
          >
            {{ keyword.name }}
          </el-tag>
        </div>
      </div>
  
      <div class="section">
        <el-popconfirm
            title="确定退出登录吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-question"
            @confirm="logout"
            >
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
  import { ref, reactive, inject } from 'vue'
  import { ElMessageBox, ElPopconfirm } from 'element-plus'
  import { user_key } from '@/key'
  import { server, jaccount_client_id } from '@/const'

  const user = inject(user_key)!
  
  const activeTab = ref('add-source')
  const activeKeywordTab = ref('add-keyword')
  
  const newSource = reactive({ category: '', name: '', link: '' })
  const sourceToDelete = reactive({ name: '' })
  const newKeyword = reactive({ name: '' })
  const keywordToDelete = reactive({ name: '' })
  
  const sources = ref([
    { id: 1, category: '新闻', name: '新闻网站1', link: 'https://news1.com' },
    { id: 2, category: '博客', name: '博客网站1', link: 'https://blog1.com' },
    { id: 3, category: '论坛', name: '论坛网站1', link: 'https://forum1.com' },
    { id: 4, category: '新闻', name: '新闻网站2', link: 'https://news2.com' },
    { id: 5, category: '博客', name: '博客网站2', link: 'https://blog2.com' },
    { id: 6, category: '论坛', name: '论坛网站2', link: 'https://forum2.com' },
    { id: 7, category: '新闻', name: '新闻网站3', link: 'https://news3.com' },
    { id: 8, category: '博客', name: '博客网站3', link: 'https://blog3.com' },
    { id: 9, category: '论坛', name: '论坛网站3', link: 'https://forum3.com' },
    { id: 10, category: '新闻', name: '新闻网站4', link: 'https://news4.com' },
    { id: 11, category: '博客', name: '博客网站4', link: 'https://blog4.com' },
    { id: 12, category: '论坛', name: '论坛网站4', link: 'https://forum4.com' },
    { id: 13, category: '新闻', name: '新闻网站5', link: 'https://news5.com' },
    { id: 14, category: '博客', name: '博客网站5', link: 'https://blog5.com' },
    { id: 15, category: '论坛', name: '论坛网站5', link: 'https://forum5.com' },
    { id: 16, category: '新闻', name: '新闻网站6', link: 'https://news6.com' },
    { id: 17, category: '博客', name: '博客网站6', link: 'https://blog6.com' }
  ])
  
  const keywords = ref([
    { id: 1, name: '科技' },
    { id: 2, name: '教育' },
    { id: 3, name: '健康' },
    { id: 4, name: '娱乐' },
    { id: 5, name: '体育' },
    { id: 6, name: '财经' },
    { id: 7, name: '军事' },
    { id: 8, name: '文化' },
    { id: 9, name: '汽车' },
    { id: 10, name: '旅游' },
    { id: 11, name: '房产' }
  ])

  const tagTypes = ['primary', 'success', 'info', 'warning', 'danger']

  function getRandomTagType() {
    const randomIndex = Math.floor(Math.random() * tagTypes.length)
    return tagTypes[randomIndex]
  }

  // Add and delete source functions
  function addSource() {
    if (newSource.name.trim() && newSource.link.trim()) {
      sources.value.push({ id: Date.now(), ...newSource })
      newSource.category = ''
      newSource.name = ''
      newSource.link = ''
    }
  }
  
  function deleteSource() {
    const source = sources.value.find(s => s.name === sourceToDelete.name)
    if (source) {
      sources.value = sources.value.filter(s => s.id !== source.id)
      sourceToDelete.name = ''
    }
  }
  
  function querySourceSearch(queryString: string, cb) {
    const results = queryString ? sources.value.filter(createFilter(queryString)) : sources.value
    cb(results)
  }
  
  function createFilter(queryString: string) {
    return (source) => source.name.toLowerCase().includes(queryString.toLowerCase())
  }
  
  // Add and delete keyword functions
  function addKeyword() {
    if (newKeyword.name.trim()) {
      keywords.value.push({ id: Date.now(), name: newKeyword.name.trim() })
      newKeyword.name = ''
    }
  }
  
  function deleteKeyword() {
    const keyword = keywords.value.find(k => k.name === keywordToDelete.name)
    if (keyword) {
      keywords.value = keywords.value.filter(k => k.id !== keyword.id)
      keywordToDelete.name = ''
    }
  }
  
  function queryKeywordSearch(queryString: string, cb) {
    const results = queryString ? keywords.value.filter(createFilter(queryString)) : keywords.value
    cb(results)
  }
  
  function handleSourceSelect(item) {
    sourceToDelete.name = item.name
  }
  
  function handleKeywordSelect(item) {
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
          ElMessageBox.alert('退出登录成功', '提示', {
            confirmButtonText: '确定',
            type: 'success',
            callback: () => {
              user.value = null
              location.reload()
              window.location.href = `http://jaccount.sjtu.edu.cn/oauth2/logout?client_id=${jaccount_client_id}&post_logout_redirect_uri=${encodeURIComponent(window.location.href)}`
            }
          })
        else throw new Error(d.msg)
      })
      .catch((e) => {
        ElMessageBox.alert('退出登录失败: ' + e, '错误', {
          confirmButtonText: '确定',
          type: 'error'
        })
      })
  }
  </script>
  
  <style scoped>
  .user-page {
    padding: 16px;
    background: rgba(255, 255, 255, 0.8); /* 半透明背景 */
    border-radius: 8px; /* 圆角 */
    max-width: 800px; /* 最大宽度 */
    margin: 40px auto; /* 垂直居中，顶部有间距 */
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