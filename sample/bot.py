from menu import get_todays_menu


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Use command /today to get today's menu!")


def today(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=get_todays_menu(), parse_mode='markdown')
