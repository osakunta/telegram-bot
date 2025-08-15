# SatO Telegram Bot

This bot has some useful functionality for Satakuntalainen Osakunta. It can be found on Telegram as `@osakuntabot`.

Available commands:

    /huolto
    /huoltoilmoitus
    /ruokalista
    /tjviisi

## Development

⚠️⚠️ Read the entirety of this section before making changes to the repository ⚠️⚠️

### Development flow

1. Always create a new branch for whatever you are working on
2. When you're done, create a pull request
3. Check the preview for what changes will be done upon deployment
4. If everything looks good, merge the pull request and the changes will be automatically done

### Warnings

The code in the `master` branch is automatically deployed. Therefore you should be careful as to what you merge to this branch.

Changes to the `infra/` directory modify the resources that are deployed on the cloud. These can incur extra cost if you are not careful.
Changes to the application source code (`main.py`, `telegram_bot/`) can also incur costs if they run for long or consume a lot of resources (processor time, bandwidth)

Be mindful to the changes you make. You can ask for help and comments on your pull request before merging. After large changes, monitor the costs incurred manually on the cloud dashboard.

### Local development

Get `pipenv` from [here](https://pipenv.pypa.io/en/latest/)

Setup the development environment with:

    pipenv install

Enter the project's virtual environment with

    pipenv shell

Check pipenv docs for more information.

You can test the commands on commandline by:

    python main.py /command [args]

NB! If you add dependencies to the project, remember to generate a new requirements.txt with `pipenv requirements > requirements.txt` and push it to the repo. Pipfile is not supported by Google Cloud Functions.
