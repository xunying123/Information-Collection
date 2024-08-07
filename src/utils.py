from goose3 import Goose
from goose3.text import StopWordsChinese
import tldextract
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from htmldate import find_date
import re

cookie = "HSID=AMaXiW-mKafze-IIs; SSID=A_ZmnTiS1rJFe09Lg; APISID=gCnWRnrS8tIxdkOA/ACnF5b_50tQ6hPHaN; SAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; __Secure-1PAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; __Secure-3PAPISID=9uTNvJkKuInp7EgO/A11lmhMkJpKD6Hm1O; SEARCH_SAMESITE=CgQI0JoB; receive-cookie-deprecation=1; SID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetwdm8T4ox3UAGSiR1BSBq-AgACgYKAaoSAQASFQHGX2Mi-xPoei5MGIAXEPwoxohqeRoVAUF8yKoNnktrkf-yY6ceaSpAc04q0076; __Secure-1PSID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetw8c16mKIPvpb3x_pqDBHZAwACgYKAV8SAQASFQHGX2MiR_uZym0V_kS6jzYOXiz9xRoVAUF8yKooyNAZ_IhL_TKJz8yCq7ge0076; __Secure-3PSID=g.a000mAgYeIk-jYtW-UjDZuO63M31Rh6f4TSGv8tliBxPFTjcIetwKB_JULP4AYAbnqA9aQZVZgACgYKAeoSAQASFQHGX2MiwW0JaLwL4SjiUSYvJrtXnRoVAUF8yKoJLx7rCeinp85Vyu60YNR90076; __Secure-1PSIDTS=sidts-CjIB4E2dkZKzPpjBTOm9BIr6QfoYqeVqpRKuMB-sghX432OH4lsO2Osly8K5nO5dzXlPrRAA; __Secure-3PSIDTS=sidts-CjIB4E2dkZKzPpjBTOm9BIr6QfoYqeVqpRKuMB-sghX432OH4lsO2Osly8K5nO5dzXlPrRAA; AEC=AVYB7cruur-ev21GM7lrDELf1PTkKqqiJYYjf4vm52tQBg7PXc7f3-XTBcc; OTZ=7674257_24_24__24_; NID=516=rLsbFnlAS4dIjTE7RGunFnRYe4g2ESkpLxb8ZRIsxG1yYHzjgsZCGb_xJEWOlVMII1aJenSc51kQZjQZ5U8NozDS5e8AK3r2cwUbxJS6g6VRG7_UMBUW6tJKc2F9tqoLBL16hJc2f8_O_tWnaWvdCbzebYKcq3oL5OsKpDa-exEtVzyRU0WWnhRZ3ybQZVkmclGQLmim9WP6zqlV4MReyp2VXJZXMu38DlplcqcXYdDkymFFkhmQo-H8vC1JkJxtWgvvfYh3PaMA4AiwY5yr5Gm-0fOImy4Sp-OcxmHD1k0mrQLMeqK041-JOF4nO0bfeI6YAyF_2Wb7ues9KCA1OKZ_j2WJ0thW-V86O5zaoRS-CMsSEADxdpXJa95I7dY2EBjKcEZAGqD1rKa_PIs; SIDCC=AKEyXzVlk8N1sOX6wRtc9xu-hj49rLfPh3mUb2qbOHFwDpN6rDFfq-vmdatcSIcpIL2WN7XBlnw; __Secure-1PSIDCC=AKEyXzVvXT7_zT4Wdb5B3rFNeIcJFOYSjBt59s4-HgRQSI_9Z0rQVTzg8yVXH02xSbG2AxsE0Q; __Secure-3PSIDCC=AKEyXzXuj0PVL1Nvq8O71UMHs02pxA0LDADRirBXUIzL6R1xRtr6Vh2q8QnlMPJYog6QJN1gVQ"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
}

def is_url(url):
        if not url:
                return False
        if not url.startswith('http'):
                return False
        return True

def is_ad(url):
        if 'qzshare' in url or 'share' in url or 'comment' in url or 'login' in url or 'register' in url:
                return True
        return False

def is_article(url):
        if not is_url(url):
                return False
        
def normalize_url(url):    
        match = re.search(r'click=(https?://[\w./-]+)', url)
        if match:
                return match.group(1)
        return url
        
        
        # g = Goose({'stopwords_class': StopWordsChinese})
        # article = g.extract(url=url)    
        
        # if len(article.cleaned_text) < 100:
        #         return False
            
        # if not article.title:
        #         return False        
        
        return True

def extract_domain(url):
        ext = tldextract.extract(url)
        # 组合域名和后缀，例如 moe.gov
        domain = f"{ext.domain}.{ext.suffix}"
        return domain

def get_date_by_google(url):
        search_url = f'https://www.google.com/search?q={url}&as_qdr=y15'        

        # 发送请求获取搜索结果页面
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # 解析HTML内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 获取第一个搜索结果的时间信息
        time_info = None
        target_span = soup.find('span', class_='LEwnzc Sqrs4e')

        # 提取该span中的所有span的内容
        if target_span:
                spans = target_span.find_all('span')
                for span in spans:
                        time_info = span.get_text()
                        if time_info:
                            break
                    
        if time_info:        
                if "天前" in time_info:
                        days_ago = int(time_info.replace("天前", ""))
                        publish_date = datetime.now() - timedelta(days=days_ago)
                elif "小时前" in time_info:
                        hours_ago = int(time_info.replace("小时前", ""))
                        publish_date = datetime.now() - timedelta(hours=hours_ago)
                elif "分钟前" in time_info:
                        minutes_ago = int(time_info.replace("分钟前", ""))
                        publish_date = datetime.now() - timedelta(minutes=minutes_ago)
                else:
                        publish_date = datetime.strptime(time_info, "%Y年%m月%d日")
                publish_date = publish_date.strftime('%Y-%m-%d')
                return publish_date
        else:
                return None
            
def get_date_by_meta(url):        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta = soup.find_all('meta')        
        for tag in meta:                
                if 'name' in tag.attrs and tag.attrs['name'].lower() in ['date', 'date_published', 'publish_date', 'publishdate']:
                        return tag.attrs['content']                
        return None
            
def get_date(url):
        publish_date = get_date_by_meta(url)
        if publish_date:
                return publish_date
        
        try:
                publish_date = find_date(url)
                if publish_date:
                        today = datetime.now()
                        if today - datetime.strptime(publish_date, '%Y-%m-%d') < timedelta(days=35):
                                return publish_date
        except ValueError as e:
                print(f"Error processing URL: {e}")
                publish_date = None                
                
        # try:        
        #         publish_date = get_date_by_google(url)
        #         if publish_date:
        #                 return publish_date
        # except Exception as e:
        #         print(f"Error processing URL: {e}")
        #         publish_date = None
        
        return None
        