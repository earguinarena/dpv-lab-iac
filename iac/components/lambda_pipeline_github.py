from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_s3 as s3,
)


class LambdaGithubPipeline:
    def __init__(self,
                 stack: Stack,
                 name,
                 family_name,
                 stage,
                 github_owner,
                 repo,
                 branch,
                 codestar_connection,
                 storage_pipeline: s3.Bucket,
                 architecture="x86"
                 ) -> None:


        source_output = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="CodeConectionSource",
            owner=github_owner,
            repo=repo,
            branch=branch,
            connection_arn=codestar_connection,
            output=source_output
        )

        manual_approval_action = codepipeline_actions.ManualApprovalAction(
            action_name="Approve",
        )

        if architecture == "arm":
            # https://docs.aws.amazon.com/codebuild/latest/userguide/available-runtimes.html
            build_image = codebuild.LinuxArmBuildImage.AMAZON_LINUX_2_STANDARD_3_0
            # https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html
            compute_type = codebuild.ComputeType.SMALL
        elif architecture == "x86":
            build_image = codebuild.LinuxBuildImage.AMAZON_LINUX_2_5
            compute_type = codebuild.ComputeType.MEDIUM
        else:
            raise Exception(f"Pipeline Architecture is wrong: {architecture}")

        build_environment_variables = {
            "ENVIRONMENT": codebuild.BuildEnvironmentVariable(value=stage),
            "ARCHITECTURE": codebuild.BuildEnvironmentVariable(value=architecture),
            "ACCOUNT_ID": codebuild.BuildEnvironmentVariable(value=stack.account),
            "REGION": codebuild.BuildEnvironmentVariable(value=stack.region),
        }

        project = codebuild.PipelineProject(
            stack, f"CodeBuildMicroservice{family_name}",
            project_name=f"{name}-{stage}",
            description="Deploy Lambda",
            environment=codebuild.BuildEnvironment(
                build_image=build_image,
                compute_type=compute_type,
                privileged=True,
            ),
            environment_variables=build_environment_variables,

        )

        project.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "sts:AssumeRole"
                ],
                resources=[
                    "arn:aws:iam::*:role/cdk-*"
                ],
            )
        )

        # Code Artifacti policies
        project.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "sts:GetServiceBearerToken"
                ],
                resources=["*"],
                conditions={
                    "StringEquals": {
                        "sts:AWSServiceName": "codeartifact.amazonaws.com"
                    }

                }

            )
        )
        project.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "codeartifact:GetAuthorizationToken",
                    "codeartifact:GetRepositoryEndpoint",
                    "codeartifact:ReadFromRepository",
                    "ssm:GetParameter"
                  ],
                resources=[
                    "*"
                ],
            )
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=project,
            input=source_output,
        )

        # Pipeline
        pipeline = codepipeline.Pipeline(
            stack, f"PipelineMicroservice{family_name}",
            pipeline_name=f"{name}-{stage}",
            artifact_bucket=storage_pipeline,
            pipeline_type=codepipeline.PipelineType.V1
        )

        pipeline.add_stage(
            stage_name="Get_Source",
            actions=[source_action]
        )

        if stage not in ["dev"]:
            pipeline.add_stage(
                stage_name="ManualApproval",
                actions=[manual_approval_action]
            )

        pipeline.add_stage(
            stage_name="Deploy_Lambda",
            actions=[build_action]
        )
