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
