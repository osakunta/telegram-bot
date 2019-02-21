import requests
from bs4 import BeautifulSoup

url = 'https://hys.net/osakuntabaari/ruokalista/'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
food_today = soup.find("div", {"class": "row-today"})

print(food_today)
