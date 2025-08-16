#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Main Pokemon Table
        pokemon_table = dynamodb.Table(
            self, "PokemonTable",
            table_name="PokemonTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Pokemon Types Table (for reference data)
        types_table = dynamodb.Table(
            self, "PokemonTypesTable",
            table_name="PokemonTypesTable",
            partition_key=dynamodb.Attribute(
                name="type_name",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Pokemon Abilities Table
        abilities_table = dynamodb.Table(
            self, "PokemonAbilitiesTable",
            table_name="PokemonAbilitiesTable",
            partition_key=dynamodb.Attribute(
                name="ability_id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Pokemon Stats Table (for detailed stats tracking)
        stats_table = dynamodb.Table(
            self, "PokemonStatsTable",
            table_name="PokemonStatsTable",
            partition_key=dynamodb.Attribute(
                name="pokemon_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="stat_name",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Output table names
        CfnOutput(self, "PokemonTableName", value=pokemon_table.table_name)
        CfnOutput(self, "TypesTableName", value=types_table.table_name)
        CfnOutput(self, "AbilitiesTableName", value=abilities_table.table_name)
        CfnOutput(self, "StatsTableName", value=stats_table.table_name)

app = cdk.App()
DatabaseStack(app, "PokemonDatabaseStack")
app.synth()