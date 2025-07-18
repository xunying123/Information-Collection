<template>
  <div class="register-page">
    <div class="card-wrapper">
      <el-card class="register-card">
        <el-form ref="registerFormRef" :model="registerForm" :rules="rules" label-position="top">
          <h2 style="text-align: center; margin-bottom: 20px">注册</h2>
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              placeholder="请再次输入密码"
              show-password
            />
          </el-form-item>
          <!-- <el-form-item label="手机号" prop="phone">
            <el-slider v-model="value1" :max="20000000000" :min="13000000000"/>
          </el-form-item> -->
          <el-form-item label="姓名" prop="name">
            <el-input v-model="registerForm.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="选择组织" prop="group">
            <el-select v-model="registerForm.group_id" placeholder="请选择组织" clearable>
              <el-option
                v-for="group in groupList"
                :key="group.id"
                :label="group.name"
                :value="group.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              style="width: 100%; margin-top: 0.5em; margin-right: 0%"
              @click="submitForm(registerFormRef)"
            >
              注册
            </el-button>
            <el-button
              style="width: 100%; margin-top: 1em; margin-left: 0%"
              @click="resetForm(registerFormRef)"
            >
              重置
            </el-button>
          </el-form-item>
        </el-form>
        <router-link :to="{ path: '/login', query: { next: next } }">
          <el-button link style="width: 100%; margin-top: 0.5em"> 返回登录 </el-button>
        </router-link>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElNotification } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { register, getGroups, type Group, type RegisterForm as BackendRegisterForm } from '@/sdk'

// const value1 = ref(0)

const groupList = ref<Group[]>([])

async function fetchGroupList() {
  const { data, error } = await getGroups()
  if (error) {
    ElNotification({
      title: '获取组织列表失败',
      message: String(error),
      type: 'error'
    })
    return
  }
  groupList.value = data!
}

interface RegisterForm extends BackendRegisterForm {
  confirmPassword: string
}

const registerFormRef = ref<FormInstance>()
const registerForm = reactive<RegisterForm>({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  group_id: null
})

const route = useRoute()

console.log('route', route.query)

const next = computed<string>(() => {
  return typeof route.query.next === 'string' ? route.query.next : '/'
})

const maxLen = 50

// 自定义确认密码校验器：确保确认密码与密码一致
const validateConfirmPassword = (rule: any, value: string, callback: (error?: Error) => void) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules<RegisterForm>>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: maxLen, message: `用户名长度应为2到${maxLen}个字符`, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: maxLen, message: `密码长度至少为6位`, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { max: maxLen, message: `姓名不能超过 ${maxLen} 个字符`, trigger: 'blur' }
  ],
  group_id: [{ required: true, message: '请选择组织', trigger: 'change' }]
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate(async (valid, fields) => {
    if (valid) {
      const { data, error } = await register({
        body: registerForm
      })
      if (error || data.status !== 200) {
        ElNotification({
          title: '注册失败',
          message: error ? String(error.detail) : data.message,
          type: 'error'
        })
        console.log(error)
        return
      }
      ElNotification({
        title: '注册成功！',
        message: '您可以使用新账号登录了，即将跳转到登录页面。<br>组织请等待管理员审核！',
        type: 'success',
        dangerouslyUseHTMLString: true
      })
      // 跳转到登录页面
      setTimeout(() => {
        window.location.href = '/login' + (next.value ? `?next=${next.value}` : '')
      }, 6000)
    } else {
      console.log('提交错误', fields)
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

onMounted(() => {
  fetchGroupList()
})
</script>

<style scoped>
.register-page {
  background: url('https://i.sjtu.edu.cn/css/assets/images/bdbg.png') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  padding: 20px;
  text-align: center;
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

.register-card {
  padding: 20px;
}
</style>
