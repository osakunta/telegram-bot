import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot import start, today

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
today_handler = CommandHandler('today', today)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(today_handler)

updater.start_polling()
