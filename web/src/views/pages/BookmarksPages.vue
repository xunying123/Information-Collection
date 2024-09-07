<template>
  <ShowCards :pages="displayedBookmarks" title="书签" :loading="false">
    <div style="margin-left: 10px;">
      <el-button type="primary" @click="openDialog">导出 Word</el-button>
      <el-button type="danger" @click="reset_bookmarks">清空书签</el-button>
    </div>
    <el-pagination @current-change="handleCurrentChange" :current-page="currentDay + 1" layout="prev, pager, next"
      style="margin-left: 10px;" :page-count="groupedBookmarks.length" />

    <el-dialog title="选择要导出的书签" v-model="dialogVisible" :width="dialogWidth" class="responsive-dialog">
      <el-form ref="form" label-width="120px" size="large">
        <el-form-item label="当前期数">
          <el-input v-model="formIssue" class="issue-input"></el-input>
        </el-form-item>
        <el-form-item label="选择日期">
          <el-date-picker v-model="formDate" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
      </el-form>
      <el-scrollbar style="height: 300px;" :width="dialogWidth">
        <el-checkbox-group v-model="selectedBookmarks"
          style="margin-left: 56px; width: 90%;">
          <el-checkbox size="large" v-for="bookmark in bookmarks" :value="bookmark" :label="bookmark.title"
          class="checkbox"
          >
            {{ bookmark.title }} - {{ bookmark.publish_time.slice(0, 10) }}
          </el-checkbox>
        </el-checkbox-group>
      </el-scrollbar>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmExport">确认导出</el-button>
      </span>
    </el-dialog>
  </ShowCards>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect, onMounted, onBeforeUnmount } from 'vue'
import { groupBy } from 'lodash'
import { bookmarks } from '@/bookmark'
import PizZip from 'pizzip'
import Docxtemplater from 'docxtemplater'
import { saveAs } from 'file-saver'
import type { BookmarkItemPage } from '../../api_interface'
import ShowCards from '@/components/ShowCards.vue'

let dialogWidth = ref('900px');

let currentDay = ref(0)
let dialogVisible = ref(false) // 控制弹窗的可见性
let selectedBookmarks = ref<BookmarkItemPage[]>([]) // 用户选择的书签

let groupedBookmarks = ref<BookmarkItemPage[][]>([])
let displayedBookmarks = computed(() => {
  return groupedBookmarks.value[currentDay.value] || []
})

onMounted(() => {
  bookmarks.sort((a, b) => b.mark_time.localeCompare(a.mark_time))
  updateDialogWidth();
  window.addEventListener('resize', updateDialogWidth);
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateDialogWidth);
});

let updateDialogWidth = () => {
  if (window.innerWidth <= 768) {
    dialogWidth.value = '90%';
  } else {
    dialogWidth.value = '900px';
  }
};

// 已知的日期和期数
const knownDate = new Date(2024, 6, 17) // 注意，JavaScript中的月份是从0开始的，所以7月是6
const knownIssue = 4282

// 计算今天的日期和已知日期之间的天数差
const today = new Date()
const diffDays = Math.ceil((today.getTime() - knownDate.getTime()) / (1000 * 60 * 60 * 24))

// 计算今天的期数
let formIssue = ref(knownIssue + diffDays)
let formDate = ref(new Date().toISOString().slice(0, 10))


watchEffect(() => {
  let groups = groupBy(bookmarks, (bookmark: BookmarkItemPage) => bookmark.mark_time.slice(0, 10))
  groupedBookmarks.value = Object.values(groups)
})

let handleCurrentChange = (newDay: number) => {
  currentDay.value = newDay - 1
}

// 打开弹窗并默认选中今日书签
function openDialog() {
  selectedBookmarks.value = displayedBookmarks.value
  dialogVisible.value = true
}

// 确认导出
async function confirmExport() {
  dialogVisible.value = false
  await exportWord(selectedBookmarks.value)
}

function reset_bookmarks() {
  bookmarks.splice(0, bookmarks.length)
}

async function exportWord(selectedBookmarks: BookmarkItemPage[]) {
  const response = await fetch('/static/template.docx')
  const templateArrayBuffer = await response.arrayBuffer()

  // 初始化 PizZip 和 Docxtemplater
  const zip = new PizZip(templateArrayBuffer)
  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true
  })

  // 当前日期
  const currentDate = new Date(formDate.value)
  const year = currentDate.getFullYear()
  const month = currentDate.getMonth() + 1
  const date = currentDate.getDate()
  const day = ['日', '一', '二', '三', '四', '五', '六'][currentDate.getDay()]

  // 准备数据
  const categories = ['科教要闻', '院校动态', '国际视野']

  const data = {
    sum: formIssue.value, // 使用书签数量作为期数
    year,
    month,
    date,
    day,
    articles: [] as {
      category: string
      bookmarks: { title: string; content: string; site: string }[]
    }[] // 修改 articles 属性
  }

  const articles = categories
    .map((category) => {
      const categoryBookmarks = selectedBookmarks
        .filter((bookmark) => bookmark.category === category)
        .map((bookmark) => ({
          title: bookmark.title,
          content: bookmark.content,
          site: bookmark.site
        }))

      return { category, bookmarks: categoryBookmarks }
    })
    .filter((article) => article.bookmarks.length > 0)

  data.articles = articles

  // 替换模板中的占位符
  doc.render(data)

  // 导出为 Word 文档
  const output = doc.getZip().generate({
    type: 'blob',
    mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  })

  // 使用 FileSaver.js 保存文档
  saveAs(output, `每日情况通报_${year}_${month}_${date}.docx`)
}
</script>

<style scoped>
@media (max-width: 768px) {
  .issue-input {
    width: 70px !important;
  }
}

.issue-input {
  width: 10%;
}

.checkbox {
  width: 100%;
  white-space: normal;
  overflow-wrap: break-word; 
}

</style>