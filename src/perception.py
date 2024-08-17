import json
import os
from datetime import datetime
from utils import is_article, extract_domain, is_url, headers, normalize_url, is_ad, find_date
import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from crawler import crawl
import requests
from GeneralAgent import Agent
proxies = {
    'http': 'http://127.0.0.1:7890',  # 为HTTP设置代理，端口根据实际情况修改
    'https': 'https://127.0.0.1:7890',  # 为HTTPS设置代理，端口根据实际情况修改
}

Summary = Agent('下面会给你一篇文章，请帮我对它进行总结，大概三百字左右', hide_python_code=True)

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

def save_content(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def read_content(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def preception(url):
    print(f"Fetching {url}")    
    current_links = asyncio.run(fetch_website_content(url))
    # print(f"Total {len(current_links)} articles found.")       
    today_date = datetime.today().strftime('%Y-%m-%d') 
    filename = "data/saved_links/" + extract_domain(url) + '.json'
    article_path = "data/articles/" + today_date + '.json'
    previous_links = read_content(filename)    
    new_links = list(set(current_links) - set(previous_links))
    current_links = list(set(current_links) | set(previous_links))    
    if new_links:
        # print(new_links)
        print(f"New \033[92m{len(new_links)}\033[0m articles found.")
        save_content(current_links, filename)
        articles = read_content(article_path)
        for link in new_links:
            # response = requests.get(url, headers=headers)
            # date = find_date(response.text)
            # today = datetime.now().strftime('%Y-%m-%d')
            # if date != today:
            #     continue
            if not is_article(link):
                continue
            # 这里的判断有问题
            title, content = crawl(link)
            summary = Summary.run(content)
            articles.append({
                "title": title,
                "content": summary,
                "url": link
            })
            print(f"\033[92m{title}\033[0m saved.")
        save_content(articles, article_path)
    else:
        print(f"\033[31mNo\033[0m new articles found.")

def main():
    for i in range(0, 100):
        url = 'https://edu.cri.cn/'
        preception(url)
    
    # for url in websites:
    #     preception(url)

if __name__ == '__main__':
    main()
