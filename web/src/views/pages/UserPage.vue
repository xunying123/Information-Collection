<template>
  <div class="user-page">
    <h1 class="title">用户界面</h1>
    <h2>所属组织</h2>
    <div class="org-info">
      <div>{{ userDisplayGroup }}</div>
      <el-button
        type="danger"
        size="large"
        style="margin-left: 16px; margin-top: 8px"
        @click="quitGroup"
      >
        退出组织
      </el-button>
    </div>

    <h2>定制管理</h2>
    <div class="custom-management">
      <el-button plain type="primary" @click="openSubDrawer"> 管理订阅源 </el-button>
      <el-button plain type="primary" @click="openKeyDrawer"> 管理关键词 </el-button>
    </div>

    <!-- 管理订阅源 Drawer -->
    <el-drawer
      v-model="showSubDrawer"
      title="管理订阅源"
      direction="rtl"
      size="40%"
      @close="handleDrawerClose"
    >
      <!-- 引入管理订阅源组件 -->
      <SubscriptionsPage />
    </el-drawer>

    <!-- 管理关键词 Drawer -->
    <el-drawer
      v-model="showKeyDrawer"
      title="管理关键词"
      direction="rtl"
      size="40%"
      @close="handleDrawerClose"
    >
      <!-- 引入管理关键词组件 -->
      <KeywordsPage />
    </el-drawer>

    <!-- <router-view></router-view> -->
    <h2>侧边栏显示模式</h2>
    <div class="sidebar-mode-setting">
      <el-radio-group v-model="sidebarMode">
        <el-radio value="category" border> 按照网站分类 </el-radio>
        <el-radio value="subject" border> 按照文章分类 </el-radio>
        <el-radio value="both" border> 同时显示两种分类 </el-radio>
      </el-radio-group>
    </div>
    <div v-if="false">
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
          <i class="el-icon-upload" />
          <div class="el-upload__text">拖拽文件到此处，或<em>点击上传</em></div>
        </el-upload>
        <div class="button-group">
          <el-button type="primary" :disabled="!tempImage" @click="confirmUpload">
            确认上传
          </el-button>
          <el-button type="warning" @click="restoreDefault"> 恢复默认 </el-button>
        </div>
      </div>
    </div>

    <h2>侧边栏颜色</h2>
    <div class="sidebar-setting">
      <el-radio-group v-model="sidebarColor">
        <el-radio value="blue" border> 蓝色 </el-radio>
        <el-radio value="yellow" border> 黄色 </el-radio>
        <el-radio value="red" border> 红色 </el-radio>
        <el-radio value="green" border> 绿色 </el-radio>
        <el-radio value="orange" border> 橙色 </el-radio>
      </el-radio-group>
    </div>

    <div class="section">
      <div class="button-container">
        <el-button size="large" type="danger" @click="confirmLogout"> 退出登录 </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, computed } from 'vue'
import { ElNotification, ElMessageBox, type UploadFile } from 'element-plus'
import { bg_url_key, sidebar_color_key, sidebar_show_mode_key, user_key } from '@/key'
import { logout, leaveGroup } from '@/sdk'

// 引入原有的管理组件
import SubscriptionsPage from '@/views/pages/SubscriptionsPage.vue'
import KeywordsPage from '@/views/pages/KeywordsPage.vue'

const user = inject(user_key)!

const userDisplayGroup = computed(() => {
  return user.value?.group
    ? user.value.group.name + (user.value.group_accepted ? '' : '（待审核）')
    : '未属于任何组织'
})

// 侧边栏颜色设置
const sidebarColor = inject(sidebar_color_key)!
// 侧边栏显示模式设置
const sidebarMode = inject(sidebar_show_mode_key)!

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
const dummyRequest = ({ onSuccess }: { onSuccess: (x: string) => undefined }) => {
  setTimeout(() => {
    onSuccess('ok')
  }, 0)
}

const handleFileChange = (file: UploadFile) => {
  if (!file.raw) return
  const reader = new FileReader()
  reader.onload = () => {
    tempImage.value = reader.result as string
  }
  reader.readAsDataURL(file.raw)
}

const bgUrl = inject(bg_url_key)!
const confirmUpload = () => {
  if (tempImage.value) {
    bgUrl.value = tempImage.value
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
  bgUrl.value = undefined
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
      '当前操作会使您退出您所在的组织，如希望重新加入，需要再次联系对应组织的管理员，请确认，并谨慎操作！！！',
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

// 控制抽屉显示的变量
const showSubDrawer = ref(false)
const showKeyDrawer = ref(false)

// 打开订阅源管理抽屉
const openSubDrawer = () => {
  showSubDrawer.value = true
}

// 打开关键词管理抽屉
const openKeyDrawer = () => {
  showKeyDrawer.value = true
}

function handleDrawerClose() {
  // 触发网页的 reload
  window.location.reload()
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
  height: 0.5em;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.button-group {
  display: flex;
  gap: 16px;
  /* margin-top: 6px; */
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

/* 定制管理部分样式 */
.custom-management {
  display: flex;
  gap: 16px;
  margin: 20px 0;
  margin-left: 1em;
}

.sidebar-setting {
  margin: 20px;
}

.sidebar-mode-setting {
  margin: 20px;
}
</style>
