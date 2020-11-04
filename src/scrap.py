import re
import requests
from requests import HTTPError, Timeout, ConnectionError
from bs4 import BeautifulSoup
from multiprocessing import Process
from database import *


def step(current_url, father_url):
    if check_if_been_crawled(current_url) > 0:
        return
    try:
        page = requests.get(current_url)
        if page.status_code == 200:
            data = page.text
            soup = BeautifulSoup(data, features="html.parser")
            links = []
            for link in soup.find_all(attrs={'href': re.compile("http")}):
                links.append(link.get('href'))
            create_new_link_model(current_url, page.status_code, links, father_url)
            for link in set(links):
                procs = []
                proc = Process(target=step, args=(link, current_url))
                proc.start()
            for proc in procs:
                proc.join()
        else:
            create_new_link_model(current_url, page.status_code, None, father_url)
    except (HTTPError, Timeout, ConnectionError):
        create_new_link_model(current_url, 404, None, father_url, error='Fail to get url')
        return
