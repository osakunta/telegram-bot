import os
import requests
from menu import get_todays_menu
from dotenv import load_dotenv


def send_todays_menu():
    token = os.getenv('TOKEN')
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    chat_id = os.getenv('CHAT_ID')
    text = get_todays_menu()
    data = {'chat_id': chat_id, 'text': str(text), 'parse_mode': 'markdown'}

    requests.post(url=url, data=data).json()

load_dotenv()
send_todays_menu()
