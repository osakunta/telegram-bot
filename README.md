SatO Telegram Bot
=================

This bot has some useful functionality for Satakuntalainen Osakunta. It can be found on Telegram as `@osakuntabot`.

Available commands:

    /huolto
    /huoltoilmoitus
    /ruokalista
    /tjviisi


Development
-----------

Get `pipenv` from [here](https://pipenv.pypa.io/en/latest/)

Setup the development environment with:

    pipenv install

Enter the project's virtual environment with

    pipenv shell

Check pipenv docs for more information.

You can test the commands on commandline by:

    python main.py /command [args]

The bot is hosted in Google Cloud Functions and CircleCI is used to continuously deploy new versions of the bot to GCP.
NB! If you add dependencies to the project, remember to generate a new requirements.txt with `pipenv lock -r` and push it to the repo. Pipfile is not supported by Google Cloud Functions.
