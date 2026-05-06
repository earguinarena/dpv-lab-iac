from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam,
    aws_certificatemanager as cm,
    aws_cloudfront_origins as cloudfront_origins,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm
)


class ReactWebappHosting:

    def __init__(self,
                 stack: Stack,
                 stage,
                 host,
                 domain,
                 bucket_name,
                 root_domain=False,
                 ) -> None:

        domain_name = f"{host}.{domain}"

        # Bucket en S3 para almacenar la webapp
        self.__site_bucket = s3.Bucket(
            stack, "SiteBucket",
            bucket_name=bucket_name,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )


        # # Import Hosted zone
        # zone = route53.HostedZone.from_lookup(
        #     stack, "ImportedHostedZone",
        #     domain_name=domain,
        # )

        certificate = acm.Certificate(
            stack, "SslCertificate",
            domain_name=domain_name,
            subject_alternative_names=[] if not root_domain else [domain],
            # validation=acm.CertificateValidation.from_dns(zone)
            validation=acm.CertificateValidation.from_dns()
        )

        self.__distribution = cloudfront.Distribution(
            stack, "SiteDistribution",
            certificate=certificate,
            default_root_object="index.html",
            domain_names=[domain_name] if not root_domain else [domain_name, domain],
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=400,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(60)
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(60)
                ),
            ],
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3BucketOrigin.with_origin_access_control(
                    bucket=self.__site_bucket,
                ),
                compress=True,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )

        # Create dns register
        # route53.ARecord(
        #     stack, "WebAppAliasRecord",
        #     record_name=domain_name,
        #     target=route53.RecordTarget.from_alias(
        #         targets.CloudFrontTarget(self.__distribution)
        #     ),
        #     zone=zone
        # )

        # if root_domain:
        #     route53.ARecord(
        #         stack, "RootWebAppAliasRecord",
        #         record_name=domain,
        #         target=route53.RecordTarget.from_alias(
        #             targets.CloudFrontTarget(self.__distribution)
        #         ),
        #         zone=zone
        #     )

        CfnOutput(
            stack, "SiteBucketName",
            value=self.__site_bucket.bucket_name
        )
        CfnOutput(
            stack, "DistributionDomainName",
            value=self.__distribution.domain_name
        )


    def get_site_bucket(self):
        return self.__site_bucket

    def get_distribution_id(self):
        return self.__distribution.distribution_id