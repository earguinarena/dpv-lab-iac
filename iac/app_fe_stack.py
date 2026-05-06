import os
from aws_cdk import (
    Stack,
    Fn,
    aws_s3 as s3,
)
from constructs import Construct

from iac.components.react_webapp_hosting import ReactWebappHosting
from iac.components.react_webapp_pipeline import ReactWebappPipeline


class AppFeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 stage,
                 name,
                 cognito_user_pool_id,
                 cognito_app_client_id,
                 cognito_app_region,
                 domain,
                 app_host,
                 api_base_url,
                 github_owner,
                 branch,
                 app_fe_repo,
                 storage_pipeline: s3.Bucket,
                 codestar_connection,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # App hosting: S3 + Cloudfront + R53 Host + Certificate
        app_fe_hosting = ReactWebappHosting(
            stack=self,
            stage=stage,
            domain=domain,
            host=app_host,
            bucket_name=f"{stage}-{name}-app-fe",
        )

        environment_variables_fe = {
            "STAGE": stage,
            "APP_USER_POOL_ID": cognito_user_pool_id,
            "APP_CLIENT_ID": cognito_app_client_id,
            "APP_REGION": cognito_app_region,
            "API_URL": api_base_url
        }

        # Pipeline + S3 Artifact
        ReactWebappPipeline(
            stack=self,
            name=f"{name}-app-fe",
            stage=stage,
            owner=github_owner,
            codestar_connection=codestar_connection,
            repo=app_fe_repo,
            branch=branch,
            deploy_bucket=app_fe_hosting.get_site_bucket(),
            distribution_id=app_fe_hosting.get_distribution_id(),
            environment_variables=environment_variables_fe,
            storage_pipeline=storage_pipeline
        )
