from utils import read_content
from perception import preception
from post import post
import os
from datetime import datetime

def run():
    websites = read_content("data/websites.json")
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"data/articles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    for links in websites:
        preception(links)
        post(links)

def main():
    run()
    
if __name__ == '__main__':
    main()