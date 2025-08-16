import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PokemonTable')

def lambda_handler(event, context):
    try:
        pokemon_id = event['pathParameters']['id']
        
        table.delete_item(Key={'id': pokemon_id})
        
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }