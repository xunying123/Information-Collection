import { ref } from 'vue'

const count = ref(50)
const loading = ref(false)
const noMore = ref(false)

export function useInfiniteScroll(increment = 10) {
  const load = () => {
    if (loading.value || noMore.value) return
    console.log('加载更多项目，当前count:', count.value)
    count.value += increment
    loading.value = true
    setTimeout(() => {
      loading.value = false
    }, 1000)
  }

  function setNoMore(v: boolean) {
    noMore.value = v
  }

  return {
    count,
    load,
    loading,
    noMore,
    setNoMore
  }
}
