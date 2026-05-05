import os
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
)


class ApiDomainName:

    def __init__(self, stack: Stack,
                 name,
                 domain,
                 host,
                 stage,
                 ) -> None:
        domain_name = f"{host}.{domain}"

        # # Import Hosted zone
        # zone = route53.HostedZone.from_lookup(
        #     stack, "ImportedHostedZone",
        #     domain_name=domain,
        # )

        certificate = acm.Certificate(
            stack, "SslCertificate",
            domain_name=domain_name,
            # validation=acm.CertificateValidation.from_dns(zone)
            validation=acm.CertificateValidation.from_dns()
        )

        api_domain_name = apigateway.DomainName(
            stack,
            "DomainName",
            domain_name=domain_name,
            certificate=certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL
        )

        # # Create dns register
        # route53.ARecord(
        #     stack, "ApiStripeRecord",
        #     record_name=domain_name,
        #     target=route53.RecordTarget.from_alias(
        #         targets.ApiGatewayDomain(api_domain_name)
        #     ),
        #     zone=zone
        # )

        CfnOutput(
            stack, "ApiDomainRegionalHostedZoneExport",
            export_name=f"{stage}-{name}-dpv-api-regional-hosted-zone",
            value=api_domain_name.domain_name_alias_hosted_zone_id
        )

        CfnOutput(
            stack, "ApiDomainExport",
            export_name=f"{stage}-{name}-dpv-api-domain",
            value=domain
        )

        CfnOutput(
            stack, "ApiDomainNameExport",
            export_name=f"{stage}-{name}-api-domain-name",
            value=domain_name
        )