from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3
)

from constructs import Construct


class StorageService:
    __bucket: s3.Bucket
    __region: str

    def __init__(self,
                 stack: Stack,
                 name,
                 stage,
                 removal_policy: RemovalPolicy = None,
                 auto_delete_objects=False
                 ) -> None:

        if removal_policy is not None:
            pass
        elif stage in ["dev", "testing"]:
            removal_policy = RemovalPolicy.DESTROY
        else:
            removal_policy = RemovalPolicy.RETAIN

        self.__bucket = s3.Bucket(
            stack, f"StorageBucket-{name}",
            bucket_name=f"{stage}-{name}-storage",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            removal_policy=removal_policy,
            auto_delete_objects=auto_delete_objects
        )

        self.__region= stack.region

    def get_bucket_name(self):
        return self.__bucket.bucket_name

    def get_bucket(self):
        return self.__bucket

    def get_region(self):
        return self.__region