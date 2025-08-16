import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PokemonTable')

def lambda_handler(event, context):
    try:
        pokemon_id = event['pathParameters']['id']
        data = json.loads(event['body'])
        
        response = table.update_item(
            Key={'id': pokemon_id},
            UpdateExpression='SET #name = :name, #type = :type, image = :image, pokedexNumber = :pokedexNumber',
            ExpressionAttributeNames={
                '#name': 'name',
                '#type': 'type'
            },
            ExpressionAttributeValues={
                ':name': data['name'],
                ':type': data['type'],
                ':image': data.get('image', ''),
                ':pokedexNumber': data.get('pokedexNumber', 0)
            },
            ReturnValues='ALL_NEW'
        )
        
        item = response['Attributes']
        
        # Convert Decimal to int/float for JSON serialization
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = int(value) if value % 1 == 0 else float(value)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }