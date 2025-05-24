import { ref } from 'vue'
// 全局请求状态
export const isRequesting = ref(false)

// 锁定请求的函数
export function lockRequest() {
  isRequesting.value = true
}

// 释放请求锁的函数
export function unlockRequest() {
  isRequesting.value = false
}
