import os
import sys
import logging
from google.cloud import logging
import telegram
import functions_framework
from telegram_bot.bot import execute_bot_command
from telegram_bot.mocks import bot as bot_mock, update as update_mock

def parse_instructions(update):
    if update and update.message and isinstance(update.message.text, str):
        instructions = update.message.text.split()
        command = instructions[0].split('@', 1)[0]
        args = instructions[1:]

        return command, args

    return None, None

logging_client = logging.Client()
logger = logging_client.logger('telegram_bot')

@functions_framework.http
def telegram_bot(request):

    # check the header for the secret token
    secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    logger.log_text(f"Received request with secret token: {secret_token}")
    logger.log_text(f"Environment variable WEBHOOK_TOKEN: {os.getenv('WEBHOOK_TOKEN')}")
    if secret_token != os.getenv('WEBHOOK_TOKEN'):
        logger.log_text("Invalid secret token")
        return "Forbidden", 403

    bot = telegram.Bot(token=os.getenv('API_TOKEN'))

    if request and request.method == "POST":
        try:
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            command, args = parse_instructions(update)

            execute_bot_command(command, args, bot, update)
            return "OK", 200
        except Exception as e:
            logging.error(f"Error processing update: {e}")
            return "Internal Server Error", 500

    return "Invalid request", 400

# Used to test the bot on commandline by: python main.py /command [args]
if __name__ == '__main__':
    command = sys.argv[1]
    args = sys.argv[2:]

    execute_bot_command(command, args, bot_mock, update_mock)
