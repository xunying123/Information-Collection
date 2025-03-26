from utils import read_content
from perception import preception
from data import get_post_websites
import os
from datetime import datetime
import sys

def do(web):
    preception(web)

def run():
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")

    folder_path = f"./src/data/out/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    path = f"./src/data/out/{folder_name}/run.txt"  
    
    with open(path, 'a') as f:
        f.write("Start! ")
        sys.stdout = f
        get_post_websites()
        post_websites = read_content("./src/data/post_websites.json")
        f.close()

    for web in reversed(post_websites):
        try:
            do(web)
        except:
            with open(path, 'a') as f:
                f.write(web)
                f.write("\n")
                f.write("byd sb web\n")
                f.close()

def main():
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    execution_time = (end_time - start_time)
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    path = f"./src/data/out/{folder_name}/run.txt"  
    with open(path, 'a') as f:
        f.write(str(execution_time))
    
if __name__ == '__main__':
    main()