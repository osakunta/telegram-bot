import pulumi
import pulumi_gcp as gcp

def setup_project():
    config = pulumi.Config("gcp")
    LOCATION = config.require("region")
    STACK_NAME = pulumi.get_stack()
    
    project = gcp.organizations.Project("project",
        name=f"telegram-bot-{STACK_NAME}",
        project_id=f"telegram-bot-{STACK_NAME}",
    )

    # # Set up secret to hold the Telegram API token
    # telegram_bot_token = gcp.secretmanager.Secret("telegram-bot-token",
    #     secret_id="telegram-bot-token",
    #     replication={
    #         "user_managed": {
    #             "replicas": [{ "location": LOCATION }]
    #         }
    #     }
    # )

    # # Set up a service account that has access to the secret, for the Function to use
    # function_service_account = gcp.serviceaccount.Account("function-service-account",
    #     account_id="telegram-bot-service-account",
    #     display_name="Telegram Bot Service Account")

    # secret_access = gcp.secretmanager.SecretIamMember("secret-access",
    #     secret_id=telegram_bot_token.id,
    #     role="roles/secretmanager.secretAccessor",
    #     member=function_service_account.email.apply(lambda email: f"serviceAccount:{email}")
    # )

    # # Set up the source code
    # source_bucket = gcp.storage.Bucket("source-bucket",
    #     location=LOCATION,
    #     name=f"{PROJECT_ID}-source-bucket",
    # )

    # source_asset = pulumi.AssetArchive({
    #     "telegram_bot": pulumi.FileArchive("../telegram_bot"),
    #     "main.py": pulumi.FileAsset("../main.py"),
    #     "requirements.txt": pulumi.FileAsset("../requirements.txt")
    # })
    # source_object = gcp.storage.BucketObject("source-object",
    #     bucket=source_bucket.name,
    #     name="telegram-bot-source",
    #     source=source_asset
    # )

    # # Set up the Function, which handles the requests
    # function = gcp.cloudfunctionsv2.Function("function",
    #     location=LOCATION,
    #     name="telegram-bot-function",
    #     description="Cloud Run Function for handling telegram bot requests",
    #     build_config={
    #         "runtime": "python313",
    #         "entryPoint": "telegram_bot",
    #         "source": {
    #             "storage_source": {
    #                 "bucket": source_bucket.name,
    #                 "object": source_object.name,
    #                 "generation": source_object.generation
    #             }
    #         }
    #     },  
    #     service_config={
    #         "availableMemory": "128Mi",
    #         "maxInstanceCount": 1, # No need for more than one instance
    #         "minInstanceCount": 0, # Important to allow scale-to-zero, to save costs
    #         "service_account_email": function_service_account.email,
    #         "ingressSettings": "ALLOW_ALL",
    #         "secret_environment_variables": [{
    #             "key": "TOKEN",
    #             "project_id": PROJECT_ID,
    #             "secret": telegram_bot_token.secret_id,
    #             "version": "latest"
    #         }],
    #     }
    # )

    # # Finally, set an IAM policy to allow unauthenticated people (anyone) to invoke the function
    # # this has to be cloudrun.ServiceIamMember instead of cloudfunctions.FunctionIamMember
    # # because the function is v2
    # function_public_iam = gcp.cloudrunv2.ServiceIamMember("function-public-iam",
    #     location=LOCATION,
    #     name=function.name,
    #     role="roles/run.invoker",
    #     member="allUsers"
    # )