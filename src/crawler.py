from goose3 import Goose
from goose3.text import StopWordsChinese
from lxml.etree import ParserError
from datetime import datetime
import json
import os
from newspaper import Article
import requests
from bs4 import BeautifulSoup

url = 'https://www.gov.cn/zhengce/content/202408/content_6968086.htm'

def save_content(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def read_content(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def Newspaper(url):
    try:
        article = Article(url, language='zh')
        article.download()
        article.parse()
        if article.text and len(article.text) > 50:
            return article.title, article.text
    except Exception as e:
        return None, None
    return None, None

def Goose(url):
    try:
        g = Goose({'stopwords_class': StopWordsChinese})
        article = g.extract(url=url)
        if article.cleaned_text and len(article.cleaned_text) > 50:
            return article.title, article.cleaned_text
    except Exception as e:
        return None, None
    return None, None

def BeautifulSoup(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text
        content = soup.find('div', class_='pages_content').text
        if content and len(content) > 50:
            return title, content
    except Exception as e:
        return None, None
    return None, None

def crawl(url):
    print(f"Fetching {url}")
    today_date = datetime.today().strftime('%Y-%m-%d')
    wrong_path = "data/wrong/" + today_date + '.json'

    title, content = Newspaper(url)
    if title and content:
        print(1)
        return title, content
    
    title, content = Goose(url)
    if title and content:
        print(2)
        return title, content
    
    title, content = BeautifulSoup(url)
    if title and content:
        print(3)
        return title, content
    
    wrong = read_content(wrong_path)
    wrong.append(url)
    save_content(wrong, wrong_path)
    return None, None

def main():
    crawl(url)
    
if __name__ == '__main__':
    main()