import pulumi
import pulumi_gcp as gcp 

def setup_cicd():
    gcp_config = pulumi.Config("gcp")
    LOCATION = gcp_config.require("region")
    PROJECT_ID = gcp_config.require("project")

    config = pulumi.Config()
    STACK_NAME = config.require("stack_name")
    GITHUB_BRANCH = config.require("github_branch") 


    # Set up secret to hold the GitHub token
    github_token_secret = gcp.secretmanager.Secret("github-token-secret",
        secret_id="github-token",
        replication={
            "user_managed": {
                "replicas": [{ "location": LOCATION }]
            }
        }
    )
    # Populate this manually
    github_token_secret_version = gcp.secretmanager.get_secret_version(secret=github_token_secret.id) 

    PROJECT_NUMBER = gcp.projects.get_project(filter=f"id:{PROJECT_ID}").projects[0].number
    service_account_secret_access = gcp.secretmanager.SecretIamMember("service-account-secret-access",
        secret_id=github_token_secret.id,
        role="roles/secretmanager.secretAccessor",
        member=f"serviceAccount:service-{PROJECT_NUMBER}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
    )

    github_connection = gcp.cloudbuildv2.Connection("github-connection",
        name="github-connection",
        location=LOCATION,
        github_config={
            "app_installation_id": 30357801,
            "authorizer_credential": {
                "oauth_token_secret_version": github_token_secret_version.id,
            }
        },
        opts=pulumi.ResourceOptions(
            depends_on=[service_account_secret_access]
        )
    )

    github_repository = gcp.cloudbuildv2.Repository("github-repository",
        name="telegram-bot",
        location=LOCATION,
        parent_connection=github_connection.name,
        remote_uri="https://github.com/osakunta/telegram-bot.git",
    )

    cicd_service_account = gcp.serviceaccount.Account("cicd-service-account",
        account_id="cicd-service-account",
        display_name="CICD Service Account"
    )

    # Artefact Registry stores the Docker images built by Cloud Build
    artefact_repository = gcp.artifactregistry.Repository("artefact-repository",
        repository_id="telegram-bot",
        location=LOCATION,
        format="DOCKER",
        description="Docker repository for the Telegram Bot",
        labels={
            "osakunta": "telegram-bot"
        }
    )

    # staging_build_trigger = gcp.cloudbuild.Trigger("staging-build-trigger",
    #     name="staging-build",
    #     location=LOCATION,
    #     repository_event_config={
    #         "repository": github_repository.id,
    #         "push": {
    #             "branch": "^staging$",
    #         }
    #     }
    # )

    IMAGE_URL = artefact_repository.name.apply(lambda name: f"{LOCATION}-docker.pkg.dev/{PROJECT_ID}/{name}/telegram-bot:$COMMIT_SHA")
    build_trigger = gcp.cloudbuild.Trigger("build-trigger",
        name="prod-build",
        location=LOCATION,
        service_account=cicd_service_account.id,
        repository_event_config={
            "repository": github_repository.id,
            "push": {
                "branch": "^main$",
            }
        },
        build={
            "images": [IMAGE_URL],
            "steps": [{
                "name": "gcr.io/k8s-skaffold/pack",
                "entrypoint": "pack",
                "args": [
                    "build",
                    IMAGE_URL,
                    "--builder", "gcr.io/buildpacks/builder:latest",
                    "--network",
                    "cloudbuild"
                ],
            }],
        }
    )