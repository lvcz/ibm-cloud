import re
import requests
from bs4 import BeautifulSoup


url = "http://stackoverflow.com/"
page = requests.get(url)
data = page.text
soup = BeautifulSoup(data)
soup = BeautifulSoup(data, features="html.parser")
links = []

for link in soup.find_all(attrs={'href': re.compile("http")}):
    links.append(link.get('href'))

print(links)