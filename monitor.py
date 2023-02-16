from bs4 import BeautifulSoup
from requests_html import HTMLSession

import random
import json

UA_STRINGS = [
  "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36\
      (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36\
      (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15\
      (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
]


def get_page(url, filename):
    HEADERS = {
        'User-Agent': random.choice(UA_STRINGS),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    s = HTMLSession()
    r = s.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
      with open(f"{filename}.html", "w") as file:
        file.write(str(soup.prettify()))
    except:
      with open(f"{filename}.html", "w") as file:
        file.write(r.text)
    return "Done"


def get_api(url, filename):
    HEADERS = {
        'User-Agent': random.choice(UA_STRINGS),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    s = HTMLSession()
    resp = s.get(url, headers=HEADERS)
    print(dir(resp))
    with open(f"{filename}.json", "w") as file:
      json.dump(resp.json(), file)
    print("done")
  
  
# print(get_page("https://www.boxofficemojo.com/calendar/2023-05-01/", "boxofficemojo"))

# print(get_page("https://www.metacritic.com/browse/movies/release-date/coming-soon/date?page=1", "metacritic_movies"))

# print(get_page("https://www.metacritic.com/feature/tv-premiere-dates?page=1", "metacritic_series"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/ps5/date", "ps5_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/ps4/date", "ps4_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/xbox-series-x/date", "x_box_series_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/xboxone/date", "xboxone_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/switch/date?page=1", "switch_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/coming-soon/pc/date?page=3", "pc_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/new-releases/all/date", "new_released_games"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/new-releases/ps5/date?view=detailed&page=3", "ps5_new_release"))

# print(get_page("https://www.metacritic.com/browse/games/release-date/new-releases/ps4/date?page=2", "ps4_new_release"))

# print(get_page("https://www.ign.com/upcoming/games/ps4", "ign_ps4"))

# print(get_page("https://www.ign.com/upcoming/games/nintendo-switch", "ign_switch"))

print(get_page("https://www.moviefone.com/new-movie-releases/?page=2", "theater_movies"))

print(get_page("https://www.moviefone.com/feeds/what-to-watch.rss", "what-to-watch"))

print(get_page("https://www.moviefone.com/feeds/movie-trailers.rss", "movie-trailers"))

print(get_page("https://www.moviefone.com/streaming-movies/?page=2", "streaming-movies"))

print(get_page("https://www.moviefone.com/places/", "showtimes_places"))

print(get_page("https://www.moviefone.com/places/los-angeles-california/canoga-park/?page=2", "showtimes_schedule"))