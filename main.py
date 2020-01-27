import os
import logging
import telegram
from telegram_bot.bot import hamis_menu, janitor, janitor_form

def telegram_bot(request):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot = telegram.Bot(token=os.getenv('TOKEN'))

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        instructions = update.text.split()
        command = instructions[0]
        args = instructions[1:]

        commands = {
            '/ruokalista': hamis_menu,
            '/huolto': janitor,
            '/huoltoilmoitus': janitor_form,
        }

        commands.get(command)(bot, update, args)
