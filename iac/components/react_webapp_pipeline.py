import os
from aws_cdk import (
    Stack,
    SecretValue,
    RemovalPolicy,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_s3 as s3,
    aws_lambda as _lambda
)


class ReactWebappPipeline:

    def __init__(self,
                 stack: Stack,
                 name,
                 stage,
                 owner,
                 codestar_connection,
                 repo,
                 branch,
                 deploy_bucket: s3.Bucket,
                 distribution_id,
                 environment_variables,
                 storage_pipeline: s3.Bucket,
                 ) -> None:

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="CodeConectionSource",
            owner=owner,
            repo=repo,
            branch=branch,
            connection_arn=codestar_connection,
            output=source_output
        )
        manual_approval_action = codepipeline_actions.ManualApprovalAction(
            action_name="Approve",
        )

        # Create environment variables dynamically
        build_environment_variables = {}
        for variable in environment_variables:
            build_environment_variables[variable] = codebuild.BuildEnvironmentVariable(
                value=environment_variables[variable]
            )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=codebuild.PipelineProject(
                stack, "Build",
                project_name=f"{stage}-{name}-build",
                description="React Webapp Build",
                environment=codebuild.BuildEnvironment(
                    compute_type=codebuild.ComputeType.MEDIUM,
                    build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5,
                ),
                environment_variables=build_environment_variables,
            ),
            input=source_output,
            outputs=[build_output],
        )

        deploy_s3 = codepipeline_actions.S3DeployAction(
            action_name="S3Deploy",
            bucket=deploy_bucket,
            input=build_output,

        )

        # Delete S3 Files Lambda
        delete_s3_files_lambda = _lambda.Function(
            stack, "DeleteS3Files",
            description="Delete React file from S3",
            function_name=f"{stage}-{name}-delete-s3-files",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="webapp-delete-s3-objects.handler",
            code=_lambda.Code.from_asset(os.path.dirname(__file__) + "/../../lambda/"),
            environment={
                "bucketName": deploy_bucket.bucket_name
            },
        )

        # Add S3 delete permissions
        delete_s3_files_lambda.add_to_role_policy(iam.PolicyStatement(
            resources=[deploy_bucket.bucket_arn],
            actions=["s3:ListBucket",
                     "s3:ListBucketVersions"
                     ]
        ))
        delete_s3_files_lambda.add_to_role_policy(iam.PolicyStatement(
            resources=[deploy_bucket.arn_for_objects("*")],
            actions=["s3:DeleteObject",
                     "s3:DeleteObjectVersion"
                     ]
        ))

        delete_s3_files_lambda.add_to_role_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["codepipeline:PutJobFailureResult",
                     "codepipeline:PutJobSuccessResult"
                     ]
        ))

        delete_s3_files_lambda_action = codepipeline_actions.LambdaInvokeAction(
            action_name="Lambda",
            lambda_=delete_s3_files_lambda
        )

        # Cloudfront Invalidation Lambda
        cloudfront_invalidation_lambda = _lambda.Function(
            stack, "CloudfrontInvalidation",
            description="Cloudfront Invalidation",
            function_name=f"{stage}-{name}-cloudfront_invalidation",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="webapp-cloudfront-invalidation.handler",
            code=_lambda.Code.from_asset(os.path.dirname(__file__) + "/../../lambda/"),
        )
        cloudfront_invalidation_lambda.add_to_role_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["codepipeline:PutJobFailureResult",
                     "codepipeline:PutJobSuccessResult"
                     ]
        ))
        distribution_arn = f"arn:aws:cloudfront::{stack.account}:distribution/{distribution_id}"
        cloudfront_invalidation_lambda.add_to_role_policy(iam.PolicyStatement(
            resources=[distribution_arn],
            actions=["cloudfront:CreateInvalidation"
                     ]
        ))
        cloudfront_invalidation_lambda_action = codepipeline_actions.LambdaInvokeAction(
            action_name="Lambda",
            user_parameters={
                "distributionId": distribution_id
            },
            lambda_=cloudfront_invalidation_lambda
        )

        pipeline = codepipeline.Pipeline(
            stack, "ReactWebappPipeline",
            pipeline_name=f"{stage}-{name}-pipeline",
            artifact_bucket=storage_pipeline,
            pipeline_type=codepipeline.PipelineType.V1
        )
        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )

        if stage not in ["dev"]:
            pipeline.add_stage(
                stage_name="ManualApproval",
                actions=[manual_approval_action]
            )

        pipeline.add_stage(
            stage_name="Build",
            actions=[build_action],
        )
        pipeline.add_stage(
            stage_name="DeleteS3Files",
            actions=[delete_s3_files_lambda_action],
        )
        pipeline.add_stage(
            stage_name="S3Deploy",
            actions=[deploy_s3],
        )
        pipeline.add_stage(
            stage_name="InvalidateCache",
            actions=[cloudfront_invalidation_lambda_action],
        )
