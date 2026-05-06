from aws_cdk import (
    Duration,
    CfnOutput,
    aws_sqs as sqs
)

from constructs import Construct

class QueueComponent(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 name,
                 family_name,
                 stage,
                 export_name="queue-url",
                 visibility_timeout=Duration.seconds(30),
                 receive_message_wait_time=Duration.seconds(5),
                 retention_period=Duration.days(4),
                 with_dead_letter_queue=False,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if with_dead_letter_queue:
            # Dead Letter Queue
            dlq = sqs.Queue(
                self,
                f"DqlQueue{family_name}",
                queue_name=f"{stage}-dql-{name}",
                retention_period=Duration.days(14),
            )
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=5,
                queue=dlq,
            )
        else:
            dead_letter_queue = None


        self.__queue = sqs.Queue(
            self, f"Queue{family_name}",
            queue_name=f"{stage}-{name}",
            dead_letter_queue=dead_letter_queue,
            visibility_timeout=visibility_timeout,
            receive_message_wait_time=receive_message_wait_time,
            retention_period=retention_period
        )

        CfnOutput(
            self, f"Queue{family_name}UrlExport",
            export_name=f"{stage}-{export_name}-url",
            value=self.__queue.queue_url
        )

        CfnOutput(
            self, f"Queue{family_name}ArnExport",
            export_name=f"{stage}-{export_name}-arn",
            value=self.__queue.queue_arn
        )

    def get_queue(self):
        return self.__queue