from aws_cdk import (
    RemovalPolicy,
    CfnOutput,
    Stack,
    aws_s3 as s3
)


class Storage:
    def __init__(self,
                 stack: Stack,
                 bucket_name,
                 family_name,
                 ) -> None:

        # Bucket
        self.__bucket = s3.Bucket(
            stack, f"Bucket{family_name}",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN
        )


    def get_bucket_name(self):
        return self.__bucket.bucket_name

    def get_bucket(self):
        return self.__bucket