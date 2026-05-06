import os
from aws_cdk import (
    App,
    Environment,
)
from iac import utils
from iac.app_fe_stack import AppFeStack
from iac.resources_stack import ResourcesStack



stage = os.getenv('ENVIRONMENT')
conf_data = utils.get_config(stage)

domain = conf_data["domain"]
app_host = conf_data["app-host"]
api_host = conf_data["api-host"]
github_owner = conf_data["github-owner"]
git_branch = conf_data["git-branch"]
git_app_fe_repo = conf_data["git-app-fe-repo"]
codestar_connection = conf_data["codestar-connection"]

api_path="lab/v1"
base_url=f"https://{api_host}.{domain}/{api_path}"

app = App()

resources = ResourcesStack(
    app, f"{stage}-dpv-lab-resources",
    stage=stage,
    name="dpv-lab",
    domain=domain,
    api_host=api_host,
    env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                    region="us-east-1"),
)


# Web App
AppFeStack(
    app, f"{stage}-dpv-lab-app-fe",
    stage=stage,
    name="lab-app",
    cognito_user_pool_id=resources.get_cognito_user_pool_id(),
    cognito_app_client_id=resources.get_cognito_app_client_id(),
    cognito_app_region=resources.get_cognito_app_region(),
    domain=domain,
    app_host=app_host,
    api_base_url=base_url,
    github_owner=github_owner,
    branch=git_branch,
    app_fe_repo=git_app_fe_repo,
    storage_pipeline=resources.get_pipeline_artifacts_bucket(),
    codestar_connection=codestar_connection,
    env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                    region="us-east-1")
)


app.synth()
