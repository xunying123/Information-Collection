import tldextract
import re
import json
import os
from GeneralAgent import Agent

cookie = ""
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
}

Api_key = ''
Base_url = ''
Model = ''

def is_ad(url):
        if 'qzshare' in url or 'login' in url or 'register' in url:
                return True
        return False
        
def normalize_url(url):    
        match = re.search(r'click=(https?://[\w./-]+)', url)
        if match:
                return match.group(1)
        return url

def extract_domain(url):
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        return domain

def save_content(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def read_content(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def check_page_content(page_content):
    if "Not Found" in page_content or "Page Not Found" in page_content or "File not found" in page_content or "The URL you requested has been blocked" in page_content or "您所请求的网址已被屏蔽" in page_content or "Not Acceptable" in page_content:
        return 0;
    else:
        return 1;


def summary_(content):
    if len(content) > 2000:
        new = content[:2000]
    else:
        new = content
    Summary = Agent('下面会给你一篇中文文章，我需要你对它进行内容总结，使得最终得到的总结长度在400字左右', hide_python_code=True, api_key=Api_key, model=Model, base_url=Base_url)
    if bool(re.search(r'[\u4e00-\u9fff]', new)):
        if len(content) > 600:
               
               return Summary.run(new)
        else:
                return new
    else:
        Translate_content = Agent('下面会给你一个英文文章，请你逐字的把它翻译成中文，我只要翻译好的结果，不要加任何前缀', hide_python_code=True, api_key=Api_key, model=Model, base_url=Base_url)
        temp = Translate_content.run(new)
        if len(temp) > 600:
                return Summary.run(temp)
        else:
                return temp
                             
def title_(title):
    if bool(re.search(r'[\u4e00-\u9fff]', title)):
        return title
    else:
        Translate_title = Agent('下面会给你一个英文标题，请把它翻译成中文，我只要翻译好的结果，不要加任何前缀', hide_python_code=True, api_key=Api_key, model=Model, base_url=Base_url)
        return (Translate_title.run(title)).split(":", 1)[-1]

    
def check_(url):
    if "mp.weixin.qq.com" in url or "weibo.com" in url or "www.princeton.edu/events" in url:
           return 1
    else:
           return 0
