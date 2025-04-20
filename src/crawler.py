from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from dateutil import parser 
from src.utils import read_content, save_content, check_page_content, headers, extract_domain, logging
import os

def Newspaper(url):
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()

        if article.text:
            soup = BeautifulSoup(article.html, 'html.parser')

            for element in soup.find_all(style=lambda value: value and 'display:none' in value):
                element.decompose()

            for hidden_input in soup.find_all('input', type='hidden'):
                hidden_input.decompose()

            for element in soup.find_all(['div', 'p', 'span', 'a']):
                text_content = element.get_text()
                if 'ICP备' in text_content or '版权所有' in text_content or '公安机关备案' in text_content:
                    element.decompose()  # 删除该元素

            article.html = str(soup)

            if article.publish_date:
                publish_date_dt = article.publish_date
            else:
                publish_date_dt = datetime.now()

            now = datetime.now()
            if now >= publish_date_dt and (now - publish_date_dt) <= timedelta(days=3):
                formatted_publish_date = publish_date_dt.strftime('%Y-%m-%d %H:%M')
                return article, formatted_publish_date
            else:
                publish_date_dt = None

            return article, publish_date_dt

    except Exception as e:
        print("1Error parsing article:", e)
        return None, None
    print(1)
    return None, None

def Play_Wright_new(url):
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            page = context.new_page()
            page.goto(url)

            page.wait_for_load_state("networkidle")

            page_content = page.content()

            browser.close()

            article = Article(url)
            article.set_html(page_content)
            article.parse()

            if article:
                soup = BeautifulSoup(article.html, 'html.parser')

                for element in soup.find_all(style=lambda value: value and 'display:none' in value):
                    element.decompose()
                
                for hidden_input in soup.find_all('input', type='hidden'):
                    hidden_input.decompose()

                for element in soup.find_all(['div', 'p', 'span', 'a']):
                    text_content = element.get_text()
                    if 'ICP备' in text_content or '版权所有' in text_content or '公安机关备案' in text_content:
                        element.decompose()  # 删除该元素


                article.html = str(soup)
                if article.title and article.text:

                    if article.publish_date:
                        publish_date = article.publish_date.strftime('%Y-%m-%d %H:%M')
                    else:
                        publish_date = None

                    now = datetime.now()
                    if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                        return article.title, article.text, publish_date
                    else:
                        publish_date = None

                    return article.title, article.text, publish_date
                
    except Exception as e:
        print("2Error parsing article:", e)
        return None, None, None
    print(2)
    return None, None, None
        
def Beautiful_Soup(url):
    try:
        # headers = random.choice(headers_pool)
        response = requests.get(url, headers=headers)

        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')

        publish_time_str = None

        meta_attrs_list = [
            {'property': 'article:published_time'},
            {'name': 'pubdate'},
            {'name': 'publishdate'},
            {'name': 'timestamp'}
        ]


        for element in soup.find_all(style=lambda value: value and 'display:none' in value):
            element.decompose()  # 删除该元素

        for hidden_input in soup.find_all('input', type='hidden'):
            hidden_input.decompose()

        for element in soup.find_all(['div', 'p', 'span', 'a']):
            text_content = element.get_text()
            if 'ICP备' in text_content or '版权所有' in text_content or '公安机关备案' in text_content:
                element.decompose()  # 删除该元素

        title = soup.find('title').get_text()
        content = soup.find_all('p')

        article_text = "\n\n".join([p.get_text() for p in content])

        for attrs in meta_attrs_list:
            tag = soup.find('meta', attrs=attrs)
            if tag and tag.get('content'):
                publish_time_str = tag['content']
                break

        if not publish_time_str:
            time_tag = soup.find('time')
            if time_tag:
                if time_tag.has_attr('datetime'):
                    publish_time_str = time_tag['datetime']
                else:
                    publish_time_str = time_tag.get_text(strip=True)
        
        if not publish_time_str:
            publish_date_str = None
        else:
            try:
                publish_date = parser.parse(publish_time_str)
        
                publish_date_str = publish_date.strftime('%Y-%m-%d %H:%M')
        
                if publish_date.tzinfo:
                    now = datetime.now(publish_date.tzinfo)
                else:
                    now = datetime.now()
        
                if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                    a = 0
                else:
                    publish_date_str = None
            
            except Exception as e:
                print("解析发布时间错误：", e)

        if article_text :
            return title, article_text, publish_date_str
        
    except Exception as e:
        print("3Error parsing article:", e)
        return None, None, None
    print(3)
    return None, None, None

