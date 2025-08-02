import { ref } from 'vue'

const count = ref(50)

export function useInfiniteScroll(increment = 10) {
  const load = () => {
    console.log('加载更多项目，当前count:', count.value)
    count.value += increment
    this.loading = true
  }

  return {
    count,
    load
  }
}
