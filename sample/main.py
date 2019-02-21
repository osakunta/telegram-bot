import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot import start

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)
updater.start_polling()
