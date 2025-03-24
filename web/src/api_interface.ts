import type { PageItem, Page, SiteItem, Site, User, Keyword, Group } from '@/sdk'

interface BookmarkItemPage extends Page {
  mark_time: string
}

export type { PageItem, Page, SiteItem, Site, User, BookmarkItemPage, Keyword, Group }
