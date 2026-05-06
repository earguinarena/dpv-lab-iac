from aws_cdk import (
    Duration,
    CfnOutput,
    aws_ses as ses
)

from constructs import Construct

class SesIdentityDomainComponent(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 stage,
                 domain_name,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__email_identity = ses.EmailIdentity(
            self,
            f"SESIdentityDomain",
            identity=ses.Identity.domain(domain_name),
        )

        CfnOutput(
            self, f"SESIdentityDomainExport",
            export_name=f"{stage}-dpv-ses-identity-name",
            value=self.__email_identity.email_identity_name
        )


    def get_queue(self):
        return self.__queue