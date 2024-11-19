from playwright.sync_api import sync_playwright
from datetime import datetime
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from utils import read_content, save_content, check_page_content, headers, extract_domain

url = 'http://www.jyb.cn/rmtzgjyb/202411/t20241111_2111267743.html'

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

            # 返回清理后的文章
            return article

    except Exception as e:
        return None
    return None

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


            # 重新解析清理后的 HTML 内容
                article.html = str(soup)
                if article.title and article.text:
                    return article.title, article.text
                
    except Exception as e:
        return None, None
    return None, None
        
def Beautiful_Soup(url):
    try:
        # headers = random.choice(headers_pool)
        response = requests.get(url, headers=headers)

        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')

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
        if article_text :
            return title, article_text
    except Exception as e:
        return None, None
    return None, None

def Play_Wright_bs(url):
    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            context = browser.new_context()

            page = context.new_page()
            page.goto(url)

            page.wait_for_load_state("networkidle")

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
            if article_text :
                return title, article_text
    except Exception as e:
        return None, None
    return None, None

def crawl(url, source_url):
    #print(f"Fetching {url}")
    today_date = datetime.today().strftime('%Y-%m-%d')
    wrong_path = "/home/dic/Information-Collection/src/data/wrong/" + today_date + '/' + extract_domain(source_url) + '.json'

    temp = extract_domain(source_url)
    path = f"/home/dic/Information-Collection/src/data/out/{today_date}" + "/" + temp + '.txt'

    article = Newspaper(url)
    with open(path, 'a') as f:
        if article :
            if article.title and article.text and len(article.text) > 10 and check_page_content(article.title) and check_page_content(article.text):
                f.write("1")
                f.write('\n')
                # print(article.title)
                # print(article.text)
                return article.title, article.text
        
        title, content = Beautiful_Soup(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("2")
            f.write('\n')
            # print(title)
            # print(content)
            return title, content
    
        title, content = Play_Wright_new(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("3")
            f.write('\n')
            return title, content
    
        title, content = Play_Wright_bs(url)
        if title and content and len(content) > 10 and check_page_content(title) and check_page_content(content):
            f.write("4")
            f.write('\n')
            # print(title)
            # print(content)
            return title, content
        
        f.close()
    
    wrong = read_content(wrong_path)
    wrong.append({"url": url, "source_url": source_url})
    save_content(wrong, wrong_path)
    return None, None

def main():
    crawl(url, "http://www.sample.com/")
    
if __name__ == '__main__':
    main()