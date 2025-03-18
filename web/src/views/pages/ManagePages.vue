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
            v-model="newMember.username"
            :fetch-suggestions="queryUserSearch"
            popper-class="my-autocomplete"
            placeholder="请输入用户名（完全匹配后才显示提示）"
            @select="handleUserSelect"
            clearable
          >
            <template #default="{ item }">
              <div class="name">{{ item }}</div>
            </template>
          </el-autocomplete>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" @click="addMember" :disabled="!isUserValid">
            添加成员
          </el-button>
          <el-button @click="resetMemberForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 当前组织成员列表 -->
      <h3>当前组织成员</h3>
      <el-table :data="membersList" stripe height="300" style="width: 50%; margin-top: 1em">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="joinTime" label="加入时间" />
        <el-table-column prop="status" label="状态" />
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
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import { server } from '@/const'
import type { SiteItem } from '@/api_interface'
import { getSites, addSite, deleteSite } from '@/sdk'

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
const membersList = ref<Array<{ username: string; joinTime: string; status: string }>>([])

// 新增成员表单模型
const newMember = reactive({
  username: ''
})

// 示例用户列表（后续可替换为接口请求数据）
const allUsers = ref<string[]>(['用户A', '用户B', '用户C', '用户D', '用户E', '用户F'])

// 自动补全搜索：添加成员
// 仅当输入内容与某个用户名完全匹配时返回该结果
const queryUserSearch = (queryString: string, cb: any) => {
  const results = allUsers.value.filter((user) => user.toLowerCase() === queryString.toLowerCase())
  cb(results)
}

// 当选择自动补全结果时，确保输入框显示完整的用户名
const handleUserSelect = (item: string) => {
  newMember.username = item
}

// computed 判断输入的用户名是否存在于 allUsers 列表中
const isUserValid = computed(() => {
  return allUsers.value.includes(newMember.username)
})

// 添加成员函数（示例：后续可替换为调用后端接口）
const addMember = async () => {
  if (!isUserValid.value) {
    ElNotification({
      title: '添加失败',
      message: '输入的用户名不存在，请检查后重试',
      type: 'error'
    })
    return
  }
  const now = new Date().toLocaleString()
  membersList.value.push({
    username: newMember.username,
    joinTime: now,
    status: '普通用户'
  })
  ElNotification({
    title: '添加成功',
    message: `成员 ${newMember.username} 已添加`,
    type: 'success'
  })
  resetMemberForm()
}

// 重置新增成员表单
const resetMemberForm = () => {
  newMember.username = ''
}

// 删除组织成员函数
const deleteMember = async (member: { username: string; joinTime: string; status: string }) => {
  ElMessageBox.confirm(`确认删除成员 ${member.username} 吗？此操作不可恢复。`, '删除确认', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      const response = await fetch(`${server}/group/delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: member.username })
      })
      if (response.ok) {
        ElNotification({
          title: '删除成功',
          message: `成员 ${member.username} 删除成功！`,
          type: 'success'
        })
        membersList.value = membersList.value.filter((item) => item.username !== member.username)
      } else {
        ElNotification({
          title: '删除失败',
          message: '删除失败，服务器错误！',
          type: 'error'
        })
      }
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
})

// 模拟加载当前组织成员数据（实际请替换为接口请求）
const loadMembersList = async () => {
  membersList.value = [
    { username: '管理员1', joinTime: '2025-01-10 09:00', status: '管理员' },
    { username: '用户C', joinTime: '2025-02-20 15:45', status: '普通用户' },
    { username: '用户F', joinTime: '2025-03-01 14:20', status: '普通用户' },
    { username: '管理员2', joinTime: '2025-03-05 10:30', status: '管理员' }
  ]
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
