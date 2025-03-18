<template>
  <div class="user-page">
    <h1 class="title">用户界面</h1>
    <h2>所属组织</h2>
    <div class="org-info">{{ user!.organization }}</div>
    <router-view></router-view>
    <div class="section">
      <ElPopconfirm
        title="确定退出登录吗？"
        confirm-button-text="确定"
        cancel-button-text="取消"
        icon="el-icon-question"
        @confirm="logout_"
      >
        <template #reference>
          <div class="button-container">
            <el-button size="large" type="danger">退出登录</el-button>
          </div>
        </template>
      </ElPopconfirm>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { ElPopconfirm, ElNotification } from 'element-plus'
import { user_key } from '@/key'
import { logout } from '@/sdk/sdk.gen'
const user = inject(user_key)!

const logout_ = async () => {
  if (!user)
    // impossible path ?
    return
  const { data, error } = await logout()
  if (error) {
    ElNotification({
      title: '错误',
      message: '退出登录失败: ' + error,
      type: 'error'
    })
    return
  }
  if (data!.status != 200) {
    ElNotification({
      title: '错误',
      message: '退出登录失败: ' + data!.message,
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
</script>

<style scoped>
.user-page {
  padding: 16px;
  background: rgba(255, 255, 255, 0.8); /* 半透明背景 */
  border-radius: 8px; /* 圆角 */
  max-width: 800px; /* 最大宽度 */
  margin: 40px auto; /* 垂直居中，顶部有间距 */
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
</style>
