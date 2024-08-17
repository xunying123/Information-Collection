from goose3 import Goose
from goose3.text import StopWordsChinese

url = 'https://www.ustc.edu.cn/info/1362/21895.htm'

def crawl(url):
    # response = requests.get(url, headers=headers)
    # print(date)
    # print(today)
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    # print(article.title)
    # print(article.cleaned_text)
    return article.title, article.cleaned_text
        
def main():
    crawl(url)
    
if __name__ == '__main__':
    main()