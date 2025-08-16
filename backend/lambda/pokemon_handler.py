import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PokemonTable')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    try:
        if http_method == 'GET':
            return get_pokemons(event)
        elif http_method == 'POST':
            return create_pokemon(event)
        elif http_method == 'PUT':
            return update_pokemon(event)
        elif http_method == 'DELETE':
            return delete_pokemon(event)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def get_pokemons(event):
    pokemon_id = event.get('pathParameters', {}).get('id') if event.get('pathParameters') else None
    
    if pokemon_id:
        response = table.get_item(Key={'id': pokemon_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(response['Item'], default=decimal_default)
            }
        else:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Pokemon not found'})
            }
    else:
        response = table.scan()
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response['Items'], default=decimal_default)
        }

def create_pokemon(event):
    data = json.loads(event['body'])
    pokemon = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'type': data['type'],
        'level': data.get('level', 1),
        'hp': data.get('hp', 100),
        'image': data.get('image', ''),
        'pokedexNumber': data.get('pokedexNumber', 0)
    }
    
    table.put_item(Item=pokemon)
    return {
        'statusCode': 201,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(pokemon, default=decimal_default)
    }

def update_pokemon(event):
    pokemon_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    
    response = table.update_item(
        Key={'id': pokemon_id},
        UpdateExpression='SET #name = :name, #type = :type, #level = :level, hp = :hp, image = :image, pokedexNumber = :pokedexNumber',
        ExpressionAttributeNames={
            '#name': 'name',
            '#type': 'type',
            '#level': 'level'
        },
        ExpressionAttributeValues={
            ':name': data['name'],
            ':type': data['type'],
            ':level': data.get('level', 1),
            ':hp': data.get('hp', 100),
            ':image': data.get('image', ''),
            ':pokedexNumber': data.get('pokedexNumber', 0)
        },
        ReturnValues='ALL_NEW'
    )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response['Attributes'], default=decimal_default)
    }

def delete_pokemon(event):
    pokemon_id = event['pathParameters']['id']
    table.delete_item(Key={'id': pokemon_id})
    
    return {
        'statusCode': 204,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': ''
    }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError