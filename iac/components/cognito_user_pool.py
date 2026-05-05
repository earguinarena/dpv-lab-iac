from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_cognito as cognito,
)

from constructs import Construct


class CognitoUserPool(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 name,
                 stage,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if stage in ["dev", "testing"]:
            removal_policy = RemovalPolicy.DESTROY
        else:
            removal_policy = RemovalPolicy.RETAIN

        # Cognito User Pool
        self.__user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name=f"{stage}-{name}",
            self_sign_up_enabled=False,
            sign_in_case_sensitive=True,
            sign_in_aliases=cognito.SignInAliases(username=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=removal_policy,
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_lowercase=False,
                require_digits=True,
                require_uppercase=False,
                require_symbols=False,
            ),
            standard_attributes=cognito.StandardAttributes(
                phone_number=cognito.StandardAttribute(
                    required=True,
                    mutable=True,
                )
            ),
            custom_attributes={
                "role": cognito.StringAttribute(
                    min_len=1,
                    max_len=50,
                    mutable=True
                )
            }
        )

        # App Client
        self.__app_client_id_react = self.__user_pool.add_client(
            "AppClientReact",
            user_pool_client_name=f"{stage}-{name}-react",
            generate_secret=False,
            refresh_token_validity=Duration.days(30),
            access_token_validity=Duration.minutes(60),
            id_token_validity=Duration.minutes(60),
            prevent_user_existence_errors=True,
            auth_flows=cognito.AuthFlow(
                custom=True,
                user_srp=True,
            )
        )

        # App Client
        self.__app_client_id_postman = self.__user_pool.add_client(
            "AppClientPostman",
            user_pool_client_name=f"{stage}-{name}-postman",
            generate_secret=False,
            refresh_token_validity=Duration.days(30),
            access_token_validity=Duration.minutes(60),
            id_token_validity=Duration.minutes(60),
            prevent_user_existence_errors=True,
            auth_flows=cognito.AuthFlow(
                user_password=True,
            )

        )

        CfnOutput(
            self, "AppClientId",
            export_name=f"{stage}-dpv-appclientid",
            value=self.__app_client_id_react.user_pool_client_id
        )

        CfnOutput(
            self, "PostmanClientId",
            export_name=f"{stage}-dpv-postmanappclientid",
            value=self.__app_client_id_postman.user_pool_client_id
        )

        CfnOutput(
            self, "UserPoolId",
            export_name=f"{stage}-dpv-userpoolid",
            value=self.__user_pool.user_pool_id
        )


    def get_user_pool_id(self):
        return self.__user_pool.user_pool_id

    def get_app_client_id(self):
        return self.__app_client_id_react.user_pool_client_id

    def get_postman_client_id(self):
        return self.__app_client_id_postman.user_pool_client_id

    def get_user_pool_region(self):
        return Stack.of(self).region

    def get_user_pool(self):
        return self.__user_pool

    def get_app_clients(self):
        return [self.__app_client_id_react, self.__app_client_id_postman]