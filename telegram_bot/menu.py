import requests
from bs4 import BeautifulSoup
import logging


def __get_menu():
    url = 'https://hys.net/osakuntabaari/ruokalista/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    todays_list = soup.find("div", {"class": "lunch"})

    return todays_list

# If the menu is not available, check for any status message
# Usually happens during the summer break
def __get_status():
    url = 'https://hys.net/osakuntabaari/ruokalista/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    status_message = soup.find("div", {"class": "widget-lunch"}).p.get_text()

    return status_message


def __with_header(header, body):
    return '*{}*\n{}'.format(header, body)


def __format_list(days_list):
    date = days_list.find("div", {"class": "col-day"}).p.get_text().capitalize()
    food = days_list.find("div", {"class": "col-food"}).p.get_text()

    return __with_header(date, food)


def get_todays_menu():
    try:
        menu = __get_menu()
        todays_list = __get_menu().find("div", {"class": "row-today"})
        formatted_list = __format_list(todays_list)
        return __with_header('Hämiksen ruokalista', formatted_list)
    except Exception as e:
        logging.error(f"Error fetching today's menu: {e}")
        return __get_status()



def get_weeks_menu():
    menu = __get_menu()
    if menu:
        weeks_list = __get_menu().find_all("div", {"class": "row"})
        formatted_list = ''

        for days_list in weeks_list:
            formatted_list += __format_list(days_list)
            formatted_list += '\n'

        return __with_header('Hämiksen ruokalista', formatted_list)
    else:
        return __get_status()
