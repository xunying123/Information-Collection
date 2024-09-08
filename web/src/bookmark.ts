import { reactive, watch } from 'vue'
import type { BookmarkItemPage, Page } from './api_interface'
import { extend } from 'lodash'

function load_bookmarks() {
  let bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
  // 检查数据是否符合新的格式
  if (bookmarks.length > 0 && typeof bookmarks[0].mark_time === 'undefined') {
    // 如果数据不符合新的格式，清空数据
    localStorage.removeItem('bookmarks')
    bookmarks = []
  }
  return bookmarks
}

const bookmarks = reactive<BookmarkItemPage[]>(load_bookmarks())

function save_bookmarks() {
  localStorage.setItem('bookmarks', JSON.stringify(bookmarks))
}
watch(bookmarks, save_bookmarks)

function toggle_bookmark(page: Page) {
  const index = bookmarks.findIndex((b) => b.id === page.id)
  if (index === -1) {
    // const { content, ...rest } = page
    // bookmarks.push(rest)
    // content // use it to suppress the warning

    // let yesterday = new Date();
    // yesterday.setDate(yesterday.getDate() - 1);
    const today = new Date().toISOString().slice(0, 10)
    const bookmarkItemPage: BookmarkItemPage = { ...page, mark_time: today }
    bookmarks.push(bookmarkItemPage)
  } else {
    bookmarks.splice(index, 1)
  }
}

function is_bookmarked(page_id: number) {
  return bookmarks.some((b) => b.id === page_id)
}

export { bookmarks, toggle_bookmark, is_bookmarked }
