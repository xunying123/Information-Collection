from common.models import Category, Site, Page


class ResponseSiteItem(dict):
    def __init__(self, site: Site):
        super().__init__()
        self["id"] = site.id
        self["name"] = site.name
        self["url"] = site.url
        self["cate_id"] = site.cate_id
        self["category"] = site.category.name
        self["icon"] = site.icon


class ResponseCategory(dict):
    def __init__(self, cata: Category):
        super().__init__()
        self["id"] = cata.id
        self["name"] = cata.name


class ResponsePageItem(dict):
    def __init__(self, page: Page):
        super().__init__()
        self["id"] = page.id
        self["source_url"] = page.source_url
        self["title"] = page.title
        # self["content"] = page.content
        self["site_id"] = page.site.id
        self["site"] = page.site.name
        self["site_icon"] = page.site.icon
        self["cate_id"] = page.category.id
        self["category"] = page.category.name
        self["publish_time"] = page.publish_time.isoformat()


class ResponseSite(ResponseSiteItem):
    def __init__(self, site: Site):
        super().__init__(site)
        self["pages"] = []


class ResponsePage(ResponsePageItem):
    def __init__(self, page: Page):
        super().__init__(page)
        self["content"] = page.content
