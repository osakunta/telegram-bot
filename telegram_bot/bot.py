from .menu import get_todays_menu, get_weeks_menu
from datetime import datetime, date
from pytz import timezone

tz = timezone('Europe/Helsinki')


def __send_message(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='markdown')


def __hamis_menu(bot, update, args):
    if args and args[0] == 'viikko':
        __send_message(bot, update, get_weeks_menu())
    else:
        __send_message(bot, update, get_todays_menu())


def __janitor(bot, update, args):
    __send_message(bot, update, "Satakuntatalon huoltopäivystys puh. 050-2861")


def __janitor_form(bot, update, args):
    __send_message(bot, update, "[Huoltoilmoituslomake](https://m.fimx.fi/julmo/satakuntatalo/huoltoilmoitus)")

def __tj_viisi(bot, update, args):
    today = datetime.now(tz).date()
    opening = tz.localize(datetime(2022, 9, 1)).date()
    tj = (opening - today).days
    __send_message(bot, update, f"Viisi-TJ on {tj}!")

__commands = {
    '/ruokalista': __hamis_menu,
    '/huolto': __janitor,
    '/huoltoilmoitus': __janitor_form,
    '/tjviisi': __tj_viisi
}


def execute_bot_command(command, args, bot, telegram_update):
    command_function = __commands.get(command)

    if command_function:
        command_function(bot, telegram_update, args)
