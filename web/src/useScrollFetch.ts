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
// 带锁定的请求执行器
export async function executeWithLock<T>(requestFn: () => Promise<T>): Promise<T> {
  if (isRequesting.value) {
    console.log('请求已在进行中，忽略新请求')
    throw new Error('请求已在进行中')
  }
  
  try {
    lockRequest()
    return await requestFn()
  } finally {
    unlockRequest()
  }
}

export default function useScrollFetch(
  fetchPages: (count: number) => void,
  initialCount: number = 0
) {
  let count = initialCount
  let scrollEventTriggered = false
  let wheelTimeout: ReturnType<typeof setTimeout> | null = null

  const handleScroll = () => {
    scrollEventTriggered = true
  }

  const handleWheel = (event: WheelEvent) => {
    if (wheelTimeout) {
      return
    }
    if (isRequesting.value) {
      return
    }

    wheelTimeout = setTimeout(() => {
      requestAnimationFrame(() => {
        if (event.deltaY > 0 && !scrollEventTriggered) {
          count += 10
          fetchPages(count)
        }
        scrollEventTriggered = false
      })
      wheelTimeout = null
    }, 500) // 节流的时间间隔可以根据需要调整
  }

  return { handleScroll, handleWheel }
}
