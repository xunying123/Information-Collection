from src.db import db
from common.models import Keyword, Site, Page
from sqlalchemy import select, delete, exists, func, not_, or_
from utils import read_content, save_content
from perception import add_website

def get_keywords_from_db():
    keywords = db.query(Keyword).all()
    keyword = [keyword.word for keyword in keywords]
    return keyword

def get_postwebsites_from_db():
    sites = db.query(Site).all()
    site = [{"id": site.id, "name": site.name, "url": site.url, 'cate_id': site.cate_id} for site in sites]
    return site

def push_page_to_db(data):
    title = data.get("title")
    content = data.get("content")
    full_content = data.get("full_content")
    source_url = data.get("source_url")
    publish_time = data.get("publish_time")
    site_id = data.get("site_id")

    cate_id = db.scalar(select(Site.cate_id).where(Site.id == site_id))
    if cate_id is None:
        return ValueError("site_id not found")

    existed_id = db.scalar(select(Page.id).where(Page.source_url == source_url))
    if existed_id is not None:
        return
    
    page = Page(
        site_id=site_id,
        title=title,
        content=content,
        full_content=full_content,
        source_url=source_url,
        cate_id=cate_id,
        publish_time=publish_time, 
    )
    db.add(page)
    db.flush()

def get_post_websites():
    post_websites = get_postwebsites_from_db()
    new_urls = []
    for item in post_websites:
        for i in item['url']:
            new_urls.append(i)
    old_urls = read_content("./src/data/websites.json")

    new_unique_urls = [url for url in new_urls if url not in old_urls]

    for links in new_unique_urls:
        try:
            add_website(links)
        except Exception as e:
            print(f"Error: {links}", flush=True)
            new_urls.remove(links)
            continue

    save_content(new_urls, "./src/data/websites.json")
    save_content(post_websites, "./src/data/post_websites.json")