from utils import read_content, extract_domain
from perception import preception
from post import post, get_post_websites
import os
from datetime import datetime
import sys
from concurrent.futures import ThreadPoolExecutor

def do(url):
    preception(url)
    post(url)


def run():
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    folder_path = f"/home/dic/Information-Collection/src/data/articles/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    folder_path = f"/home/dic/Information-Collection/src/data/out/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    folder_path = f"/home/dic/Information-Collection/src/data/wrong/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    path = f"/home/dic/Information-Collection/src/data/out/time/{folder_name}.txt"  
    
    with open(path, 'a') as f:
        f.write("Start! ")
        sys.stdout = f
        get_post_websites()
        websites = read_content("/home/dic/Information-Collection/src/data/websites.json")
        f.close()

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     executor.map(do, reversed(websites))

    for links in reversed(websites):
        try:
            do(links)
        except:
            with open(path, 'a') as f:
                f.write(links)
                f.write("           byd sb web")
                f.write("\n")
                f.close()



def main():
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    execution_time = (end_time - start_time)
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    path = f"/home/dic/Information-Collection/src/data/out/time/{folder_name}.txt"  
    with open(path, 'a') as f:
        f.write(str(execution_time))
    
if __name__ == '__main__':
    main()