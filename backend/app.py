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

        # Lambda functions for each CRUD operation
        get_pokemons_lambda = _lambda.Function(
            self, "GetPokemonsHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="get_pokemons.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )
        
        get_pokemon_lambda = _lambda.Function(
            self, "GetPokemonHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="get_pokemon.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )
        
        create_pokemon_lambda = _lambda.Function(
            self, "CreatePokemonHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="create_pokemon.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )
        
        update_pokemon_lambda = _lambda.Function(
            self, "UpdatePokemonHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="update_pokemon.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )
        
        delete_pokemon_lambda = _lambda.Function(
            self, "DeletePokemonHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="delete_pokemon.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Grant Lambda permissions to DynamoDB
        pokemon_table.grant_read_data(get_pokemons_lambda)
        pokemon_table.grant_read_data(get_pokemon_lambda)
        pokemon_table.grant_write_data(create_pokemon_lambda)
        pokemon_table.grant_read_write_data(update_pokemon_lambda)
        pokemon_table.grant_write_data(delete_pokemon_lambda)

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

        # Lambda integrations
        get_pokemons_integration = apigateway.LambdaIntegration(get_pokemons_lambda)
        get_pokemon_integration = apigateway.LambdaIntegration(get_pokemon_lambda)
        create_pokemon_integration = apigateway.LambdaIntegration(create_pokemon_lambda)
        update_pokemon_integration = apigateway.LambdaIntegration(update_pokemon_lambda)
        delete_pokemon_integration = apigateway.LambdaIntegration(delete_pokemon_lambda)

        # API Routes
        pokemons = api.root.add_resource("pokemons")
        pokemons.add_method("GET", get_pokemons_integration)
        pokemons.add_method("POST", create_pokemon_integration)

        pokemon_item = pokemons.add_resource("{id}")
        pokemon_item.add_method("GET", get_pokemon_integration)
        pokemon_item.add_method("PUT", update_pokemon_integration)
        pokemon_item.add_method("DELETE", delete_pokemon_integration)

        # Output API URL
        cdk.CfnOutput(self, "ApiUrl", value=api.url)

app = cdk.App()
BackendStack(app, "PokemonBackendStack")
app.synth()