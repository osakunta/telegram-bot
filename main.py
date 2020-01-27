import os
import logging
import telegram
from telegram.ext import Updater, CommandHandler
from telegram_bot.bot import hamis_menu, janitor, janitor_form

def telegram_bot(request):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot = telegram.Bot(token=os.getenv('TOKEN'))

    command_handlers = [
        CommandHandler('ruokalista', hamis_menu, pass_args=True),
        CommandHandler('huolto', janitor),
        CommandHandler('huoltoilmoitus', janitor_form),
    ]

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        print(update)

    # for handler in command_handlers:
    #     updater.dispatcher.add_handler(handler)

    # updater.start_webhook()
