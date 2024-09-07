import { reactive, watch } from 'vue'
import type { BookmarkItemPage, Page } from './api_interface'
import { extend } from 'lodash'

function load_bookmarks() {
  console.log('load_bookmarks')
  // localStorage.removeItem('bookmarks');
  console.log(localStorage.getItem('bookmarks') || '[]')
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
    // const { content, ...rest } = page
    // bookmarks.push(rest)
    // content // use it to suppress the warning
    
    // let yesterday = new Date();
    // yesterday.setDate(yesterday.getDate() - 1);
    const today = new Date().toISOString().slice(0, 10);
    const bookmarkItemPage: BookmarkItemPage = { ...page, mark_time: today };
    bookmarks.push(bookmarkItemPage);
  } else {
    bookmarks.splice(index, 1)
  }
}

function is_bookmarked(page_id: number) {
  return bookmarks.some((b) => b.id === page_id)
}

export { bookmarks, toggle_bookmark, is_bookmarked }
