import os
import logging
from telegram.ext import Updater, CommandHandler
from telegram_bot.bot import hamis_menu, janitor, janitor_form

def telegram_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token=os.getenv('TOKEN'))

    command_handlers = [
        CommandHandler('ruokalista', hamis_menu, pass_args=True),
        CommandHandler('huolto', janitor),
        CommandHandler('huoltoilmoitus', janitor_form),
    ]

    for handler in command_handlers:
        updater.dispatcher.add_handler(handler)

    updater.start_webhook()

if __name__ == '__main__':
    telegram_bot()
