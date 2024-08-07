from bs4 import BeautifulSoup
import requests
from htmldate import find_date
from utils import get_date_by_meta, get_date_by_google, headers
from goose3 import Goose
from goose3.text import StopWordsChinese
from datetime import datetime

url = 'https://www.ustc.edu.cn/info/1362/21807.htm'

def crawl(url):
    response = requests.get(url, headers=headers)
    date = find_date(response.text)
    today = datetime.now().strftime('%Y-%m-%d')
    print(date)
    print(today)
    if date == today:
        g = Goose({'stopwords_class': StopWordsChinese})
        article = g.extract(url=url)
        print(article.title)
        print(article.cleaned_text)
    else:
        print('Not today')
        
def main():
    crawl(url)
    
if __name__ == '__main__':
    main()