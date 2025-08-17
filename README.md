# SatO Telegram Bot

This bot has some useful functionality for Satakuntalainen Osakunta. It can be found on Telegram as `@osakuntabot`.

Available commands:

    /huolto
    /huoltoilmoitus
    /ruokalista
    /tjviisi

## Development

⚠️⚠️ Read the entirety of this section before making changes to the repository ⚠️⚠️

If you feel lost, make sure to as for help from the verkkovastaava or tietoverkkovastaava.

### Development flow

1. Always create a new branch for whatever feature/fix you are working on. Name it descriptively. This is your development branch.
2. When you're done, create a pull request from the development to the `staging` branch. Ask for review if needed. Merge the pull request.
   - The `staging` branch automatically deploys to the staging environment.
3. Verify the project works in staging.
4. If everything looks good, create a pull request from `staging` to `prod`.
   - The `prod` branch automatically deploys to production. Make sure this branch is always working.

NB! If you add dependencies to the project, remember to generate a new requirements.txt with `pipenv requirements > requirements.txt` and push it to the repo. Pipfile is not supported by Google Cloud Functions.

### Infrastructure

This project contains the source code for the telegram bot, but it also contains code that defines the infrastructure it runs on.
In the `infra/` directory, you can find all resources that the code requires to run in the cloud, and how they are configured.
Ideally, infrastructure needs to be changed rarely. Therefore, changes to the infrastructure code are not automatically deployed. This needs to be done manually, using the command `pulumi up`.

### Warnings

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
