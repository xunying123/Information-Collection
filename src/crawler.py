from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from dateutil import parser 
from utils import read_content, save_content, check_page_content, headers, extract_domain

url = 'https://www.gov.cn/yaowen/liebiao/202501/content_7001817.htm'

def Newspaper(url):
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()

        if article.text:
            soup = BeautifulSoup(article.html, 'html.parser')
            
            # 删除所有 display:none 的元素
            for element in soup.find_all(style=lambda value: value and 'display:none' in value):
                element.decompose()

            for hidden_input in soup.find_all('input', type='hidden'):
                hidden_input.decompose()

            for element in soup.find_all(['div', 'p', 'span', 'a']):
                text_content = element.get_text()
                if 'ICP备' in text_content or '版权所有' in text_content or '公安机关备案' in text_content:
                    element.decompose()  # 删除该元素


            # 重新解析清理后的 HTML 内容
            article.html = str(soup)

            if article.publish_date:
                publish_date = article.publish_date.strftime('%Y-%m-%d %H:%M')
            else:
                publish_date = None

            now = datetime.now()
            if now >= publish_date and (now - publish_date) <= timedelta(days=3):
                return article, publish_date
            else:
                publish_date = None

            return article, publish_date

    except Exception as e:
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

            if article:
                soup = BeautifulSoup(article.html, 'html.parser')
            
            # 删除所有 display:none 的元素
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
        return None, None, None
    return None, None, None

def crawl(url, source_url):
    #print(f"Fetching {url}")
    today_date = datetime.today().strftime('%Y-%m-%d')
    wrong_path = "/home/dic/Information-Collection/src/data/wrong/" + today_date + '/' + extract_domain(source_url) + '.json'

    temp = extract_domain(source_url)
    path = f"/home/dic/Information-Collection/src/data/out/{today_date}" + "/" + temp + '.txt'

    article, time = Newspaper(url)
    with open(path, 'a') as f:
        if article :
            if article.title and article.text and len(article.text) > 10 and check_page_content(article.title) and check_page_content(article.text):
                f.write("1")
                f.write('\n')
                # print(article.title)
                # print(article.text)
                return article.title, article.text, time
        
        title, content, time = Beautiful_Soup(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("2")
            f.write('\n')
            # print(title)
            # print(content)
            return title, content, time
    
        title, content, time = Play_Wright_new(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("3")
            f.write('\n')
            return title, content, time
    
        title, content, time = Play_Wright_bs(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("4")
            f.write('\n')
            # print(title)
            # print(content)
            return title, content, time
        
        f.close()
    
    wrong = read_content(wrong_path)
    wrong.append({"url": url, "source_url": source_url})
    save_content(wrong, wrong_path)
    return None, None, None

def main():
    crawl(url, "http://www.sample.com/")
    
if __name__ == '__main__':
    main()