import './assets/main.css'

import { createApp, ref } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'element-plus/theme-chalk/el-notification.css'
import 'element-plus/theme-chalk/el-message-box.css'

import { user_key } from '@/key'
import type { User } from '@/api_interface'

const app = createApp(App)

const user = ref<User | null>(null)
app.provide(user_key, user)

app.use(createPinia())
app.use(router)

app.mount('#app')
