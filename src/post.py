from datetime import datetime
import os
import json
import requests
from utils import extract_domain
from utils import read_content, save_content
from perception import add_website
import asyncio

log_url = "http://10.119.12.91/api/login"

user = {
            "username": "wushuo123",
            "password": "u91dFZWwQpGvWQZC"
}

def post(url):
    post_websites = read_content("/home/dic/Information-Collection/src/data/post_websites.json")
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"/home/dic/Information-Collection/src/data/articles/{folder_name}/"
    article_path = folder_path + extract_domain(url) + '.json'

    if os.path.exists(article_path):
        with open(article_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        post_url = "http://10.119.12.91/api/site"

        for website in post_websites:
            if website["url"] == url:
                post_url = f"{post_url}/{website['id']}"
                break
        post_url = post_url + "/page"

        login_cookies = requests.post(log_url, json=user)

        for content in data:
            response = requests.post(post_url, json=content, cookies=login_cookies.cookies)
            print(f"Status Code: {response.status_code}", flush=True)
            print(f"Response Text: {response.text}", flush=True)


def get_post_websites():
    login_cookies = requests.post(log_url, json=user)
    response = requests.get('http://10.119.12.91/api/site', cookies=login_cookies.cookies)
    data = response.json()
    new_urls = [item['url'] for item in data]
    old_urls = read_content("/home/dic/Information-Collection/src/data/websites.json")

    new_unique_urls = [url for url in new_urls if url not in old_urls]

    for links in new_unique_urls:
        try:
            add_website(links)
        except Exception as e:
            print(f"Error: {links}", flush=True)
            new_urls.remove(links)
            continue

    save_content(new_urls, "/home/dic/Information-Collection/src/data/websites.json")
    save_content(data, "/home/dic/Information-Collection/src/data/post_websites.json")

def main():
    print("Posting articles...", flush=True)

if __name__ == "__main__":
    main()