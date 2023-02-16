import asyncio
from requests_html import HTMLSession
# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(
  filename="slot.log", 
  level=logging.DEBUG, 
  format="%(asctime)s - %(message)", 
  datefmt="%d-%b-%y %H:%M:%S")

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
    
    contents = []
    
    tables = soup.select("table.listtable.linedtable")

    for table in tables:
        headers = table.select("tr.sublistbig")
        for header in headers:
            date = header.text.strip()
            
            series = []
            
            sibling = header.next_sibling
            while sibling is not None:
                if sibling not in headers:
                    try:
                        title = sibling.select("td")[1].text.strip().replace("\n", "")
                        image = sibling.select("td")[1].select_one("img").get("src")
                        genre = sibling.select("td")[2].text.strip()
                        # url = title = sibling.select("td")[1].a.get("href")
                        
                        series.append({
                            "title": title,
                            "image": image,
                            "genre": genre
                        })
                    except:
                        pass
                    sibling = sibling.next_sibling
                else:
                    break
            contents.append({"date": date, "series":series})
                
        
    return contents


def save(products):
    pass


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__=="__main__":
    with open("metacritic_series.html", "r") as file:
        print(parse_page(file.read()))
