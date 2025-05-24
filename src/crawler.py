from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from newspaper import Article
import requests
from bs4 import BeautifulSoup,  Comment
from dateutil import parser 
from src.utils import read_content, save_content, check_page_content, headers, extract_domain, logging
import os

def Newspaper(url):
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()

        if not article.html:
            return None, None
        
        soup = BeautifulSoup(article.html, 'html.parser')
        h1 = soup.find('h1', class_='u-title')
        if h1 and h1.get_text(strip=True):
            article.title = h1.get_text(strip=True)
        else:
            h1 = soup.find('h1')
            if h1 and h1.get_text(strip=True):
                article.title = h1.get_text(strip=True)        

        comments = soup.find_all(string=lambda t: isinstance(t, Comment))

        start = next((c for c in comments if '正文开始' in c), None)
        end   = next((c for c in comments if '正文结束'   in c), None)

        if not (start and end):
            start = next((c for c in comments if '正文start' in c), None)
            end   = next((c for c in comments if '正文end'   in c), None)

        if not (start and end):
            start = next((c for c in comments if c.strip() == 'enpcontent'), None)
            end   = next((c for c in comments if c.strip() == '/enpcontent'), None)

        if start and end:
            nodes = []
            node = start.next_sibling
            while node and node is not end:
                nodes.append(node)
                node = node.next_sibling

            frag_html = ''.join(str(n) for n in nodes)

            frag_soup = BeautifulSoup(frag_html, 'html.parser')
            for el in frag_soup.find_all(style=lambda v: v and 'display:none' in v):
                el.decompose()
            for hid in frag_soup.find_all('input', type='hidden'):
                hid.decompose()
            for el in frag_soup.find_all(['div', 'p', 'span', 'a']):
                txt = el.get_text()
                if any(tag in txt for tag in ['ICP备', '版权所有', '公安机关备案']):
                    el.decompose()

            article.article_html = str(frag_soup)

            article.text = frag_soup.get_text(separator='\n\n', strip=True)

            if article.publish_date:
                publish_date_dt = article.publish_date
            else:
                publish_date_dt = datetime.now()

            now = datetime.now()
            if now >= publish_date_dt and (now - publish_date_dt) <= timedelta(days=3):
                return article, publish_date_dt
            else:
                publish_date_dt = datetime.now()
                
            return article, publish_date_dt
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
                return article, publish_date_dt
            else:
                publish_date_dt = datetime.now()

            return article, publish_date_dt

    except Exception as e:
        print("1Error parsing article:", e)
        return None, None
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

            if not article.html:
                return None, None
            
            soup = BeautifulSoup(article.html, 'html.parser')
            
            h1 = soup.find('h1', class_='u-title')
            if h1 and h1.get_text(strip=True):
                article.title = h1.get_text(strip=True)
            else:
                h1 = soup.find('h1')
                if h1 and h1.get_text(strip=True):
                    article.title = h1.get_text(strip=True)        

            comments = soup.find_all(string=lambda t: isinstance(t, Comment))
            start = next((c for c in comments if '正文开始' in c), None)
            end   = next((c for c in comments if '正文结束'   in c), None)
            
            if not (start and end):
                start = next((c for c in comments if '正文start' in c), None)
                end   = next((c for c in comments if '正文end'   in c), None)

            if not (start and end):
                start = next((c for c in comments if c.strip() == 'enpcontent'), None)
                end   = next((c for c in comments if c.strip() == '/enpcontent'), None)

            if start and end:
                nodes = []
                node = start.next_sibling
                while node and node is not end:
                    nodes.append(node)
                    node = node.next_sibling

                frag_html = ''.join(str(n) for n in nodes)

                frag_soup = BeautifulSoup(frag_html, 'html.parser')
                for el in frag_soup.find_all(style=lambda v: v and 'display:none' in v):
                    el.decompose()
                for hid in frag_soup.find_all('input', type='hidden'):
                    hid.decompose()
                for el in frag_soup.find_all(['div', 'p', 'span', 'a']):
                    txt = el.get_text()
                    if any(tag in txt for tag in ['ICP备', '版权所有', '公安机关备案']):
                        el.decompose()

                article.article_html = str(frag_soup)

                article.text = frag_soup.get_text(separator='\n\n', strip=True)

                if article.publish_date:
                    publish_date = article.publish_date
                else:
                    publish_date = datetime.now()

                now = datetime.now()
                if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                    return article.title, article.text, publish_date
                else:
                    publish_date = datetime.now()
                    
                    
                return article.title, article.text, publish_date

            if article:
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
                        publish_date = article.publish_date
                    else:
                        publish_date = datetime.now()

                    now = datetime.now()
                    if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                        return article.title, article.text, publish_date
                    else:
                        publish_date = datetime.now()

                    return article.title, article.text, publish_date
                
    except Exception as e:
        print("2Error parsing article:", e)
        return None, None, None
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
    crawl('http://politics.people.com.cn/n1/2025/0515/c1001-40480329.html', 'test')
    
if __name__ == '__main__':
    main()