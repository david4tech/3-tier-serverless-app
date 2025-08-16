#!/usr/bin/env python3
"""
Local development server for Pokemon API
Simulates API Gateway + Lambda locally for testing
"""

import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os

# Add lambda directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lambda'))

# Mock DynamoDB for local development
MOCK_POKEMON_DATA = {}

class MockDynamoDBTable:
    def __init__(self, table_name):
        self.table_name = table_name
        
    def get_item(self, Key):
        pokemon_id = Key['id']
        if pokemon_id in MOCK_POKEMON_DATA:
            return {'Item': MOCK_POKEMON_DATA[pokemon_id]}
        return {}
    
    def scan(self):
        return {'Items': list(MOCK_POKEMON_DATA.values())}
    
    def put_item(self, Item):
        MOCK_POKEMON_DATA[Item['id']] = Item
        
    def update_item(self, Key, UpdateExpression, ExpressionAttributeNames, ExpressionAttributeValues, ReturnValues):
        pokemon_id = Key['id']
        if pokemon_id in MOCK_POKEMON_DATA:
            pokemon = MOCK_POKEMON_DATA[pokemon_id]
            pokemon.update({
                'name': ExpressionAttributeValues[':name'],
                'type': ExpressionAttributeValues[':type'],
                'level': ExpressionAttributeValues[':level'],
                'hp': ExpressionAttributeValues[':hp']
            })
            return {'Attributes': pokemon}
        return {}
    
    def delete_item(self, Key):
        pokemon_id = Key['id']
        if pokemon_id in MOCK_POKEMON_DATA:
            del MOCK_POKEMON_DATA[pokemon_id]

# Mock boto3 for local development
class MockBoto3:
    def resource(self, service_name):
        return MockDynamoDBResource()
    
    def __getattr__(self, name):
        return self

class MockDynamoDBResource:
    def Table(self, table_name):
        return MockDynamoDBTable(table_name)

# Mock boto3 before importing handler
sys.modules['boto3'] = MockBoto3()

# Import handler after mocking
import importlib.util
spec = importlib.util.spec_from_file_location("pokemon_handler", "lambda/pokemon_handler.py")
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)

class PokemonAPIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        event = {
            'httpMethod': 'GET',
            'pathParameters': None
        }
        
        if len(path_parts) == 2 and path_parts[0] == 'pokemons':
            event['pathParameters'] = {'id': path_parts[1]}
        
        response = handler.lambda_handler(event, {})
        
        self.send_response(response['statusCode'])
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response['body'].encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        event = {
            'httpMethod': 'POST',
            'body': post_data.decode('utf-8')
        }
        
        response = handler.lambda_handler(event, {})
        
        self.send_response(response['statusCode'])
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response['body'].encode())
    
    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        
        event = {
            'httpMethod': 'PUT',
            'pathParameters': {'id': path_parts[1]},
            'body': put_data.decode('utf-8')
        }
        
        response = handler.lambda_handler(event, {})
        
        self.send_response(response['statusCode'])
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response['body'].encode())
    
    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        event = {
            'httpMethod': 'DELETE',
            'pathParameters': {'id': path_parts[1]}
        }
        
        response = handler.lambda_handler(event, {})
        
        self.send_response(response['statusCode'])
        self._set_cors_headers()
        self.end_headers()

if __name__ == '__main__':
    # Add first 25 Pokemon
    first_25_pokemon = [
        {'name': 'Bulbasaur', 'type': 'Grass', 'level': 5, 'hp': 45, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png', 'pokedexNumber': 1},
        {'name': 'Ivysaur', 'type': 'Grass', 'level': 16, 'hp': 60, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png', 'pokedexNumber': 2},
        {'name': 'Venusaur', 'type': 'Grass', 'level': 32, 'hp': 80, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png', 'pokedexNumber': 3},
        {'name': 'Charmander', 'type': 'Fire', 'level': 5, 'hp': 39, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png', 'pokedexNumber': 4},
        {'name': 'Charmeleon', 'type': 'Fire', 'level': 16, 'hp': 58, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png', 'pokedexNumber': 5},
        {'name': 'Charizard', 'type': 'Fire', 'level': 36, 'hp': 78, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png', 'pokedexNumber': 6},
        {'name': 'Squirtle', 'type': 'Water', 'level': 5, 'hp': 44, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png', 'pokedexNumber': 7},
        {'name': 'Wartortle', 'type': 'Water', 'level': 16, 'hp': 59, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/8.png', 'pokedexNumber': 8},
        {'name': 'Blastoise', 'type': 'Water', 'level': 36, 'hp': 79, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png', 'pokedexNumber': 9},
        {'name': 'Caterpie', 'type': 'Bug', 'level': 3, 'hp': 45, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10.png', 'pokedexNumber': 10},
        {'name': 'Metapod', 'type': 'Bug', 'level': 7, 'hp': 50, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/11.png', 'pokedexNumber': 11},
        {'name': 'Butterfree', 'type': 'Bug', 'level': 10, 'hp': 60, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/12.png', 'pokedexNumber': 12},
        {'name': 'Weedle', 'type': 'Bug', 'level': 3, 'hp': 40, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/13.png', 'pokedexNumber': 13},
        {'name': 'Kakuna', 'type': 'Bug', 'level': 7, 'hp': 45, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/14.png', 'pokedexNumber': 14},
        {'name': 'Beedrill', 'type': 'Bug', 'level': 10, 'hp': 65, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/15.png', 'pokedexNumber': 15},
        {'name': 'Pidgey', 'type': 'Normal', 'level': 2, 'hp': 40, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/16.png', 'pokedexNumber': 16},
        {'name': 'Pidgeotto', 'type': 'Normal', 'level': 18, 'hp': 63, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/17.png', 'pokedexNumber': 17},
        {'name': 'Pidgeot', 'type': 'Normal', 'level': 36, 'hp': 83, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/18.png', 'pokedexNumber': 18},
        {'name': 'Rattata', 'type': 'Normal', 'level': 2, 'hp': 30, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/19.png', 'pokedexNumber': 19},
        {'name': 'Raticate', 'type': 'Normal', 'level': 20, 'hp': 55, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/20.png', 'pokedexNumber': 20},
        {'name': 'Spearow', 'type': 'Normal', 'level': 2, 'hp': 40, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/21.png', 'pokedexNumber': 21},
        {'name': 'Fearow', 'type': 'Normal', 'level': 20, 'hp': 65, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/22.png', 'pokedexNumber': 22},
        {'name': 'Ekans', 'type': 'Poison', 'level': 4, 'hp': 35, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/23.png', 'pokedexNumber': 23},
        {'name': 'Arbok', 'type': 'Poison', 'level': 22, 'hp': 60, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/24.png', 'pokedexNumber': 24},
        {'name': 'Pikachu', 'type': 'Electric', 'level': 5, 'hp': 35, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png', 'pokedexNumber': 25}
    ]
    
    for pokemon_data in first_25_pokemon:
        pokemon = {
            'id': str(uuid.uuid4()),
            **pokemon_data
        }
        MOCK_POKEMON_DATA[pokemon['id']] = pokemon
    
    server = HTTPServer(('localhost', 3001), PokemonAPIHandler)
    print('Starting local Pokemon API server on http://localhost:3001')
    print('Available endpoints:')
    print('  GET    /pokemons     - Get all Pokemon')
    print('  GET    /pokemons/id  - Get specific Pokemon')
    print('  POST   /pokemons     - Create new Pokemon')
    print('  PUT    /pokemons/id  - Update Pokemon')
    print('  DELETE /pokemons/id  - Delete Pokemon')
    server.serve_forever()