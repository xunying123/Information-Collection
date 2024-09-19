from utils import read_content
from perception import preception
from post import post, get_post_websites
import os
from datetime import datetime
import sys

def run():
    get_post_websites()
    websites = read_content("/home/dic/Information-Collection/src/data/websites.json")
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"/home/dic/Information-Collection/src/data/articles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    
    for links in reversed(websites):
        preception(links)
        post(links)


def main():
    current_date = datetime.now()
    start_time = datetime.now()
    name = current_date.strftime("%Y-%m-%d")
    path = f"/home/dic/Information-Collection/src/data/out/{name}.txt"  
    with open(path, 'w') as f:
        sys.stdout = f
        run()
        end_time = datetime.now()
        execution_time = (end_time - start_time)
        print(execution_time, flush=True)
    
if __name__ == '__main__':
    main()
