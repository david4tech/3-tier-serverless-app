import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PokemonTable')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        
        pokemon = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'type': data['type'],
            'image': data.get('image', ''),
            'pokedexNumber': data.get('pokedexNumber', 0)
        }
        
        table.put_item(Item=pokemon)
        
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(pokemon)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }