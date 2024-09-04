<template>
  <ShowCards :pages="bookmarks" title="书签" :loading="false">
    <el-button type="primary" @click="exportWord">导出 Word</el-button>
    <el-button type="danger" @click="reset_bookmarks">清空书签</el-button>
  </ShowCards>
</template>

<script setup lang="ts">
import { bookmarks } from '@/bookmark'
import PizZip from 'pizzip'
import Docxtemplater from 'docxtemplater'
import { saveAs } from 'file-saver'
import type { Blob } from 'buffer'
import { ar } from 'element-plus/es/locales.mjs'
import ShowCards from '@/components/ShowCards.vue'

function reset_bookmarks() {
  bookmarks.splice(0, bookmarks.length)
}

async function exportWord() {
  const response = await fetch('/static/template.docx')
  const templateArrayBuffer = await response.arrayBuffer()

  // 初始化 PizZip 和 Docxtemplater
  const zip = new PizZip(templateArrayBuffer)
  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true
  })

  // 当前日期
  const currentDate = new Date()
  const year = currentDate.getFullYear()
  const month = currentDate.getMonth() + 1
  const date = currentDate.getDate()
  const day = ['日', '一', '二', '三', '四', '五', '六'][currentDate.getDay()]

  // 准备数据
  const categories = ['科教要闻', '院校动态', '国际视野']

  const data = {
    sum: bookmarks.length, // 使用书签数量作为期数
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
      const categoryBookmarks = bookmarks
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