def Play_Wright_bs(url):
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            page = context.new_page()
            page.goto(url)

            page.wait_for_load_state("networkidle")

            publish_time_str = None

            meta_attrs_list = [
                {'property': 'article:published_time'},
                {'name': 'pubdate'},
                {'name': 'publishdate'},
                {'name': 'timestamp'}
            ]

            page_content = page.content()

            browser.close()
            soup = BeautifulSoup(page_content, 'lxml')

            for element in soup.find_all(style=lambda value: value and 'display:none' in value):
                element.decompose()  # 删除该元素

            for hidden_input in soup.find_all('input', type='hidden'):
                hidden_input.decompose()

            for element in soup.find_all(['div', 'p', 'span', 'a']):
                text_content = element.get_text()
                if 'ICP备' in text_content or '版权所有' in text_content or '公安机关备案' in text_content:
                    element.decompose()  # 删除该元素

            title = soup.find('title').get_text()
            content = soup.find_all('p')

            article_text = "\n\n".join([p.get_text() for p in content])

            for attrs in meta_attrs_list:
                tag = soup.find('meta', attrs=attrs)
                if tag and tag.get('content'):
                    publish_time_str = tag['content']
                    break

            if not publish_time_str:
                time_tag = soup.find('time')
                if time_tag:
                    if time_tag.has_attr('datetime'):
                        publish_time_str = time_tag['datetime']
                    else:
                        publish_time_str = time_tag.get_text(strip=True)
        
            if not publish_time_str:
                publish_date_str = None
            else:
                try:
                    publish_date = parser.parse(publish_time_str)
        
                    publish_date_str = publish_date.strftime('%Y-%m-%d %H:%M')
        
                    if publish_date.tzinfo:
                        now = datetime.now(publish_date.tzinfo)
                    else:
                        now = datetime.now()
        
                    if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                        a = 0
                    else:
                        publish_date_str = None
            
                except Exception as e:
                    print("解析发布时间错误：", e)

            if article_text :
                return title, article_text, publish_date_str
    except Exception as e:
        print("4Error parsing article:", e)
        return None, None, None
    print(4)
    return None, None, None

def crawl(url, source_url):
    today_date = datetime.today().strftime('%Y-%m-%d')
    wrong_path = "./src/data/out/" + today_date + '/wrong.json'

    path = "./src/data/out/" + today_date + '/crawler/' + extract_domain(source_url) + '.txt'
    dir_path = os.path.dirname(path)
    
    os.makedirs(dir_path, exist_ok=True)
    
    article, time = Newspaper(url)
    logging(path, f"Fetching {url}\n")
    if article :
        a = check_page_content(article.title)
        b = check_page_content(article.text)
        if a == 0 or b == 0:
            logging(path, "Page Not Found")
        elif a == 1 or b == 1:
            logging(path, "The URL you requested has been blocked")
        elif a == 2 or b == 2:
            logging(path, "LLM(Large Languate Model) error")
        elif article.title and article.text and len(article.text) > 10:
            logging(path, "1\n")
            # print(article.title)
            # print(article.text)
            # print(time)
            return article.title, article.text, time
        
    title, content, time = Beautiful_Soup(url)
    if title and content:
        a = check_page_content(title)
        b = check_page_content(content)
        if a == 0 or b == 0:
            logging(path, "Page Not Found")
        elif a == 1 or b == 1:
            logging(path, "The URL you requested has been blocked")
        elif a == 2 or b == 2:
            logging(path, "LLM(Large Languate Model) error")
        elif title and content and len(content) > 10:
            logging(path, "2\n")
            # print(title)
            # print(content)
            # print(time)
            return title, content, time

    title, content, time = Play_Wright_new(url)
    if title and content:
        a = check_page_content(title)
        b = check_page_content(content)
        if a == 0 or b == 0:
            logging(path, "Page Not Found")
        elif a == 1 or b == 1:
            logging(path, "The URL you requested has been blocked")
        elif a == 2 or b == 2:
            logging(path, "LLM(Large Languate Model) error")
        elif title and content and len(content) > 10:
            logging(path, "3\n")
            return title, content, time


    title, content, time = Play_Wright_bs(url)
    if title and content:
        a = check_page_content(title)
        b = check_page_content(content)
        if a == 0 or b == 0:
            logging(path, "Page Not Found")
        elif a == 1 or b == 1:
            logging(path, "The URL you requested has been blocked")
        elif a == 2 or b == 2:
            logging(path, "LLM(Large Languate Model) error")
        elif title and content and len(content) > 10:
            logging(path, "4\n")
            return title, content, time
    
    wrong = read_content(wrong_path)
    wrong.append({"url": url})
    save_content(wrong, wrong_path)
    return None, None, None

def main():
    crawl('https://news.upc.edu.cn/info/1432/116321.htm', 'test')
    
if __name__ == '__main__':
    main()