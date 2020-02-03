from .menu import get_todays_menu, get_weeks_menu


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
    __send_message(bot, update, "[Huoltoilmoituslomake](https://asuntola.satakuntatalo.fi/huoltoilmoitus)")


__commands = {
    '/ruokalista': __hamis_menu,
    '/huolto': __janitor,
    '/huoltoilmoitus': __janitor_form,
}


def execute_bot_command(command, args, bot, telegram_update):
    command_function = __commands.get(command)

    if command_function:
        command_function(bot, telegram_update, args)
