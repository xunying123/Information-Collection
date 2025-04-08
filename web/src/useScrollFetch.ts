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

    wheelTimeout = setTimeout(() => {
      requestAnimationFrame(() => {
        if (event.deltaY > 0 && !scrollEventTriggered) {
          count += 10
          fetchPages(count)
        }
        scrollEventTriggered = false
      })
      wheelTimeout = null
    }, 10) // 节流的时间间隔可以根据需要调整
  }

  return { handleScroll, handleWheel }
}
