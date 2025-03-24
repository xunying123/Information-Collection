<template>
  <el-tabs v-model="activeTab" class="custom-tabs" style="--el-font-size-base: 24px">
    <!-- 增加网站 Tab -->
    <el-tab-pane label="增加网站" name="add-site" style="--el-font-size-base: initial">
      <el-form :model="newSite" ref="siteForm" label-width="120px">
        <el-form-item label="网站类别" prop="category" size="large">
          <el-autocomplete
            v-model="newSite.category"
            :fetch-suggestions="queryClassSearch"
            popper-class="my-autocomplete"
            placeholder="请输入类别"
            @select="handleSelect"
            clearable
          >
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
          <el-button
            type="primary"
            @click="addSite_"
            size="large"
            :disabled="!(newSite.category && newSite.name && newSite.url)"
            >提交</el-button
          >
          <el-button @click="resetForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>

    <!-- 删除网站 Tab -->
    <el-tab-pane label="删除网站" name="remove-site" style="--el-font-size-base: initial">
      <el-form :model="siteToDelete" label-width="120px">
        <el-form-item label="网站名称" size="large">
          <el-autocomplete
            v-model="siteToDelete.name"
            :fetch-suggestions="querySearch"
            popper-class="my-autocomplete"
            placeholder="输入要删除的网站名称"
            @select="handleSelect"
            clearable
          >
            <template #default="{ item }">
              <div class="name">{{ item.name }}</div>
              <span class="link">{{ item.url }}</span>
            </template>
          </el-autocomplete>
        </el-form-item>
        <el-form-item>
          <el-popconfirm
            width="280"
            title="确认删除该网站吗？"
            @cancel="onCancel"
            @confirm="deleteSite_"
          >
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

    <!-- 成员管理 Tab -->
    <el-tab-pane label="成员管理" name="group-management" style="--el-font-size-base: initial">
      <!-- 新增成员区域 -->
      <h3>添加成员</h3>
      <el-form :model="newMember" label-width="120px">
        <el-form-item label="用户名" size="large">
          <el-autocomplete
            v-model="newMember.searchKey"
            :fetch-suggestions="queryUserSearch"
            popper-class="my-autocomplete"
            placeholder="请输入用户名"
            @select="handleUserSelect"
            clearable
            value-key="username"
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
            @click="addMember"
            :disabled="!newMember.selectedUser"
          >
            添加成员
          </el-button>
          <el-button @click="resetMemberForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 当前组织成员列表 -->
      <h3>当前组织成员</h3>
      <el-table :data="membersList" stripe height="300" style="width: 50%; margin-top: 1em">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="is_admin" label="状态" :formatter="formatAdminStatus" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" size="small" @click="deleteMember(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import type { SiteItem } from '@/api_interface'
import { getSites, addSite, deleteSite, getPendingMembers, getGroupUsers, addUserToGroup, removeUserFromGroup, getUserinfoNotInGroup, type User } from '@/sdk'

// 当前激活的 Tab，从 localStorage 中读取或使用默认值
const activeTab = ref(localStorage.getItem('activeTab') || 'add-site')
watch(activeTab, (newVal) => {
  localStorage.setItem('activeTab', newVal)
})

// 增加网站表单模型
const newSite = reactive({
  category: '',
  name: '',
  url: ''
})

// 删除网站表单模型
const siteToDelete = reactive({
  name: ''
})

// 网站数据和类别列表
const Sites = ref<SiteItem[]>([])
const categories = ['科教要闻', '院校动态', '国际视野']

// 自动完成搜索：网站类别
const queryClassSearch = (queryString: string, cb: any) => {
  const results = categories.filter((category) => category.includes(queryString))
  cb(results)
}

// 自动完成搜索：网站名称（用于删除）
const querySearch = (queryString: string, cb: any) => {
  const results = queryString ? Sites.value.filter(createFilter(queryString)) : Sites.value
  cb(results)
}
const createFilter = (queryString: string) => {
  return (site: SiteItem) => {
    return site.name.toLowerCase().indexOf(queryString.toLowerCase()) === 0
  }
}
const handleSelect = (item: string | SiteItem) => {
  if (typeof item === 'string') {
    newSite.category = item
  } else {
    siteToDelete.name = item.name
  }
}

const clicked = ref(false)
function onCancel() {
  clicked.value = true
}

// 添加网站函数
const addSite_ = async () => {
  if (!newSite.category || !newSite.name || !newSite.url) {
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
      cate_id: categories.indexOf(newSite.category) + 1,
      icon: ''
    }
  })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '错误',
      message: '添加网站失败: ' + (error ? error : data?.message),
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: '添加网站成功',
    type: 'success'
  })
}

// 删除网站函数
const deleteSite_ = async () => {
  if (!siteToDelete.name) {
    ElNotification({
      title: '失败',
      message: '请填写网站名称!',
      type: 'error'
    })
    return
  }
  const site = Sites.value.find((s) => s.name === siteToDelete.name)
  if (!site) {
    ElNotification({
      title: '失败',
      message: '找不到网站!',
      type: 'error'
    })
    return
  }
  const { data, error } = await deleteSite({ path: { site_id: Number(site.id) } })
  if (error || data?.status !== 200) {
    ElNotification({
      title: '失败',
      message: '删除网站失败: ' + (error ? error : data?.message),
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: '网站 ' + siteToDelete.name + ' 已删除!',
    type: 'success'
  })
  siteToDelete.name = ''
  location.reload()
}

// 重置新增网站表单
const resetForm = () => {
  newSite.category = ''
  newSite.name = ''
  newSite.url = ''
}

// 加载所有网站数据
const loadAll = async (): Promise<SiteItem[]> => {
  const { data, error } = await getSites()
  if (error) {
    console.error(error)
    return []
  }
  return data
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
    ? allGroupPendingUsers.value.filter(user =>
        user.username.toLowerCase().includes(queryString.toLowerCase())
      )
    : allGroupPendingUsers.value

  if (queryString) {
    console.log('query:', queryString)
    const { data, error } = await getUserinfoNotInGroup({ query: { username: queryString } })
    if (!error && data) {
      const exists = results.some(user => user.username === data.username)
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

// 重置表单
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
  Sites.value = await loadAll()
  await loadMembersList()
  await loadGroupPendingList()
})

const loadMembersList = async () => {
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
</style>
