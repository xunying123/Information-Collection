from common.models import Category, Site, Page

class ResponseSite(dict):
    def __init__(self, Site):
        super().__init__()
        self["id"] = Site.id
        self["name"] = Site.name
        self["url"] = Site.url
        self["category"] = Site.category.name


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
