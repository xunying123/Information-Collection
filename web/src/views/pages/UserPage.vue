<template>
  <div class="user-page">
    <h1 class="title">用户界面</h1>
    <h2>所属组织</h2>
    <div class="org-info">
      <div>{{ userDisplayGroup }}</div>
      <el-button type="danger" size="mini" @click="quitGroup" style="margin-left: 16px; margin-top: 8px">
        退出组织
      </el-button>
    </div>

    <router-view></router-view>
    <h2>背景设置</h2>
    <div class="bg-setting">
      <el-upload
        class="upload-demo"
        drag
        action=""
        :auto-upload="false"
        accept="image/*"
        :file-list="fileList"
        :http-request="dummyRequest"
        :on-change="handleFileChange"
        list-type="picture"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">拖拽文件到此处，或<em>点击上传</em></div>
      </el-upload>
      <div class="button-group">
        <el-button type="primary" @click="confirmUpload" :disabled="!tempImage">
          确认上传
        </el-button>
        <el-button type="warning" @click="restoreDefault">
          恢复默认
        </el-button>
      </div>
    </div>

    <!-- 新增侧边栏颜色设置项 -->
    <h2>侧边栏颜色</h2>
    <div class="sidebar-setting">
      <el-radio-group v-model="sidebarColor" @change="changeSidebarColor">
        <el-radio label="blue" border>蓝色</el-radio>
        <el-radio label="yellow" border>黄色</el-radio>
        <el-radio label="red" border>红色</el-radio>
        <el-radio label="green" border>绿色</el-radio>
        <el-radio label="orange" border>橙色</el-radio>
      </el-radio-group>
    </div>

    <div class="section">
      <div class="button-container">
        <el-button size="large" type="danger" @click="confirmLogout">退出登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, computed } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import { user_key } from '@/key'
import { logout, leaveGroup } from '@/sdk'

const user = inject(user_key)!

const userDisplayGroup = computed(() => {
  return user.value?.group
    ? user.value.group.name + (user.value.group_accepted ? '' : '（待审核）')
    : '未属于任何组织'
})

// 侧边栏颜色设置：从 localStorage 获取当前值，默认为 "blue"
const sidebarColor = ref(localStorage.getItem('sidebarColor') || 'blue')
const changeSidebarColor = (val: string) => {
  localStorage.setItem('sidebarColor', val)
  // 触发全局事件，让侧边栏组件更新颜色
  window.dispatchEvent(new Event('sidebarColorChanged'))
  ElNotification({
    title: '成功',
    message:
      '侧边栏颜色已切换为 ' +
      (val === 'blue'
        ? '蓝色'
        : val === 'yellow'
        ? '黄色'
        : val === 'red'
        ? '红色'
        : val === 'green'
        ? '绿色'
        : '橙色'),
    type: 'success'
  })
}

const confirmLogout = async () => {
  try {
    await ElMessageBox.confirm('确定退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await logout_()
  } catch (error) {
    console.log('退出登录操作已取消', error)
  }
}

const logout_ = async () => {
  if (!user) return
  const { data, error } = await logout()
  if (error || data?.status !== 200) {
    ElNotification({
      title: '错误',
      message: `退出登录失败: ${error ? error : data?.message}`,
      type: 'error'
    })
    return
  }
  ElNotification({
    title: '成功',
    message: '退出登录成功',
    type: 'success',
    duration: 2000,
    onClose: () => {
      user.value = null
      location.reload()
    }
  })
}

const fileList = ref([])
const tempImage = ref<string | null>(null)
const dummyRequest = ({ onSuccess }: { onSuccess: Function }) => {
  setTimeout(() => {
    onSuccess('ok')
  }, 0)
}

const handleFileChange = (file: any) => {
  if (!file.raw) return
  const reader = new FileReader()
  reader.onload = () => {
    tempImage.value = reader.result as string
  }
  reader.readAsDataURL(file.raw)
}

const confirmUpload = () => {
  if (tempImage.value) {
    localStorage.setItem('bgUrl', tempImage.value)
    window.dispatchEvent(new Event('bgUrlChanged'))
    fileList.value = []
    tempImage.value = null
    ElNotification({
      title: '成功',
      message: '背景图片已保存',
      type: 'success'
    })
  }
}

const restoreDefault = () => {
  localStorage.removeItem('bgUrl')
  window.dispatchEvent(new Event('bgUrlChanged'))
  ElNotification({
    title: '成功',
    message: '背景已恢复为默认',
    type: 'success'
  })
  location.reload()
}

const quitGroup = async () => {
  try {
    await ElMessageBox.confirm(
      '当前操作会使您退出您所在的组织，如希望重新加入，需要再次联系对应组织的管理员，请确认。',
      '提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await ElMessageBox.confirm('确认退出吗？', '再次确认', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const { data, error } = await leaveGroup()
    if (error || data?.status !== 200) {
      ElNotification({
        title: '错误',
        message: `退出组织失败: ${error ? error : data?.message}`,
        type: 'error'
      })
      return
    }
    ElNotification({
      title: '成功',
      message: '已退出组织',
      type: 'success'
    })
  } catch (error) {
    console.log('退出组织操作已取消', error)
  }
}
</script>

<style scoped>
.user-page {
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  max-width: 800px;
  margin: 40px auto;
}

.title {
  text-align: left;
  margin-bottom: 16px;
}

.org-info {
  text-align: center;
  margin-bottom: 24px;
  font-size: 16px;
  color: #333;
}

.section {
  margin-bottom: 24px;
  height: 1em;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.button-group {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.bg-setting {
  margin: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-demo {
  width: 300px;
}

/* 侧边栏颜色设置区域 */
.sidebar-setting {
  margin: 20px;
}
</style>
