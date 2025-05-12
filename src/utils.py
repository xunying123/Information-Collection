import re
import json
import os
from src.LLM.model import Model
from src.LLM.run import summary, translate, get_keywords, get_score
from src.data import get_keywords_map_from_db
import requests
from urllib.parse import urlparse, urlunparse

cookie = "HSID=AMaXiW-mKafze-IIs; SSID=A_ZmnTiS1rJFe09Lg; APISID=gCnWRnrS8tIxdkOA/ACnF5b_50tQ6hPHaN; SAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; __Secure-1PAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; __Secure-3PAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; SEARCH_SAMESITE=CgQI0JoB; receive-cookie-deprecation=1; SID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetwdm8T4ox3UAGSiR1BSBq-AgACgYKAaoSAQASFQHGX2Mi-xPoei5MGIAXEPwoxohqeRoVAUF8yKoNnktrkf-yY6ceaSpAc04q0076; __Secure-1PSID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetw8c16mKIPvpb3x_pqDBHZAwACgYKAV8SAQASFQHGX2MiR_uZym0V_kS6jzYOXiz9xRoVAUF8yKooyNAZ_IhL_TKJz8yCq7ge0076; __Secure-3PSID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetwKB_JULP4AYAbnqA9aQZVZgACgYKAeoSAQASFQHGX2MiwW0JaLwL4SjiUSYvJrtXnRoVAUF8yKoJLx7rCeinp85Vyu60YNR90076; __Secure-1PSIDTS=sidts-CjIB4E2dkZKzPpjBTOm9BIr6QfoYqeVqpRKuMB-sghX432OH4lsO2Osly8K5nO5dzXlPrRAA; __Secure-3PSIDTS=sidts-CjIB4E2dkZKzPpjBTOm9BIr6QfoYqeVqpRKuMB-sghX432OH4lsO2Osly8K5nO5dzXlPrRAA; AEC=AVYB7cruur-ev21GM7lrDELf1PTkKqqiJYYjf4vm52tQBg7PXc7f3-XTBcc; OTZ=7674257_24_24__24_; NID=516=rLsbFnlAS4dIjTE7RGunFnRYe4g2ESkpLxb8ZRIsxG1yYHzjgsZCGb_xJEWOlVMII1aJenSc51kQZjQZ5U8NozDS5e8AK3r2cwUbxJS6g6VRG7_UMBUW6tJKc2F9tqoLBL16hJc2f8_O_tWnaWvdCbzebYKcq3oL5OsKpDa-exEtVzyRU0WWnhRZ3ybQZVkmclGQLmim9WP6zqlV4MReyp2VXJZXMu38DlplcqcXYdDkymFFkhmQo-H8vC1JkJxtWgvvfYh3PaMA4AiwY5yr5Gm-0fOImy4Sp-OcxmHD1k0mrQLMeqK041-JOF4nO0bfeI6YAyF_2Wb7ues9KCA1OKZ_j2WJ0thW-V86O5zaoRS-CMsSEADxdpXJa95I7dY2EBjKcEZAGqD1rKa_PIs; SIDCC=AKEyXzVlk8N1sOX6wRtc9xu-hj49rLfPh3mUb2qbOHFwDpN6rDFfq-vmdatcSIcpIL2WN7XBlnw; __Secure-1PSIDCC=AKEyXzVvXT7_zT4Wdb5B3rFNeIcJFOYSjBt59s4-HgRQSI_9Z0rQVTzg8yVXH02xSbG2AxsE0Q; __Secure-3PSIDCC=AKEyXzXuj0PVL1Nvq8O71UMHs02pxA0LDADRirBXUIzL6R1xRtr6Vh2q8QnlMPJYog6QJN1gVQ"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'cookie': cookie
}

deepseek = Model("deepseek-v3")
keyword_map = get_keywords_map_from_db()

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
    sanitized_url = re.sub(r'[^a-zA-Z0-9\-]', '-', url)
    return sanitized_url

def save_content(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def read_content(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def check_page_content(page_content):
    if "Not Found" in page_content or "Page Not Found" in page_content or "File not found" in page_content :
        return 0;
    elif "The URL you requested has been blocked" in page_content or "您所请求的网址已被屏蔽" in page_content or "Not Acceptable" in page_content or "403 禁止访问" in page_content or "403 Forbidden" in page_content or "身份认证系统" in page_content:
        return 1;
    elif "LLM(Large Languate Model) error" in page_content or "好的，请提供英文标题" in page_content :
         return 2;
    else:
        return 3;

def summary_(content):
    if len(content) > 16000:
        new = content[:16000]
    else:
        new = content
    if bool(re.search(r'[\u4e00-\u9fff]', new)):
        if len(content) > 400:
               return summary(deepseek, new)
        else:
                return new
    else:
        temp = translate(deepseek, new)
        if len(temp) > 400:
                return summary(deepseek, temp)
        else:
                return temp
                             
def title_(title):
    if bool(re.search(r'[\u4e00-\u9fff]', title)):
        return title
    else:
        return translate(deepseek, title)

    
def check_(url):
    if "mp.weixin.qq.com" in url or "weibo.com" in url or "www.princeton.edu/events" in url:
           return 1
    else:
           return 0

def what_word(content):
    keyword_set = set()
    for _ in range(3):
        keywords = get_keywords(deepseek, content)
        if len(keyword_set) == 0:
            keyword_set = set(keywords)
        else:
            keyword_set = keyword_set.intersection(set(keywords))
    return list(keyword_set)

def what_score(content):
    return get_score(deepseek, content)

def get_keywords_id(content):
    return [keyword_map[k] for k in content if k in keyword_map]

def logging(path, content):
    with open(path, 'a') as f:
        f.write(content + '\n')
        f.close()
        
def wash_url(url):
    resp = requests.get(url, timeout=10)
    p = urlparse(resp.url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    if scheme == 'http' and netloc.endswith(':80'):
        netloc = netloc[:-3]
    if scheme == 'https' and netloc.endswith(':443'):
        netloc = netloc[:-4]
    path = (p.path or '/').rstrip('/') or '/'
    return urlunparse((scheme, netloc, path, '', p.query, ''))

