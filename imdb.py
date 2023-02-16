import asyncio
# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging
import json
from urllib.parse import urljoin

# logging.basicConfig(
#   filename="imdb.log", 
#   level=logging.DEBUG, 
#   format="%(asctime)s - %(message)", 
#   datefmt="%d-%b-%y %H:%M:%S")

type_codes = ["MOVIE", "TV", "TV_EPISODE"]


def get_regions(page):
    soup = BeautifulSoup(page, "lxml")
    options = soup.select("select[id='country-selector'] option")
    regions = [{"country": option.get_text(strip=True), "code": option.get("value")} for option in options]
    with open(f"regions.json", "w") as file:
      json.dump(regions, file, indent=4)
    return "done"


def get_type(page):
    url = "https://www.imdb.com"
    soup = BeautifulSoup(page, "lxml")
    items = soup.select("a.ipc-chip--on-base")
    typs = [{"type": item.span.text.strip(), "url": urljoin(url, item.get("href"))} for item in items]
    return typs
    

async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body
    
    
async def get_pages():
    tasks = []
  
    async with ClientSession() as session:
        num = 1
        while True:
            url = f"https://www.imdb.com/calendar/?ref_=rlm&region={region}&type={typ}"
            try:
                tasks.append(
                    asyncio.create_task(fetch(url, session))
                )
            except:
                break
            num += 1
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def parse_page(page):
    soup = BeautifulSoup(page, "html.parser")
    articles = soup.select("article[data-testid='calendar-section']")
    
    products = []
    
    for article in articles:
        date = article.select_one("div[data-testid='release-date'] h3").text.strip()
        movies = []
        
        items = article.select("li[data-testid='coming-soon-entry']")
        for item in items:
            title = item.select_one("div.ipc-metadata-list-summary-item__tc a").text.strip()
            try:
                image = item.select_one("div.ipc-poster__poster-image img").get("src")
            except:
                image = ""
            grs = item.select("div.ipc-metadata-list-summary-item__tc ul.ipc-metadata-list-summary-item__tl li")
            genres = [g.label.text.strip() for g in grs]
            cts = item.select("div.ipc-metadata-list-summary-item__tc ul.ipc-metadata-list-summary-item__stl li")
            casts = [c.label.text.strip() for c in cts]
            movies.append({
                "title": title,
                "image": image,
                "genres": genres,
                "casts": casts,
            })
        products.append({
            "date": date,
            "movies": movies,
        })
    return products


def save(products):
    pass


def main():
    pages = asyncio.run(get_pages())
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__=="__main__":
    with open("imdb_calender.html", "r") as file:
        print(parse_page(file.read()))
