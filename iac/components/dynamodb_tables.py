from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_dynamodb as dynamodb,
)


class DynamodbTables:
    def __init__(self,
                 stack: Stack,
                 stage,
                 ) -> None:

        self.__profesional = dynamodb.Table(
            stack, "ProfesionalDynamoTable",
            table_name=f"{stage}-dpv-lab-Profesional",
            partition_key=dynamodb.Attribute(
                name="uid_profesional",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )

        self.__establecimiento = dynamodb.Table(
            stack, "EstablecimientoDynamoTable",
            table_name=f"{stage}-dpv-lab-Establecimiento",
            partition_key=dynamodb.Attribute(
                name="uid_establecimiento",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )

        self.__establecimiento.add_global_secondary_index(
            index_name="uid_profesional_actual_index",
            partition_key=dynamodb.Attribute(
                name="uid_profesional_actual",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__protocolo = dynamodb.Table(
            stack, "ProtocoloDynamoTable",
            table_name=f"{stage}-dpv-lab-Protocolo",
            partition_key=dynamodb.Attribute(
                name="uid_protocolo",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )

        self.__analisis = dynamodb.Table(
            stack, "AnalisisDynamoTable",
            table_name=f"{stage}-dpv-lab-Analisis",
            partition_key=dynamodb.Attribute(
                name="uid_protocolo",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="uid_analisis",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )

        self.__parametros_sistema = dynamodb.Table(
            stack, "ParametrosSistemaDynamoTable",
            table_name=f"{stage}-dpv-lab-ParametrosSistema",
            partition_key=dynamodb.Attribute(
                name="nombre_parametro",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )
