from datetime import datetime
import os
import json
import requests
from utils import extract_domain

def post(url):
    post_websites = get_post_websites()
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"data/articles/{folder_name}/"
    article_path = folder_path + extract_domain(url) + '.json'

    if os.path.exists(article_path):
        with open(article_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        post_url = "http://10.80.76.4:5000/site"

        for website in post_websites:
            if website["url"] == url:
                post_url = f"{post_url}/{website['id']}"
                break
        post_url = post_url + "/page"
        # print(f"Posting to {post_url}")

        for content in data:
            response = requests.post(post_url, json=content)
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

def get_post_websites():
    return 0

def main():
    print("Posting articles...")

if __name__ == "__main__":
    main()