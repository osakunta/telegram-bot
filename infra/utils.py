import pulumi
import pulumi_gcp as gcp

def service_account_with_roles(name, roles, **account_args):
    account = gcp.serviceaccount.Account(name, **account_args)
    for role in roles:
        gcp.projects.IAMMember(f"{name}-role:{role}",
            project=account.project,
            role=role,
            member=account.member,
            opts=pulumi.ResourceOptions(
                depends_on=[account]
            )
        )
    return account


def secret_with_access(name, members, **secret_args):
    secret = gcp.secretmanager.Secret(name, **secret_args)
    for member in members:
        member.apply(
            lambda m: gcp.secretmanager.SecretIamMember(f"{name}-access:{m}",
                project=secret.project,
                secret_id=secret.id,
                role="roles/secretmanager.secretAccessor",
                member=m,
                opts=pulumi.ResourceOptions(
                    depends_on=[secret]
                )
            )
        )
    return secret