from common.models import Category, Site, Page

class ResponseSiteItem(dict):
    def __init__(self, site: Site):
        super().__init__()
        self["id"] = site.id
        self["name"] = site.name
        self["url"] = site.url
        self["cate_id"] = site.cate_id
        self["category"] = site.category.name


class ResponseCategory(dict):
    def __init__(self, cata: Category):
        super().__init__()
        self["id"] = cata.id
        self["name"] = cata.name
        print(self)


class ResponsePage(dict):
    def __init__(self, Page):
        super().__init__()
        self["id"] = Page.id
        self["source_url"] = Page.source_url
        self["title"] = Page.title
        self["content"] = Page.content
        self["site_id"] = Page.site.id
        self["site"] = Page.site.name
        self["cate_id"] = Page.category.id
        self["category"] = Page.category.name

class ResponseSite(ResponseSiteItem):
    def __init__(self, site: Site):
        super().__init__(site)
        self["pages"] = []
