// useScrollFetch.ts

export default function useScrollFetch(fetchPages: (count: number) => void, initialCount: number = 50) {
  let count = initialCount
  let scrollEventTriggered = false
  let wheelTimeout: ReturnType<typeof setTimeout> | null = null

  const handleScroll = (event: any) => {
    const scrollTop = event
    console.log('scrollTop', scrollTop)
    scrollEventTriggered = true
  }

  const handleWheel = (event: WheelEvent) => {
    if (wheelTimeout) {
      return
    }

    wheelTimeout = setTimeout(() => {
      requestAnimationFrame(() => {
        if (event.deltaY > 0 && !scrollEventTriggered) {
          console.log('鼠标向下滚动，但滚动事件没有被触发')
          count += 50
          fetchPages(count)
        }
        scrollEventTriggered = false
      })
      wheelTimeout = null
    }, 300)  // 节流的时间间隔可以根据需要调整
  }

  return { handleScroll, handleWheel }
}