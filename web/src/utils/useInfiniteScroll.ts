import { ref } from 'vue'

const count = ref(50)

export function useInfiniteScroll(increment = 10) {
  const loading = ref(false)
  const load = () => {
    console.log('加载更多项目，当前count:', count.value)
    count.value += increment
    loading.value = true
    setTimeout(() => {
      loading.value = false
    }, 1000)
  }

  return {
    count,
    load,
    loading
  }
}
