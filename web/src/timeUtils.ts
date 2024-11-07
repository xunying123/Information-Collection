export const timeType = (date: string) => {
    const now = new Date()
    const diff = now.getTime() - new Date(date).getTime()
    const diffHours = diff / 1000 / 60 / 60
    if (diffHours < 48) {
      return 'relative'
    } else {
      return 'date'
    }
  }