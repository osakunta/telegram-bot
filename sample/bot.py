from menu import get_todays_menu


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def today(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=get_todays_menu())
