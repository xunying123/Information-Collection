from links import websites
from perception import preception

def run():
    for links in websites:
        preception(links)


def main():
    run()
    
if __name__ == '__main__':
    main()