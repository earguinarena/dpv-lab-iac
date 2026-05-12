from aws_cdk import (
    Duration,
    CfnOutput,
    aws_sns as sns
)

from constructs import Construct

class SnsTopicComponent(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 name,
                 family_name,
                 stage,
                 export_name="sns",
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__topic = sns.Topic(
            self, f"{family_name}Topic",
            topic_name=f"{name}-{stage}",
        )

        CfnOutput(
            self, f"{family_name}TopicArnExport",
            export_name=f"{stage}-{export_name}-arn",
            value=self.__topic.topic_arn
        )

    def get_topic(self):
        return self.__topic