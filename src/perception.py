from datetime import datetime
from utils import extract_domain, headers, normalize_url, is_ad, read_content, save_content
import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from crawler import crawl
from GeneralAgent import Agent

proxies = {
    'http': 'http://127.0.0.1:7890',  # 为HTTP设置代理，端口根据实际情况修改
    'https': 'https://127.0.0.1:7890',  # 为HTTPS设置代理，端口根据实际情况修改
}

Summary = Agent('下面会给你一篇中文文章，我需要你对它进行总结，是的最终我得到的总结长度在300-400之间', hide_python_code=True)

Translate = Agent('下面会给你一个英文标题，请把它翻译成中文', hide_python_code=True)

async def fetch_website_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers(headers)
        base_url = url
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

def preception(url):
    print(f"Fetching {url}")    
    current_links = asyncio.run(fetch_website_content(url))
    # print(f"Total {len(current_links)} articles found.")  
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"data/articles/{folder_name}/"     
    filename = "data/saved_links/" + extract_domain(url) + '.json'
    article_path = folder_path + extract_domain(url) + '.json'
    previous_links = read_content(filename)    
    new_links = list(set(current_links) - set(previous_links))
    current_links = list(set(current_links) | set(previous_links))  
    save_content(current_links, filename)  
    if new_links:
        print(f"New \033[92m{len(new_links)}\033[0m articles found.")
        articles = []
        for link in new_links:
            title, content = crawl(link)
            if not title or not content:
                continue
            # summary = Summary.run(content)
            publish_time = current_date.strftime("%Y-%m-%d %H:%M")
            data = {
                "title": title,
                "content": content,
                "source_url": link,
                "publish_time": publish_time
            }
            articles.append(data)
            # print(f"\033[92m{title}\033[0m saved.")
        save_content(articles, article_path)
    else:
        print(f"\033[31mNo\033[0m new articles found.")

def add_website(url):
    print(f"Fetching {url}")    
    current_links = asyncio.run(fetch_website_content(url)) 
    filename = "data/saved_links/" + extract_domain(url) + '.json' 
    save_content(current_links, filename)  

def main():
    for i in range(0, 100):
        url = 'https://edu.cri.cn/'
        preception(url)
    
    # for url in websites:
    #     preception(url)

if __name__ == '__main__':
    main()
