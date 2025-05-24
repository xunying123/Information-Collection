export const showTime = (date: string) => {
  const now = new Date()
  const dateObj = new Date(date)
  const diff = now.getTime() - dateObj.getTime()
  const diffHours = diff / 1000 / 60 / 60
  if (diffHours < 24) {
    return `${Math.floor(diffHours)} 小时前`
  } else if (diffHours < 48) {
    return '1 天前'
  } else {
    return dateObj.toLocaleDateString()
  }
}
