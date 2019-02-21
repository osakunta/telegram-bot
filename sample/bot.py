from menu import get_todays_menu, get_weeks_menu


def __send_message(bot, update, message):
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='markdown')


def today(bot, update):
    __send_message(bot, update, get_todays_menu())


def week(bot, update):
    __send_message(bot, update, get_weeks_menu())
