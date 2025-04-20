from common.models import *
from sqlalchemy import select, delete, exists, func, not_, or_
from src.db import get_db

def get_keywords_from_db():
    with get_db() as db:
        keywords = db.query(Keyword).all()
        keyword = [{"id": keyword.id, "word": keyword.word} for keyword in keywords]
        return keyword
    
def get_keywords_map_from_db():
    with get_db() as db:
        keywords = db.query(Keyword).all()
        keyword = [{"id": keyword.id, "word": keyword.word} for keyword in keywords]
        mapping = {item['word']: item['id'] for item in keyword}
        return mapping

def get_postwebsites_from_db():
    with get_db() as db:
        sites = db.query(Site).all()
        site = [{"id": site.id, "name": site.name, "url": site.url} for site in sites]
        return site

def push_page_to_db(data):
    title = data.get("title")
    content = data.get("content")
    full_content = data.get("full_content")
    source_url = data.get("source_url")
    publish_time = data.get("publish_time")
    site_id = data.get("site_id")
    score = data.get("score")
    
    with get_db() as db:
        id = db.scalar(select(Site.id).where(Site.id == site_id))
        if id is None:
            raise ValueError("site_id not found")

        existed_id = db.scalar(select(Page.id).where(Page.source_url == source_url))
        if existed_id is not None:
            raise ValueError("source_url already exists")

        page = Page(
            site_id=site_id,
            title=title,
            content=content,
            full_content=full_content,
            source_url=source_url,
            publish_time=publish_time, 
            score=score,
        )
        try:
            db.add(page)
            db.flush()
            aa = page.id
            db.commit()
            return aa
        except Exception as e:
            raise ValueError(f"Error adding page: {e}")
    
def push_keyword_to_db(data):
    page_id = data.get("page_id")
    keyword_id = data.get("keyword_id")
    
    if not all([page_id, keyword_id]):
        raise ValueError("page_id or keyword_id not found")
    for kw_id in keyword_id:
        if type(kw_id) is not int:
            raise ValueError("keyword_id must be integer")
        
    with get_db() as db:
        if db.scalar(select(Page.id).where(Page.id == page_id)) is None:
            return ValueError("page_id not found")
        
        for kw_id in keyword_id:
            if db.scalar(select(Keyword.id).where(Keyword.id == kw_id)) is None:
                return ValueError("keyword_id not found")
        try:
            for kw_id in keyword_id:
                if (
                    db.scalar(
                        select(PageKeywordRelation).where(
                            (PageKeywordRelation.page_id == page_id)
                            & (PageKeywordRelation.keyword_id == kw_id)
                        )
                    )
                    is not None
                ):
                    continue
                db.add(PageKeywordRelation(page_id=page_id, keyword_id=kw_id))
            db.commit()
        except Exception as e:
            raise ValueError(f"Error adding page_keyword_relation: {e}")

def get_post_websites():
    from src.utils import read_content, save_content, logging
    from src.perception import add_website
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
            current_date = datetime.now()
            folder_name = current_date.strftime("%Y-%m-%d")
            path = f"./src/data/out/{folder_name}/run.txt"  
            logging(path, f"Error: {links}")
            new_urls.remove(links)
            continue

    save_content(new_urls, "./src/data/websites.json")
    save_content(post_websites, "./src/data/post_websites.json")
    
def get_keywords():
    from src.utils import save_content
    keywords = get_keywords_from_db()
    save_content(keywords, "./src/data/word.json")