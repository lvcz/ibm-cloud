import re
import requests
from requests import HTTPError, Timeout, ConnectionError
from bs4 import BeautifulSoup
from multiprocessing import Process
from database import save_url, was_crawled
from http import HTTPStatus


def step(current_url, parent_url):
    if was_crawled(current_url):
        return
    try:
        page = requests.get(current_url)
        if page.status_code == HTTPStatus.OK:
            html_content = page.text
            links = extract_urls(html_content)
            save_url(current_url, page.status_code, parent_url)
            step_children(current_url, links)
    except HTTPError as e:
        save_url(current_url, e.response.status_code, parent_url, error='Failed to crawl url')
    except (Timeout, ConnectionError) as e:
        # Log exception. Perhaps retry
        return


def extract_urls(html):
    soup = BeautifulSoup(html, features="html.parser")
    links = []
    for link in soup.find_all(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
    return links


def step_children(parent_url, links):
    for link in set(links):
        procs = []
        proc = Process(target=step, args=(link, parent_url))
        proc.start()
    for proc in procs:
        proc.join()
