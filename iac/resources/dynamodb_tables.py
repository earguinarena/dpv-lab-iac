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
                 family_name
                 ) -> None:

        self.__profesional = dynamodb.Table(
            stack, f"{family_name}ProfesionalDynamoTable",
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
            stack, f"{family_name}EstablecimientoDynamoTable",
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
            stack, f"{family_name}ProtocoloDynamoTable",
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

        self.__protocolo.add_global_secondary_index(
            index_name="entity_type_numero_protocolo_index",
            partition_key=dynamodb.Attribute(
                name="entity_type",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="numero_protocolo",
                type=dynamodb.AttributeType.NUMBER
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__protocolo.add_global_secondary_index(
            index_name="uid_establecimiento_numero_protocolo_index",
            partition_key=dynamodb.Attribute(
                name="uid_establecimiento",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="numero_protocolo",
                type=dynamodb.AttributeType.NUMBER
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__protocolo.add_global_secondary_index(
            index_name="uid_profesional_numero_protocolo_index",
            partition_key=dynamodb.Attribute(
                name="uid_profesional",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="numero_protocolo",
                type=dynamodb.AttributeType.NUMBER
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__analisis = dynamodb.Table(
            stack, f"{family_name}AnalisisDynamoTable",
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
            stack, f"{family_name}ParametrosSistemaDynamoTable",
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

        self.__envio_informe = dynamodb.Table(
            stack, f"{family_name}EnvioInformeDynamoTable",
            table_name=f"{stage}-dpv-lab-EnvioInforme",
            partition_key=dynamodb.Attribute(
                name="uid_envio",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=True
            )
        )
        self.__envio_informe.add_global_secondary_index(
            index_name="uid_protocolo_index",
            partition_key=dynamodb.Attribute(
                name="uid_protocolo",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="fecha_solicitud",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__envio_informe.add_global_secondary_index(
            index_name="uid_envio_batch_index",
            partition_key=dynamodb.Attribute(
                name="uid_envio_batch",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="fecha_solicitud",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        self.__envio_informe.add_global_secondary_index(
            index_name="message_id_index",
            partition_key=dynamodb.Attribute(
                name="message_id",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )



