interface PageItem {
  id: number
  title: string
  source_url: string
  site_id: number
  site: string
  site_icon: string
  cate_id: number
  category: string
  publish_time: string // iso8601
}

interface Page extends PageItem {
  content: string
}

interface SiteItem {
  id: number
  name: string
  url: string
  cate_id: number
  category: string
  icon: string
}

interface Site extends SiteItem {
  pages: PageItem[]
}

export type { PageItem, Page, SiteItem, Site }
