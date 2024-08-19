interface Site {
  id: number
  name: string
  url: string
  cate_id: number
  category: string
}

interface CateSite {
  cate_id: number
  cate_name: string
  sites: Site[]
}

interface Page {
  id: number
  title: string
  content: string
  source_url: string
  site_id: number
  site: string
  cate_id: number
  category: string
}

interface SiteQuery extends Site {
  pages: Page[]
}

export type { Site, CateSite, Page, SiteQuery }
