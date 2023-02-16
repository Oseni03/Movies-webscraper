import asyncio
from requests_html import HTMLSession
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging

# logging.basicConfig(
#   filename="metametric.log", 
#   level=logging.DEBUG, 
#   format="%(asctime)s - %(message)", 
#   datefmt="%d-%b-%y %H:%M:%S")

async def fetch(url, session):
  async with session.get(url) as resp:
    html_body = await resp.read()
    return html_body
    
    
async def get_pages(search_word):
    tasks = []
  
    async with ClientSession() as session:
        num = 1
        while True:
            url = f"https://slot.ng/catalogsearch/result/index/?p={num}&q={search_word}"
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
    items = soup.select("div.products div.item")
    
    products = []
    
    for item in items:
        image = item.select_one("div.img-wrap img").get("src")
        title = item.select_one("div.mid div.title").text.strip()
        url = item.select_one("a").get("href")
        release_date = item.select_one("div.release_date").text
        summary = item.select_one("div.product_summary").text
        
        products.append({
            "title": title,
            "image": image,
            "release_date": release_date,
            "summary": summary,
            "url": url,
        })
    return products


def save(products):
    pass


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__=="__main__":
    with open("metacritic_movies.html", "r") as file:
        print(parse_page(file.read()))
