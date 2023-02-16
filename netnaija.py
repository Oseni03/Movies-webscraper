import requests, re, json, csv
from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque
from requests import RequestException
from requests.exceptions import HTTPError
from requests.exceptions import InvalidURL


queue = deque()
links = set()
def netnaija_pages(url):
  global links
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
  except RequestException as e:
    print(e)
  else:
    nexts = soup.find("div", class_="row my-3")
    pages = nexts.find_all("a", class_="page-numbers")
    for page in pages:
      ll = page.get("href")
      #print(ll)
      if ll not in links:
        links.add(ll)
  if links:
    print(links)
    links.add(netnaija_pages(links.pop()))
  return links


def netnaija_movie_links(url):
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
  except RequestException as e:
    print(e)
  else:
    links = []
    
    articles = soup.find_all("article", class_="file-one shadow")
    for article in articles:
      url = article.find("div", class_="info").a.get("href")
      if url not in links:
        links.append(url)
        print(url)
  return links
          
          
def netnaija_movies(url):
  try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
  except RequestException as e:
    print(e)
  else:
    article = soup.find("article", class_="post-body")
    
    img = article.figure.img.get("src")
    url = article.find("div", class_="post-meta")
    try:
      description = article.find_all("p")[:2]
      description = description[0].text + description[1].text 
    except:
      description = article.find_all("p")[0].text 
    try:
      director = article.find_all("p")[1].text 
    except:
      director = article.find_all("p")[1].text.split("\n")[0].split(": ")[-1]
    name = soup.find("h1").text 
    try:
      genres = article.find_all("p")[3].text.split(", ")
    except:
      genres = article.find_all("p")[1].text.split("\n")[3].split(": ")[-1].split(" | ")
    for idx, genre in enumerate(genres):
      if genre.startswith("Genre"):
        genres[idx] = genre.replace("Genre: ", "")
    try:
      date = article.find_all("p")[4].text
      date = date.replace("Release Date: ", "").replace(str(re.compile("[\(A-Za-z*\)+]")), "")
    except:
      date = soup.find_all("div", class_="post-meta")[0].find_all("span")[1].text.replace("\n", "")
    try:
      actors = article.find_all("p")[5].text.split(", ")
      for idx, actor in enumerate(actors):
        if actor.startswith("Star"):
          actors[idx] = actor.replace("Stars: ", "")
    except:
      actors = article.find_all("p")[1].text.split("\n")[2].split(": ")[-1].split(", ")
    movie_download = article.find("div", class_="download-block-con").div.div.a.get("href")
    if movie_download.startswith("/"):
      movie_download = str(url) + str(movie_download)
    subtitle_download = article.find("div", class_="db-one").a.get("href")
    if subtitle_download.startswith("/"):
      subtitle_download = url+subtitle_download
    
    #print(f"Name: {name},\nImage: {img},\ngenre: {genres},\ndate: {date},\nactors: {actors},\ndescription: {description}, \nmovie_download: {movie_download}, \nsub_download: {subtitle_download}")
    
    movie = {
      "Name": name,
      "Date_Created": date,
      "Image": img,
      "Genre": genres,
      "Director": director,
      "Description": description,
      "Actors": actors,
      "Movie_download": movie_download,
      "Subtitle_download": subtitle_download
    }
    print(movie)
    # with open("netnaija_movies.json", "a") as file:
    #   json.dump(movie, file)
    
    
def netnaija_scraper(url):
  pages = netnaija_pages(url)
  for link in pages:
    movie_links = netnaija_movie_links(link)
    for link in movie_links:
      netnaija_movies(link)
      
      
# def videos(url):
#   try:
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#   except RequestException as e:
#     print(e)
#   else:
    
      
      
      
if __name__=="__main__":
  print(netnaija_movies("https://www.thenetnaija.co/videos/movies/16344-the-unbearable-weight-of-massive-talent-2022"))