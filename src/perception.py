from datetime import datetime
from src.utils import extract_domain, headers, normalize_url, read_content, save_content, title_, summary_, is_ad, check_, what_score, what_word, get_keywords_id, logging, wash_url
import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from src.crawler import crawl
import time
import random
from src.data import push_page_to_db, push_keyword_to_db
import os
import requests
from bs4 import BeautifulSoup

proxies = {
    'http': 'http://127.0.0.1:7890',  # 为HTTP设置代理，端口根据实际情况修改
    'https': 'https://127.0.0.1:7890',  # 为HTTPS设置代理，端口根据实际情况修改
}

def get_article_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for item in soup.find_all('div', class_='item'):
        aid_tag = item.find('textarea', class_='item-aid')
        type_tag = item.find('textarea', class_='item-addltype')
        host_tag = item.find('textarea', class_='item-cnf-host')
        if aid_tag and type_tag and host_tag:
            aid = aid_tag.text.strip()
            addltype = type_tag.text.strip()
            host = host_tag.text.strip()
            url = f"https://{host}/{addltype}/{aid}"
            links.add(url)

    return list(set(links))

async def fetch_website_content(url):
    if "huanqiu" in "https://world.huanqiu.com/":
        return get_article_links(url)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers(headers)
        base_url = url
        try:
            await page.goto(base_url, wait_until='domcontentloaded', timeout=60000)     

        # await page.goto(base_url, timeout=60000)
            max_scroll_times = 30  # 最多滚动 30 次
            scroll_count = 0
            last_height = await page.evaluate("document.body.scrollHeight")

            while scroll_count < max_scroll_times:            
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")                        
                await page.wait_for_timeout(2000)  # 等待2秒            
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break  # 如果页面高度没有变化，则停止滚动

                last_height = new_height
                scroll_count += 1

        except:
            await page.goto(base_url, wait_until='networkidle', timeout=60000)     

        # await page.goto(base_url, timeout=60000)
            last_height = await page.evaluate("document.body.scrollHeight")
            max_scroll_times = 30 # 最多滚动 30 次
            scroll_count = 0

            while scroll_count < max_scroll_times:            
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")                        
                await page.wait_for_timeout(2000)  # 等待2秒            
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break  # 如果页面高度没有变化，则停止滚动

                last_height = new_height
                scroll_count += 1
        
        links = await page.query_selector_all("a")

        extract_links = []
        for link in links:
            href = await link.get_attribute("href")
            if href:
                absolute_url = urljoin(base_url, href)
                absolute_url = normalize_url(absolute_url)
                if absolute_url.startswith("http") and not is_ad(absolute_url): 
                    extract_links.append(absolute_url)
                # print(absolute_url)
        
        await browser.close()
        extract_links = list(set(extract_links))
        return extract_links

def preception(web):
    for url in web['url']:
        current_links = asyncio.run(fetch_website_content(url))
        current_date = datetime.now()

        folder_name = current_date.strftime("%Y-%m-%d")
        folder_path = "./src/data/out/" + folder_name + "/perception/" + extract_domain(url) + ".txt"     
        filename = "./src/data/saved_links/" + extract_domain(url) + '.json'
        dir_path = os.path.dirname(folder_path)
        
        os.makedirs(dir_path, exist_ok=True)

        previous_links = read_content(filename)    
        new_links = list(set(current_links) - set(previous_links))
        current_links = list(set(current_links) | set(previous_links))  
        save_content(current_links, filename) 
        
        logging(folder_path, f"Fetching {url}\n") 

        if new_links:
            logging(folder_path, f"New {len(new_links)} articles found.\n")
            for link in new_links:
                try:
                    if check_(link):
                        continue
                    title, content, times = crawl(link, url)
                    if not title or not content:
                        continue
                    summary = summary_(content)
                    title = title_(title)
                    publish_time = current_date.strftime("%Y-%m-%d %H:%M")
                    score = what_score(content)
                    source_url = wash_url(link)
                    if times:
                        publish_time = times
                    data = {
                        "title": title,
                        "content": summary,
                        "full_content":content,
                        "source_url": source_url,
                        "publish_time": publish_time,
                        'site_id': web['id'],
                        'score': score,
                    }
                    page_id = push_page_to_db(data)
                    keywords = what_word(content)
                    keywords_id = get_keywords_id(keywords)
                    if keywords_id:
                        push_keyword_to_db({
                            "page_id": page_id,
                            "keyword_id": keywords_id
                        })
                    sleep_time = random.uniform(0, 3)
                    time.sleep(sleep_time)
                except Exception as e:
                    logging(folder_path, f"Error: {link} {e}\n")
        else:
            logging(folder_path, f"No new articles found.\n")

def add_website(url):
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    path = f"./src/data/out/{folder_name}/run.txt" 
    logging(path, f"Adding {url}")    
    current_links = asyncio.run(fetch_website_content(url))
    filename = "./src/data/saved_links/" + extract_domain(url) + '.json' 
    save_content(current_links, filename)  

def main():
    web = {
        'id': 1,
        'url': [
            'https://news.swu.edu.cn/'
        ]
    }
    preception(web)

if __name__ == '__main__':
    main()
