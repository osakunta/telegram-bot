from menu import get_todays_menu, get_weeks_menu


def __send_message(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='markdown')


def hamis_menu(bot, update, args):
    if args[0] == 'viikko':
        __send_message(bot, update, get_weeks_menu())
    else:
        __send_message(bot, update, get_todays_menu())


def janitor(bot, update):
    __send_message(bot, update, "Satakuntatalon huoltopäivystys puh. 050-2861")
