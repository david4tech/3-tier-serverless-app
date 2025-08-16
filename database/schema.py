"""
Pokemon Database Schema Documentation

This module defines the complete schema for the Pokemon application database.
All tables use DynamoDB as the underlying storage.

Tables:
1. PokemonTable - Main pokemon data
2. PokemonTypesTable - Pokemon type reference data
3. PokemonAbilitiesTable - Pokemon abilities reference data
4. PokemonStatsTable - Detailed pokemon statistics
"""

# Pokemon Table Schema
POKEMON_SCHEMA = {
    "table_name": "PokemonTable",
    "partition_key": "id",  # UUID string
    "attributes": {
        "id": "string",           # Primary key - UUID
        "name": "string",         # Pokemon name
        "type": "string",         # Primary type
        "secondary_type": "string",  # Optional secondary type
        "level": "number",        # Pokemon level (1-100)
        "hp": "number",          # Hit points
        "attack": "number",      # Attack stat
        "defense": "number",     # Defense stat
        "speed": "number",       # Speed stat
        "abilities": "list",     # List of ability IDs
        "created_at": "string",  # ISO timestamp
        "updated_at": "string",  # ISO timestamp
        "trainer_id": "string",  # Optional trainer reference
        "is_shiny": "boolean",   # Shiny variant flag
        "gender": "string",      # Male/Female/Unknown
        "nature": "string",      # Pokemon nature
        "experience": "number",  # Experience points
        "moves": "list"          # List of move names
    }
}

# Pokemon Types Table Schema
TYPES_SCHEMA = {
    "table_name": "PokemonTypesTable",
    "partition_key": "type_name",
    "attributes": {
        "type_name": "string",      # Primary key - type name
        "color": "string",          # Type color for UI
        "strengths": "list",        # Types this is strong against
        "weaknesses": "list",       # Types this is weak against
        "immunities": "list",       # Types this is immune to
        "description": "string"     # Type description
    }
}

# Pokemon Abilities Table Schema
ABILITIES_SCHEMA = {
    "table_name": "PokemonAbilitiesTable",
    "partition_key": "ability_id",
    "attributes": {
        "ability_id": "string",     # Primary key - UUID
        "name": "string",           # Ability name
        "description": "string",    # Ability description
        "effect": "string",         # Game effect description
        "is_hidden": "boolean",     # Hidden ability flag
        "generation": "number"      # Generation introduced
    }
}

# Pokemon Stats Table Schema
STATS_SCHEMA = {
    "table_name": "PokemonStatsTable",
    "partition_key": "pokemon_id",
    "sort_key": "stat_name",
    "attributes": {
        "pokemon_id": "string",     # Foreign key to Pokemon
        "stat_name": "string",      # hp, attack, defense, sp_attack, sp_defense, speed
        "base_value": "number",     # Base stat value
        "current_value": "number",  # Current stat value (with modifiers)
        "iv": "number",            # Individual Value (0-31)
        "ev": "number",            # Effort Value (0-255)
        "modifier": "number"        # Temporary modifier
    }
}

# Sample data for initial seeding
SAMPLE_TYPES = [
    {
        "type_name": "Fire",
        "color": "#FF6666",
        "strengths": ["Grass", "Ice", "Bug", "Steel"],
        "weaknesses": ["Water", "Ground", "Rock"],
        "immunities": [],
        "description": "Fire-type Pokemon are known for their fiery attacks"
    },
    {
        "type_name": "Water",
        "color": "#6666FF",
        "strengths": ["Fire", "Ground", "Rock"],
        "weaknesses": ["Electric", "Grass"],
        "immunities": [],
        "description": "Water-type Pokemon excel in aquatic environments"
    },
    {
        "type_name": "Grass",
        "color": "#66FF66",
        "strengths": ["Water", "Ground", "Rock"],
        "weaknesses": ["Fire", "Ice", "Poison", "Flying", "Bug"],
        "immunities": [],
        "description": "Grass-type Pokemon harness the power of nature"
    },
    {
        "type_name": "Electric",
        "color": "#FFFF66",
        "strengths": ["Water", "Flying"],
        "weaknesses": ["Ground"],
        "immunities": [],
        "description": "Electric-type Pokemon generate electrical energy"
    }
]

SAMPLE_ABILITIES = [
    {
        "ability_id": "blaze",
        "name": "Blaze",
        "description": "Powers up Fire-type moves when HP is low",
        "effect": "Increases Fire-type move power by 50% when HP is below 1/3",
        "is_hidden": False,
        "generation": 3
    },
    {
        "ability_id": "torrent",
        "name": "Torrent",
        "description": "Powers up Water-type moves when HP is low",
        "effect": "Increases Water-type move power by 50% when HP is below 1/3",
        "is_hidden": False,
        "generation": 3
    },
    {
        "ability_id": "overgrow",
        "name": "Overgrow",
        "description": "Powers up Grass-type moves when HP is low",
        "effect": "Increases Grass-type move power by 50% when HP is below 1/3",
        "is_hidden": False,
        "generation": 3
    }
]