import { reactive, watch } from 'vue'
import type { Page } from './interface'

interface BookmarkItemPage {
  id: number
  title: string
  // content: string // except content
  source_url: string
  site_id: number
  site: string
  cate_id: number
  category: string
}

function load_bookmarks() {
  return JSON.parse(localStorage.getItem('bookmarks') || '[]')
}

const bookmarks = reactive<BookmarkItemPage[]>(load_bookmarks())

function save_bookmarks() {
  localStorage.setItem('bookmarks', JSON.stringify(bookmarks))
}
watch(bookmarks, save_bookmarks)

function toggle_bookmark(page: Page) {
  const index = bookmarks.findIndex((b) => b.id === page.id)
  if (index === -1) {
    const { content, ...rest } = page
    bookmarks.push(rest)
    content // use it to suppress the warning
  } else {
    bookmarks.splice(index, 1)
  }
}

function is_bookmarked(page: Page) {
  return bookmarks.some((b) => b.id === page.id)
}

export { bookmarks, toggle_bookmark, is_bookmarked }
