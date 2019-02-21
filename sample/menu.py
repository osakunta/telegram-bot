import requests
from bs4 import BeautifulSoup


def __get_menu():
    url = 'https://hys.net/osakuntabaari/ruokalista/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    todays_list = soup.find("div", {"class": "lunch"})

    return todays_list


def __format_list(days_list):
    date = days_list.find("div", {"class": "col-day"}).p.get_text().capitalize()
    food = days_list.find("div", {"class": "col-food"}).p.get_text()

    return '*{}*\n{}'.format(date, food)


def get_todays_menu():
    todays_list = __get_menu().find("div", {"class": "row-today"})

    return __format_list(todays_list)


def get_weeks_menu():
    weeks_list = __get_menu().find_all("div", {"class": "row"})
    formatted_list = ''

    for days_list in weeks_list:
        formatted_list += __format_list(days_list)
        formatted_list += '\n'

    return formatted_list
