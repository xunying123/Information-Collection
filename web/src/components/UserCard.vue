<script setup lang="ts">
import { user_key } from '@/key'
import { inject, ref, unref } from 'vue'
import { ElAvatar } from 'element-plus'
import { server } from '@/const'
import { ElMessageBox } from 'element-plus'
import { ClickOutside as vClickOutside } from 'element-plus'
import { jaccount_client_id } from '@/const'

let user = inject(user_key)!
let buttonRef = ref(null)
let popoverRef = ref(null)

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

const onClickOutside = () => {
  unref(popoverRef).popperRef?.delayHide?.()
}
</script>

<!-- <template>
  <div v-if="user" class="horizon-grid">
    <el-avatar size="" :src="user.avatars" />
    <div>
      <h2>{{ user.name }}</h2>
      <p>{{ user.organization }}</p>
    </div>
    <el-button type="primary" @click="logout()">退出登录</el-button>
  </div>
</template> -->

<template>
  <div v-if="user" class="horizon-grid">
    <div ref="buttonRef" class="user-card" v-click-outside="onClickOutside">
      <el-avatar size="" :src="user.avatars" />
      <div class="user-info">
        <h2>{{ user.name }}</h2>
        <p>{{ user.organization }}</p>
      </div>
    </div>
    <el-popover ref="popoverRef" :virtual-ref="buttonRef" trigger="click" virtual-triggering>
      <el-button size="large" @click="logout">退出登录</el-button>
    </el-popover>
  </div>
</template>

<style lang="css" scoped>
.horizon-grid {
  /* display: grid; */
  grid-template-columns: min-content 1fr;
  align-items: center;
  justify-items: start;
  grid-column-gap: 1em;
  padding: 0 1em;
}

.user-card {
  /* width: 20em; */
  width: 100%;
  display: flex;
  align-items: center;
  cursor: pointer;

}

.avatar {
  display: flex;
  margin-left: 1em;
}


.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 2em;
}
</style>
