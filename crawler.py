import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

URLs = []
SAVE_AFTER = 100 # Save values after x entries
MAX_DEPTH = 100
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4891.91 Safari/537.36'}


def remove_duplicates(url_list:list):
    return list(dict.fromkeys(url_list))
    

def strip_url(input_url):
    separator = "://"
    return str(urlparse(input_url).scheme + separator + urlparse(input_url).netloc)

def valid(test_url):
    if validators.url(test_url):
        return True
    return False

def get_urls(html:str):
    parser = BeautifulSoup(html,"html.parser")
    a_tags = parser.find_all('a')
    output_list = list()
    for item in a_tags:
        try:
            href = str(item['href'])
            if valid(href):
                output_list.append(href)
        except:
            pass
    return output_list

def get_site_html(url:str):
    if valid(url):
        return str(requests.get(url,headers=user_agent).text)
    return False

def crawl(url:str,save_after:int,depth:int=1):
    print("depth:",depth)
    print()
    global URLs
    if depth > MAX_DEPTH: # RECURSIVE STOP
        return
    if len(URLs) >= save_after: # SAVE VALUES TO FILE
        save_urls_list = list()
        for url in URLs:
            save_urls_list.append(strip_url(url))
        print("removing duplicates")
        save_urls_list = remove_duplicates(save_urls_list)
        print("saving..")
        output_file_path = "entries.dat"
        output_file = open(output_file_path,"a")
        for url in save_urls_list:
            output_file.write(strip_url(url))
            output_file.write("\n")
        output_file.close()
        URLs = []
        print("saved.")
        print()

    urls = get_urls(get_site_html(url))
    if urls: # if there are URLS found
        for url in urls: # save urls
            URLs.append(url)
        for url in urls: # crawl urls
            crawl(url,save_after,depth+1)
    return False

start_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
crawl(start_url,SAVE_AFTER)

