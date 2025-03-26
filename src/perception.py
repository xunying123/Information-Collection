from datetime import datetime
from utils import extract_domain, headers, normalize_url, read_content, save_content, title_, summary_, is_ad, check_
import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from crawler import crawl
import time
import random
from data import push_page_to_db

proxies = {
    'http': 'http://127.0.0.1:7890',  # 为HTTP设置代理，端口根据实际情况修改
    'https': 'https://127.0.0.1:7890',  # 为HTTPS设置代理，端口根据实际情况修改
}

async def fetch_website_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers(headers)
        base_url = url
        try:
            await page.goto(base_url, wait_until='domcontentloaded', timeout=60000)     

        # await page.goto(base_url, timeout=60000)
            last_height = await page.evaluate("document.body.scrollHeight")

            while True:            
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")                        
                await page.wait_for_timeout(2000)  # 等待2秒            
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break  # 如果页面高度没有变化，则停止滚动

                last_height = new_height

        except:
            await page.goto(base_url, wait_until='networkidle', timeout=60000)     

        # await page.goto(base_url, timeout=60000)
            last_height = await page.evaluate("document.body.scrollHeight")

            while True:            
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")                        
                await page.wait_for_timeout(2000)  # 等待2秒            
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break  # 如果页面高度没有变化，则停止滚动

                last_height = new_height
        
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

        previous_links = read_content(filename)    
        new_links = list(set(current_links) - set(previous_links))
        current_links = list(set(current_links) | set(previous_links))  
        save_content(current_links, filename)  
    
        with open(folder_path, 'a') as f:
            f.write(f"Fetching {url}\n")  

            if new_links:
                f.write(f"New {len(new_links)} articles found.\n")
                for link in new_links:
                    if check_(link):
                        continue
                    title, content, times = crawl(link, url)
                    if not title or not content:
                        continue
                    summary = summary_(content)
                    title = title_(title)
                    publish_time = current_date.strftime("%Y-%m-%d %H:%M")
                    if times:
                        publish_time = times
                    data = {
                        "title": title,
                        "content": summary,
                        "full_content":content,
                        "source_url": link,
                        "publish_time": publish_time,
                        'cate_id': web['cate_id'],
                    }
                    push_page_to_db(data)
                    sleep_time = random.uniform(0, 3)
                    time.sleep(sleep_time)
            else:
                f.write(f"No new articles found.")
                f.write('\n')

            f.close()

def add_website(url):
    print(f"Adding {url}", flush=True)    
    current_links = asyncio.run(fetch_website_content(url))
    filename = "./src/data/saved_links/" + extract_domain(url) + '.json' 
    save_content(current_links, filename)  

def main():
    url = 'http://www.xinhuanet.com/'
    preception(url)

if __name__ == '__main__':
    main()
