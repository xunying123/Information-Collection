from src.utils import read_content, logging
from src.perception import preception
from src.data import get_post_websites, get_keywords
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def do(web):
    preception(web)

def run():
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")

    folder_path = f"./src/data/out/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    path = f"./src/data/out/{folder_name}/run.txt"  
    logging(path, "Start! ")
    get_post_websites()
    get_keywords()
    post_websites = read_content("./src/data/post_websites.json")
    
    def safe_do(web):
        try:
            do(web)
        except Exception as e:
            logging(path, "Error! ")
            logging(path, str(e))
            logging(path, web['url'][0])

    max_workers = 5
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(safe_do, web) for web in reversed(post_websites)]
        for _ in as_completed(futures):
            pass
    
    # for web in reversed(post_websites):
    #     try:
    #         do(web)
    #     except Exception as e:
    #         logging(path, "Error! ")
    #         logging(path, str(e))
    #         logging(path, web['url'][0])

def main():
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    execution_time = (end_time - start_time)
    current_date = datetime.now()
    folder_name = current_date.strftime("%Y-%m-%d")
    path = f"./src/data/out/{folder_name}/run.txt"  
    logging(path, "End! ")
    logging(path, f"Execution time: {execution_time}")
    
if __name__ == '__main__':
    main()