import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def get_todays_menu():
    url = 'https://hys.net/osakuntabaari/ruokalista/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    todays_list = soup.find("div", {"class": "row-today"})

    date = todays_list.find("div", {"class": "col-day"}).p.get_text().capitalize()
    food = todays_list.find("div", {"class": "col-food"}).p.get_text()

    return '*{}*\n{}'.format(date, food)


def send_todays_menu():
    token = os.getenv('TOKEN')
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    chat_id = os.getenv('CHAT_ID')
    text = get_todays_menu()
    data = {'chat_id': chat_id, 'text': str(text), 'parse_mode': 'markdown'}

    requests.post(url=url, data=data).json()


load_dotenv()
send_todays_menu()
