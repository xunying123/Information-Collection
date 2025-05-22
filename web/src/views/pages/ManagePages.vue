<template>
  <el-tabs v-model="activeTab" class="custom-tabs" style="--el-font-size-base: 24px">
    <!-- 增加网站 Tab -->
    <el-tab-pane label="增加网站" name="add-site" style="--el-font-size-base: initial">
      <!-- 部分1：添加网站 -->
      <div class="feature-card">
        <h3>添加网站</h3>
        <el-form ref="siteForm" :model="newSite" label-width="120px">
          <el-form-item label="网站名称" prop="name" size="large">
            <el-input v-model="newSite.name" placeholder="请输入网站名称" />
          </el-form-item>
          <el-form-item label="网站链接" prop="url" size="large">
            <el-input v-model="newSite.url" placeholder="请输入链接" />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :disabled="!(newSite.name && newSite.url)"
              @click="addSite_"
            >
              提交
            </el-button>
            <el-button size="large" @click="resetForm"> 重置 </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 部分2：将网站加入分类 -->
      <div class="feature-card">
        <h3>将网站加入分类</h3>
        <el-form ref="mappingForm" :model="siteCategoryMapping" label-width="120px">
          <el-form-item label="选择分类" prop="category" size="large">
            <el-autocomplete
              v-model="siteCategoryMapping.category"
              :fetch-suggestions="queryClassSearch"
              popper-class="my-autocomplete"
              placeholder="请选择分类"
              value-key="name"
              clearable
              @select="handleCateSiteSelect"
            >
              <template #default="{ item }">
                <div class="name">
                  {{ item.name }}
                </div>
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item label="选择网站" prop="site" size="large">
            <el-autocomplete
              v-model="siteCategoryMapping.site"
              :fetch-suggestions="querySearch"
              popper-class="my-autocomplete"
              placeholder="请选择网站"
              value-key="name"
              clearable
              @select="handleCateSiteSelect"
            >
              <template #default="{ item }">
                <div class="name">
                  {{ item.name }}
                </div>
                <span class="link">{{ item.url }}</span>
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :disabled="siteCategoryMapping.cate_id == -1 || siteCategoryMapping.site_id == -1"
              @click="assignSiteToCategory"
            >
              提交
            </el-button>
            <el-button size="large" @click="resetMappingForm"> 重置 </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-tab-pane>

    <!-- 删除网站 Tab -->
    <el-tab-pane label="删除网站" name="remove-site" style="--el-font-size-base: initial">
      <div class="feature-card">
        <h3>删除网站</h3>
        <el-form :model="siteToDelete" label-width="120px">
          <el-form-item label="选择分类" prop="category" size="large">
            <el-autocomplete
              v-model="deleteCate.name"
              :fetch-suggestions="queryClassSearch"
              popper-class="my-autocomplete"
              placeholder="请选择分类"
              value-key="name"
              clearable
              @select="handleDeleteCateSiteSelect"
            >
              <template #default="{ item }">
                <div class="name">
                  {{ item.name }}
                </div>
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item label="选择网站" prop="site" size="large">
            <el-autocomplete
              v-model="siteToDelete.name"
              :fetch-suggestions="querySiteForDeletion"
              popper-class="my-autocomplete"
              placeholder="请选择网站"
              value-key="name"
              clearable
              @select="handleDeleteCateSiteSelect"
            >
              <template #default="{ item }">
                <div class="name">
                  {{ item.name }}
                </div>
                <span class="link">{{ item.url }}</span>
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item>
            <el-button
              type="danger"
              size="large"
              :disabled="!(deleteCate && siteToDelete)"
              @click="deleteSite_"
            >
              删除
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-tab-pane>

    <!-- 成员管理 Tab -->
    <el-tab-pane label="成员管理" name="group-management" style="--el-font-size-base: initial">
      <!-- 新增成员区域 -->
      <div class="feature-card">
        <h3>添加成员</h3>
        <el-form :model="newMember" label-width="120px">
          <el-form-item label="用户名" size="large">
            <el-autocomplete
              v-model="newMember.searchKey"
              :fetch-suggestions="queryUserSearch"
              popper-class="my-autocomplete"
              placeholder="请输入用户名"
              clearable
              value-key="username"
              @select="handleUserSelect"
            >
              <template #default="{ item }">
                <span class="name">{{ item.username }}</span>
                <span style="margin-left: 10px; color: #666">{{ item.name }}</span>
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :disabled="!newMember.selectedUser"
              @click="addMember"
            >
              添加成员
            </el-button>
            <el-button size="large" @click="resetMemberForm"> 重置 </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 当前组织成员列表 -->
      <div class="feature-card">
        <h3>当前组织成员</h3>
        <el-table :data="membersList" stripe height="300" style="width: 100%; margin-top: 1em">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="is_admin" label="状态" :formatter="formatAdminStatus" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="danger" size="small" @click="deleteMember(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, watch, inject } from 'vue'
