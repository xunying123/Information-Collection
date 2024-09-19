from playwright.sync_api import sync_playwright
from datetime import datetime
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from utils import read_content, save_content, check_page_content

url = 'https://sample.com'

def Newspaper(url):
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()
        if article.text:
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
                if article.title and article.text:
                    return article.title, article.text
    except Exception as e:
        return None, None
    return None, None
        
def Beautiful_Soup(url):
    try:
        response = requests.get(url)

        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('title').get_text()
        content = soup.find_all('p')

        article_text = "\n".join([p.get_text() for p in content])
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

            title = soup.find('title').get_text()
            content = soup.find_all('p')

            article_text = "\n".join([p.get_text() for p in content])
            if article_text :
                return title, article_text
    except Exception as e:
        return None, None
    return None, None

def crawl(url, source_url):
    #print(f"Fetching {url}")
    today_date = datetime.today().strftime('%Y-%m-%d')
    wrong_path = "/home/dic/Information-Collection/src/data/wrong/" + today_date + '.json'

    article = Newspaper(url)

    if article :
        if article.title and article.text and len(article.text) > 10 and check_page_content(article.title):
            print(1, flush=True)
            return article.title, article.text
        
    title, content = Beautiful_Soup(url)
    if title and content and len(content) > 10 and check_page_content(title):
        print(2, flush=True)
        # print(title)
        # print(content)
        return title, content
    
    title, content = Play_Wright_new(url)
    if title and content and len(content) > 10 and check_page_content(title):
        print(3, flush=True)
        return title, content
    
    title, content = Play_Wright_bs(url)
    if title and content and len(content) > 10 and check_page_content(title):
        print(4, flush=True)
        return title, content
    
    wrong = read_content(wrong_path)
    wrong.append({"url": url, "source_url": source_url})
    save_content(wrong, wrong_path)
    return None, None

def main():
    crawl(url, "http://www.sample.com/")
    
if __name__ == '__main__':
    main()
