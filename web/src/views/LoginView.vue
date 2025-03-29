<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElNotification } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { jaccount_client_id, jaccount_oauth, server } from '@/const'
import { login } from '@/sdk'
import router from '@/router'

const route = useRoute()

// 跳转地址计算
const next = computed(() => {
  return typeof route.query.next === 'string' ? route.query.next : '/'
})

const auth_redirect_url = computed(() => {
  const url = new URL(jaccount_oauth)
  url.searchParams.append('client_id', jaccount_client_id)
  url.searchParams.append('response_type', 'code')
  url.searchParams.append('redirect_uri', `${server}/auth`)
  url.searchParams.append('state', `${location.origin}${next.value}`)
  return url.toString()
})

const redirectToAuth = () => {
  window.location.href = auth_redirect_url.value
}

const loginForm = reactive({
  username: '',
  password: ''
})

console.log(next.value)

// 表单引用
const loginFormRef = ref<FormInstance | null>(null)

// 校验规则，可以根据需求添加更多规则，例如长度限制
const rules = reactive<FormRules<typeof loginForm>>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    // 示例：用户名长度在3到10个字符之间
    { min: 2, max: 50, message: '用户名长度应为2到50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    // 示例：密码长度不少于6位
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ]
})

// 使用凭证登录
const loginWithCredentials = async () => {
  if (loginFormRef.value) {
    loginFormRef.value.validate(async (valid: boolean) => {
      if (valid) {
        const { error } = await login({
          body: {
            username: loginForm.username,
            password: loginForm.password
          }
        })
        if (error) {
          ElNotification({
            title: '登录失败',
            message: String(error.detail),
            type: 'error'
          })
          return
        }
        ElNotification({
          title: '登录成功',
          message: '欢迎回来！',
          type: 'success'
        })
        localStorage.setItem('username', loginForm.username)
        router.push(next.value)
      } else {
        console.log('表单校验失败')
      }
    })
  }
}
</script>

<template>
  <div class="login-page">
    <div class="card-wrapper">
      <el-card class="login-card">
        <el-form
          :model="loginForm"
          :rules="rules"
          ref="loginFormRef"
          @submit.prevent="loginWithCredentials"
          label-position="top"
        >
          <h2 style="text-align: center; margin-bottom: 20px">登录</h2>
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password" style="margin-top: 0.5em">
            <el-input v-model="loginForm.password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" style="width: 100%; margin-top: 0.5em">
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <router-link :to="{ path: '/register', query: { next: next } }">
          <el-button type="default" style="width: 100%; margin-top: 0.5em">注册</el-button>
        </router-link>
        <div style="text-align: center; margin: 20px 0">
          <span style="color: #aaa">或者</span>
        </div>
        <!-- jAccount 登录按钮 -->
        <el-button
          link
          @click="redirectToAuth"
          style="
            width: 100%;
            background-color: #fff;
            color: #aaa;
            font-size: 16px;
            padding: 12px 0;
            border: none;
            box-shadow: none;
          "
        >
          <div style="display: block; width: 100%; text-align: center">
            <img
              src="https://i.sjtu.edu.cn/css/assets/images/jaccount.png"
              alt="jAccount"
              style="height: 48px"
            />
            <div style="display: block; width: 100%; text-align: center; margin-bottom: 8px">
              通过jAccount登录
            </div>
          </div>
        </el-button>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  /* 背景图设置 */
  background: url('https://i.sjtu.edu.cn/css/assets/images/bdbg.png') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  padding: 20px;
}

.card-wrapper {
  display: inline-block;
  width: 100%;
  max-width: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.login-card {
  padding: 20px;
}
</style>