import { user_key } from '@/key'
import { ElNotification, ElMessageBox } from 'element-plus'
import type { SiteItem } from '@/sdk'
import {
  getCategories,
  getSites,
  addSite,
  addSiteToCategory,
  removeSiteFromCategory,
  getPendingMembers,
  getGroupUsers,
  addUserToGroup,
  removeUserFromGroup,
  getUserinfoNotInGroup,
  type User,
  type CategoryItem,
  type Category
} from '@/sdk'

const user = inject(user_key)!

// 当前激活的 Tab，从 localStorage 中读取或使用默认值
const activeTab = ref(localStorage.getItem('activeTab') || 'add-site')
watch(activeTab, (newVal) => {
  localStorage.setItem('activeTab', newVal)
})

// ---------------------- 新增网站相关 ----------------------

const newSite = reactive({
  name: '',
  url: ''
})

// 将网站加入分类的表单模型
const siteCategoryMapping = reactive({
  category: '',
  site: '',
  cate_id: -1,
  site_id: -1
})

// 网站数据和类别列表
const Sites = ref<SiteItem[]>([])
const categories = ref<CategoryItem[]>([])

// 自动完成搜索：网站类别（用于"加入分类"部分）
const queryClassSearch = (queryString: string, cb: any) => {
  // console.log('query:', queryString)
  // console.log('categories:', categories.value)
  const results = categories.value.filter((category) => category.name.includes(queryString))
  cb(results)
}

// 自动完成搜索：网站（用于"加入分类"部分）
const querySearch = (queryString: string, cb: any) => {
  const results = queryString ? Sites.value.filter(createFilter(queryString)) : Sites.value
  cb(results)
}
const createFilter = (queryString: string) => {
  return (site: SiteItem) => {
    return site.name.toLowerCase().indexOf(queryString.toLowerCase()) === 0
  }
}

const handleCateSiteSelect = (item: CategoryItem | SiteItem) => {
  // console.log('selected:', typeof item, item)
  if (typeof item === 'object' && 'url' in item) {
    siteCategoryMapping.site_id = item.id!
    siteCategoryMapping.site = item.name
  } else if (typeof item === 'object') {
    siteCategoryMapping.cate_id = item.id!
    siteCategoryMapping.category = item.name
  }
}

// 添加网站函数（只提交网站名称和链接）
const addSite_ = async () => {
  if (!newSite.name || !newSite.url) {
    ElNotification({
      title: '添加失败',
      message: '请填写完整信息!',
      type: 'error'
    })
    return
  }

  const { data, error } = await addSite({
    body: {
      name: newSite.name,
      url: newSite.url,
      icon: ''
    }
  })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '错误',
      message: '添加网站失败: ' + (error ? error.detail : data?.message),
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: '添加网站成功',
    type: 'success'
  })
  resetForm()
}

const assignSiteToCategory = async () => {
  if (siteCategoryMapping.cate_id == -1 || siteCategoryMapping.site_id == -1) {
    ElNotification({
      title: '失败',
      message: '请选择分类和网站',
      type: 'error'
    })
    return
  }
  const category = categories.value.find((c) => c.id === siteCategoryMapping.cate_id)
  if (!category) {
    ElNotification({
      title: '失败',
      message: '找不到分类!',
      type: 'error'
    })
    return
  }
  const site = Sites.value.find((s) => s.id === siteCategoryMapping.site_id)
  if (!site) {
    ElNotification({
      title: '失败',
      message: '找不到网站!',
      type: 'error'
    })
    return
  }
  const { data, error } = await addSiteToCategory({
    body: {
      cate_id: category.id!,
      site_id: site.id!
    }
  })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '失败',
      message: '加入分类失败: ' + (error ? error.detail : data?.message),
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: `网站 ${site.name} 已加入分类 ${category.name}`,
    type: 'success'
  })
  resetMappingForm()
  setTimeout(() => {
    location.reload()
  }, 900)
}

// 重置添加网站表单
const resetForm = () => {
  newSite.name = ''
  newSite.url = ''
}

// 重置加入分类表单
const resetMappingForm = () => {
  siteCategoryMapping.cate_id = -1
  siteCategoryMapping.site_id = -1
  siteCategoryMapping.category = ''
  siteCategoryMapping.site = ''
}

// 修改后的删除网站表单模型：包含分类和网站两个字段
const siteToDelete = ref<SiteItem>({ id: 0, name: '', url: '' })
const deleteCate = ref<Category>({ id: 0, name: '', sites: [] })

const handleDeleteCateSiteSelect = (item: Category | SiteItem) => {
  if (typeof item === 'object' && 'url' in item) {
    siteToDelete.value = item
  } else if (typeof item === 'object') {
    deleteCate.value = { ...item }
  }
}

// 自动完成搜索：网站（用于删除网站部分），基于当前选择的分类
const querySiteForDeletion = (queryString: string, cb: any) => {
  let sites = deleteCate.value?.sites || []
  if (queryString) {
    sites = sites.filter((site) => site.name.toLowerCase().includes(queryString.toLowerCase()))
  }
  cb(sites)
}

