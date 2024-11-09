<template>
    <div class="user-page">
        <router-view></router-view>
        <div class="section">
            <el-popconfirm title="确定退出登录吗？" confirm-button-text="确定" cancel-button-text="取消" icon="el-icon-question"
                @confirm="logout">
                <template #reference>
                    <div class="button-container">
                        <el-button size="large" type="danger">退出登录</el-button>
                    </div>
                </template>
            </el-popconfirm>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject} from 'vue'
import { ElPopconfirm, ElNotification } from 'element-plus'
import { user_key } from '@/key'
import { server, jaccount_client_id } from '@/const'
const user = inject(user_key)!

const logout = async () => {
    if (!user)
        // impossible path ?
        return
    fetch(`${server}/logout`, { method: 'POST' })
        .then((r) => r.json())
        .then((d) => {
            if (d.code == 0)
                ElNotification({
                    title: '成功',
                    message: '退出登录成功',
                    type: 'success',
                    duration: 2000,
                    onClose: () => {
                        user.value = null
                        location.reload()
                        window.location.href = `http://jaccount.sjtu.edu.cn/oauth2/logout?client_id=${jaccount_client_id}&post_logout_redirect_uri=${encodeURIComponent(window.location.href)}`
                    }
                })
            else throw new Error(d.msg)
        })
        .catch((e) => {
            ElNotification({
                title: '错误',
                message: '退出登录失败: ' + e,
                type: 'error',
            })
        })
}
</script>

<style scoped>
.user-page {
    padding: 16px;
    background: rgba(255, 255, 255, 0.8);
    /* 半透明背景 */
    border-radius: 8px;
    /* 圆角 */
    max-width: 800px;
    /* 最大宽度 */
    margin: 40px auto;
    /* 垂直居中，顶部有间距 */
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