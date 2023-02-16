import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from urllib.request import urlopen

url = "https://tubitv.com/home"
r = urlopen(url)
soup = BeautifulSoup(r, "html.parser")
contents = soup.find_all("div", class_="Container HvEKt")
for content in contents:
  category = content.text
  link = urljoin(url, content.a.get("href"))
  meat = BeautifulSoup(urlopen(link), "html.parser")
  
  print(f"{category}: {link}")