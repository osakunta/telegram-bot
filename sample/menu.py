import requests
from bs4 import BeautifulSoup


def get_todays_menu():
    url = 'https://hys.net/osakuntabaari/ruokalista/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    todays_list = soup.find("div", {"class": "row-today"})

    date = todays_list.find("div", {"class": "col-day"}).p.get_text().capitalize()
    food = todays_list.find("div", {"class": "col-food"}).p.get_text()

    return '*{}*\n{}'.format(date, food)
