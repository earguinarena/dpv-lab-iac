from aws_cdk import (
    Stack,
    aws_s3 as s3,
)
from constructs import Construct

from iac.components.lambda_pipeline_github import LambdaGithubPipeline


class BePipelines(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 stage,
                 github_owner,
                 branch,
                 codestar_connection,
                 storage_pipeline: s3.Bucket,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        LambdaGithubPipeline(
            self,
            name="dpv-lab-be",
            family_name="DpvLabBe",
            stage=stage,
            github_owner=github_owner,
            repo="dpv-lab-be",
            branch=branch,
            codestar_connection=codestar_connection,
            storage_pipeline=storage_pipeline
        )