import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot import today, week, janitor

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher

today_handler = CommandHandler('h', today)
week_handler = CommandHandler('hv', week)
janitor_handler = CommandHandler('huolto', janitor)

dispatcher.add_handler(today_handler)
dispatcher.add_handler(week_handler)
dispatcher.add_handler(janitor_handler)

updater.start_polling()