const deleteSite_ = async () => {
  if (!siteToDelete.value || !deleteCate.value) {
    ElNotification({
      title: '失败',
      message: '请选择分类和网站!',
      type: 'error'
    })
    return
  }
  await ElMessageBox.confirm(
    `确认删除网站 "${siteToDelete.value.name}" 吗？此操作不可恢复。`,
    '删除确认',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
  const { data, error } = await removeSiteFromCategory({
    body: {
      cate_id: deleteCate.value.id!,
      site_id: siteToDelete.value.id!
    }
  })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '失败',
      message: '删除网站失败: ' + (error ? error.detail : data?.message),
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: '网站 ' + siteToDelete.value.name + ' 已删除!',
    type: 'success'
  })
  // 重置删除表单
  siteToDelete.value = { id: 0, name: '', url: '' }
  deleteCate.value = { id: 0, name: '', sites: [] }
  // 刷新网站列表
  setTimeout(() => {
    location.reload()
  }, 1500)
}

// ----------------- 组织管理相关代码 -----------------

// 当前组织成员列表
const membersList = ref<User[]>([])

const formatAdminStatus = (row: any, column: any, cellValue: any) => {
  return (cellValue ? '管理员' : '普通用户') + (row.group_accepted ? '' : '（待审核）')
}

// 新增成员表单模型
const newMember = reactive({
  searchKey: '', // 搜索关键词
  selectedUser: null as User | null // 实际选中的用户
})

// 待审核用户列表
const allGroupPendingUsers = ref<User[]>([])

// 加载待审核成员列表
const loadGroupPendingList = async () => {
  if (!user.value?.group) {
    return
  }
  const { data, error } = await getPendingMembers()
  if (error) {
    console.error('加载待审核成员失败:', error)
    return
  }
  allGroupPendingUsers.value = data
}

// 自动补全搜索：支持待审核列表及调用 getUserinfoNotInGroup 查询
const queryUserSearch = async (queryString: string, cb: any) => {
  let results = queryString
    ? allGroupPendingUsers.value.filter((user) =>
        user.username.toLowerCase().includes(queryString.toLowerCase())
      )
    : allGroupPendingUsers.value

  if (queryString) {
    console.log('query:', queryString)
    const { data, error } = await getUserinfoNotInGroup({ query: { username: queryString } })
    if (!error && data) {
      const exists = results.some((user) => user.username === data.username)
      console.log('exists:', exists)
      if (!exists) {
        results.push(data)
      }
    }
  }
  cb(results)
}

// 处理用户选择
const handleUserSelect = (item: User) => {
  console.log('selected:', item)
  newMember.selectedUser = item
}

// 添加成员函数
const addMember = async () => {
  if (!newMember.selectedUser) {
    ElNotification({
      title: '添加失败',
      message: '请先选择有效的用户',
      type: 'error'
    })
    return
  }

  const { data, error } = await addUserToGroup({
    body: {
      user_id: newMember.selectedUser.id
    }
  })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '添加失败',
      message: `添加失败: ${error ? error.detail : data?.message}`,
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '添加成功',
    message: `成员 ${newMember.selectedUser.username} 已添加`,
    type: 'success'
  })

  // 刷新成员列表和待审核列表
  await loadMembersList()
  await loadGroupPendingList()
  resetMemberForm()
}

// 重置成员表单
const resetMemberForm = () => {
  newMember.searchKey = ''
  newMember.selectedUser = null
}

// 删除组织成员函数
const deleteMember = async (member: User) => {
  ElMessageBox.confirm(`确认删除成员 ${member.username} 吗？此操作不可恢复。`, '删除确认', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      console.log('删除成员:', member)
      const { data, error } = await removeUserFromGroup({
        body: {
          user_id: member.id
        }
      })
      if (error || data?.status !== 200) {
        ElNotification({
          title: '删除失败',
          message: `删除失败: ${error ? error.detail : data?.message}`,
          type: 'error'
        })
        return
      }
      ElNotification({
        title: '删除成功',
        message: `成员 ${member.username} 已删除`,
        type: 'success'
      })
      await loadMembersList()
    })
    .catch(() => {
      ElNotification({
        title: '操作取消',
        message: '删除操作已取消',
        type: 'info'
      })
    })
}

// 页面加载时，初始化数据
onMounted(async () => {
  await loadAll()
  await loadMembersList()
  await loadGroupPendingList()
})

const loadAll = async () => {
  if (!user.value?.group) {
    return
  }
  const { data, error } = await getCategories()
  if (error) {
    console.error(error)
    return
  }
  categories.value = []
  for (let cate of data!) {
    categories.value.push(cate)
  }
  const { data: sitesData, error: sitesError } = await getSites()
  if (sitesError) {
    console.error(sitesError)
    return
  }
  Sites.value = sitesData!
  return
}

const loadMembersList = async () => {
  if (!user.value?.group) {
    return
  }
  const { data, error } = await getGroupUsers()
  if (error) {
    console.error('加载成员列表失败:', error)
    return
  }
  membersList.value = data
}
</script>

<style scoped>
.el-tabs {
  margin: 20px;
}

.custom-tabs {
  font-size: 16px;
  font-weight: bold !important;
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

.el-table {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

/* 新增功能卡片样式 */
.feature-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  width: 48%;
}

.feature-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
</style>
