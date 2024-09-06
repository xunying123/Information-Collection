<script setup lang="ts">
import { user_key } from '@/key'
import { inject } from 'vue'
import { ElAvatar } from 'element-plus'
import { server } from '@/const'
import { ElMessageBox } from 'element-plus'

let user = inject(user_key)!

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

<template>
  <div v-if="user" class="horizon-grid">
    <el-avatar size="" :src="user.avatars" />
    <div>
      <h2>{{ user.name }}</h2>
      <p>{{ user.organization }}</p>
    </div>
    <el-button type="primary" @click="logout()">退出登录</el-button>
  </div>
</template>

<style lang="css" scoped>
.horizon-grid {
  display: grid;
  grid-template-columns: min-content 1fr;
  align-items: center;
  justify-items: start;
  grid-column-gap: 1em;
  padding: 0 1em;
}
</style>
