import pulumi
import pulumi_gcp as gcp 
import pulumi_random as random
import utils

gcp_config = pulumi.Config("gcp")
LOCATION = gcp_config.require("region")
STACK_NAME = pulumi.get_stack()

project_id = random.RandomPet("project-id",
    length=2
)

project = gcp.organizations.Project("project",
    name=f"Telegram Bot {STACK_NAME}",
    project_id=project_id.id,
    folder_id="452932952214"
)

# Enable required services / APIs
secretmanager_service = gcp.projects.Service("secretmanager-service",
    project=project_id.id,
    service="secretmanager.googleapis.com",
    disable_on_destroy=True
)

cloudbuild_service = gcp.projects.Service("cloudbuild-service",
    project=project_id.id,
    service="cloudbuild.googleapis.com",
    disable_on_destroy=True
)

cloudrun_service = gcp.projects.Service("cloudrun-service",
    project=project_id.id,
    service="run.googleapis.com",
    disable_on_destroy=True
)

cloudfunctions_service = gcp.projects.Service("cloudfunctions-service",
    project=project_id.id,
    service="cloudfunctions.googleapis.com",
    disable_on_destroy=True
)

cloudresourcemanager_service = gcp.projects.Service("cloudresourcemanager-service",
    project=project_id.id,
    service="cloudresourcemanager.googleapis.com",
    disable_on_destroy=True
)


# --- Set up github repo connection ---
github_token_secret = gcp.secretmanager.Secret("github-token-secret",
    project=project_id.id,
    secret_id="github-token",
    replication={
        "user_managed": {
            "replicas": [{ "location": LOCATION }]
        }
    },
    opts=pulumi.ResourceOptions(
        depends_on=[secretmanager_service]
    )
)

github_connection_service_account_secret_access = gcp.secretmanager.SecretIamMember("github-connection-service-account-secret-access",
    project=project_id.id,
    secret_id=github_token_secret.id,
    role="roles/secretmanager.secretAccessor",
    member=pulumi.Output.concat(
        "serviceAccount:service-",
        project.number,
        "@gcp-sa-cloudbuild.iam.gserviceaccount.com"
    ),
    opts=pulumi.ResourceOptions(
        depends_on=[cloudbuild_service]
    )
)

github_connection = gcp.cloudbuildv2.Connection("github-connection",
    project=project_id.id,
    name="github-connection",
    location=LOCATION,
    github_config={
        "app_installation_id": 30357801,
        "authorizer_credential": {
            "oauth_token_secret_version": github_token_secret.name.apply(lambda name: f"{name}/versions/latest")
        }
    },
    opts=pulumi.ResourceOptions(
        depends_on=[github_connection_service_account_secret_access]
    )
)

github_repository = gcp.cloudbuildv2.Repository("github-repository",
    project=project_id.id,
    name="telegram-bot",
    location=LOCATION,
    parent_connection=github_connection.name,
    remote_uri="https://github.com/osakunta/telegram-bot.git",
)

# --- Set up CI/CD ---

cicd_service_account = utils.service_account_with_roles(
    "cicd-service-account",
    [
        "roles/logging.logWriter", 
        "roles/cloudfunctions.developer",
        "roles/run.admin",
        "roles/iam.serviceAccountUser",
        "roles/storage.objectViewer",
        "roles/artifactregistry.writer"
    ],
    project=project_id.id,
    account_id="cicd-service-account",
    display_name="CICD Service Account"
)

runtime_service_account = utils.service_account_with_roles(
    "runtime-service-account",
    [ 
        "roles/iam.serviceAccountUser",
        "roles/logging.logWriter"
    ],
    project=project_id.id,
    account_id="runtime-service-account",
    display_name="Function Runtime Service Account"
)

# used by the cloud function to access telegram API
telegram_api_token = utils.secret_with_access(
    "telegram-api-token",
    members=[runtime_service_account.member, cicd_service_account.member],
    project=project_id.id,
    secret_id="telegram-api-token",
    replication={
        "user_managed": {
            "replicas": [{ "location": LOCATION }]
        }
    },
    opts=pulumi.ResourceOptions(
        depends_on=[secretmanager_service]
    )
) 

# telegram sends this alongside the updates to the bot, so that malicious actors cannot use the endpoint
telegram_webhook_token = utils.secret_with_access(
    "telegram-webhook-token",
    members=[runtime_service_account.member, cicd_service_account.member],
    project=project_id.id,
    secret_id="telegram-webhook-token",
    replication={
        "user_managed": {
            "replicas": [{ "location": LOCATION }]
        }
    },
    opts=pulumi.ResourceOptions(
        depends_on=[secretmanager_service]
    )
)

deploy_trigger = gcp.cloudbuild.Trigger("deploy-trigger",
    project=project_id.id,
    name="deploy",
    location=LOCATION,
    service_account=cicd_service_account.id,
    repository_event_config={
        "repository": github_repository.id,
        "push": {
            "branch": f"^{STACK_NAME}$",
        }
    },
    build={
        "steps": [
            {
                "id": "Deploy function",
                "name": "gcr.io/google.com/cloudsdktool/cloud-sdk:slim",
                "entrypoint": "gcloud",
                "args": [
                    "functions", "deploy", "telegram-bot",
                    "--region", LOCATION,
                    "--runtime", "python312",
                    "--entry-point", "telegram_bot",
                    "--trigger-http",
                    "--allow-unauthenticated",
                    "--timeout", "5s",
                    "--gen2",
                    "--max-instances", "1",
                    "--min-instances", "0",
                    "--memory", "256Mi",
                    "--set-secrets", pulumi.Output.format(
                        "API_TOKEN={0}:latest,WEBHOOK_TOKEN={1}:latest",
                        telegram_api_token.name,
                        telegram_webhook_token.name
                    ),
                    "--source", ".",
                    "--run-service-account", runtime_service_account.email,
                    "--build-service-account", cicd_service_account.id,
                ],
            },
            {
                "id": "Get function URL",
                "name": "gcr.io/google.com/cloudsdktool/cloud-sdk:slim",
                "entrypoint": "bash",
                "args": [
                    "-c",
                    project_id.id.apply(
                        lambda id: 
                            f"gcloud functions describe telegram-bot --region={LOCATION} --project={id} --format='value(url)' > /workspace/url.txt"
                    )
                ]
            },
            {
                "id": "Set webhook URL",
                "name": "gcr.io/gcp-runtimes/ubuntu_20_0_4",
                "entrypoint": "bash",
                "args": [
                    "-c",
                    'curl https://api.telegram.org/bot$${API_TOKEN}/setWebhook?url=$(cat /workspace/url.txt)&secret_token=$${WEBHOOK_TOKEN}'
                ],
                "secretEnv": [
                    "API_TOKEN",
                    "WEBHOOK_TOKEN"
                ]
            }
        ],
        "options": {
            "logging": "CLOUD_LOGGING_ONLY"
        },
        "availableSecrets": {
            "secretManager": [
                {
                    "env": "API_TOKEN",
                    "versionName": telegram_api_token.name.apply(lambda name: f"{name}/versions/latest"),
                },
                {
                    "env": "WEBHOOK_TOKEN",
                    "versionName": telegram_webhook_token.name.apply(lambda name: f"{name}/versions/latest"),
                }
            ]
        },
    },
    opts=pulumi.ResourceOptions(
        depends_on=[ cloudrun_service, cloudfunctions_service, cloudresourcemanager_service ]
    )
)