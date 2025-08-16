#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)
from constructs import Construct

class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        pokemon_table = dynamodb.Table(
            self, "PokemonTable",
            table_name="PokemonTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Lambda Function
        pokemon_lambda = _lambda.Function(
            self, "PokemonHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="pokemon_handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": pokemon_table.table_name
            }
        )

        # Grant Lambda permissions to DynamoDB
        pokemon_table.grant_read_write_data(pokemon_lambda)

        # API Gateway
        api = apigateway.RestApi(
            self, "PokemonApi",
            rest_api_name="Pokemon Service",
            description="This service serves Pokemon data.",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"]
            )
        )

        # Lambda integration
        pokemon_integration = apigateway.LambdaIntegration(pokemon_lambda)

        # API Routes
        pokemons = api.root.add_resource("pokemons")
        pokemons.add_method("GET", pokemon_integration)
        pokemons.add_method("POST", pokemon_integration)

        pokemon_item = pokemons.add_resource("{id}")
        pokemon_item.add_method("GET", pokemon_integration)
        pokemon_item.add_method("PUT", pokemon_integration)
        pokemon_item.add_method("DELETE", pokemon_integration)

        # Output API URL
        cdk.CfnOutput(self, "ApiUrl", value=api.url)

app = cdk.App()
BackendStack(app, "PokemonBackendStack")
app.synth()