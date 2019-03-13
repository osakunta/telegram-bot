import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot import hamis_menu, janitor

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=os.getenv('TOKEN'))
dispatcher = updater.dispatcher

command_handlers = [
    CommandHandler('ruokalista', hamis_menu, pass_args=True),
    CommandHandler('huolto', janitor)
]

for handler in command_handlers:
    dispatcher.add_handler(handler)

updater.start_polling()
