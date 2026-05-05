from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput
)

from constructs import Construct

from iac.components.storage_service import StorageService
from iac.components.cognito_user_pool import CognitoUserPool
from iac.components.storage import Storage
from iac.resources.dynamodb_tables import DynamodbTables
from iac.components.api_domain_name import ApiDomainName
from iac.components.queue_component import QueueComponent

class ResourcesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 stage,
                 name,
                 domain,
                 api_host,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cognito
        self.__cognito = CognitoUserPool(
            self, "CognitoUserPool",
            name=name,
            stage=stage
        )

        # # Api Domain Name
        self.__api_domain_name = ApiDomainName(
            self,
            name="dpv",
            domain=domain,
            host=api_host,
            stage=stage
        )

        # S3 Bucket
        self.__data_storage = Storage(
            self,
            bucket_name="dpv-lab-data-storage",
            family_name="Data",
            stage=stage,
            export_name="dpv-bucket-name-export"
        )

        # Dynamo DB Tables Locale
        DynamodbTables(
            self,
            stage=stage,
            family_name=""

        )

        if stage=="dev":
            # creo tablas para tests de integracion
            DynamodbTables(
                self,
                stage="integration",
                family_name="Integration"
            )


        QueueComponent(
            self, "EnviosQueue",
            name="dpv-envios",
            family_name="Envios",
            stage=stage,
            export_name="dpv-envios-queue",
        )

        # pipeline artifacts bucket
        self.__pipeline_artifacts_bucket = StorageService(
            stack=self,
            name=f"{stage}-{name}-pipeline-artifacts",
            stage=stage,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        CfnOutput(
            self, "PipelineArtifactExport",
            export_name=f"{stage}GesvetResourcesPipelineArtifactsBucketName",
            value=self.__pipeline_artifacts_bucket.get_bucket_name()
        )

    def get_pipeline_artifacts_bucket(self):
        return self.__pipeline_artifacts_bucket.get_bucket()

    def get_cognito_user_pool_id(self):
        return self.__cognito.get_user_pool_id()

    def get_cognito_app_client_id(self):
        return self.__cognito.get_app_client_id()

    def get_cognito_app_region(self):
        return self.__cognito.get_user_pool_region()

    def get_cognito_user_pool(self):
        return self.__cognito.get_user_pool()

    def get_cognito_app_clients(self):
        return self.__cognito.get_app_clients()