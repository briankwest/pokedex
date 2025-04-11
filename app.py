from flask import Flask, request, jsonify
from signalwire_swaig.core import SWAIG, SWAIGArgument
from dotenv import load_dotenv
import os
import mysql.connector  # Changed from psycopg2 to mysql.connector

# Load environment variables
load_dotenv(override=True)

# Initialize Flask and SWAIG
app = Flask(__name__)
swaig = SWAIG(app)

# Database connection setup
def get_db_connection():
    conn = mysql.connector.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    conn.autocommit = True
    return conn

### 1. Get Pokemon Abilities
@swaig.endpoint("Get Pokemon Abilities",
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def get_pokemon_abilities(pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_id, pokemon.pok_name, abilities.abil_name
            FROM pokemon
            INNER JOIN pokemon_abilities
            ON pokemon.pok_id = pokemon_abilities.pok_id
            INNER JOIN abilities
            ON pokemon_abilities.abil_id = abilities.abil_id
            WHERE pokemon.pok_name LIKE %s
        """, (pokemon_name,))
        abilities = cursor.fetchall()
        if abilities:
            ability_names = [ability[2] for ability in abilities]
            response = f"{pokemon_name} has the following abilities: {', '.join(ability_names)}."
        else:
            response = f"No abilities found for {pokemon_name}."
    except Exception as e:
        response = f"An error occurred while fetching abilities: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 2. Get Pokemon Base Stats
@swaig.endpoint("Get Pokemon Base Stats",
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def get_pokemon_base_stats(pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT base_stats.b_atk, base_stats.b_def, base_stats.b_hp, base_stats.b_sp_atk, base_stats.b_sp_def, base_stats.b_speed
            FROM pokemon
            INNER JOIN base_stats
            ON pokemon.pok_id = base_stats.pok_id
            WHERE pokemon.pok_name LIKE %s
        """, (pokemon_name,))
        stats = cursor.fetchone()
        if stats:
            response = f"{pokemon_name}'s base stats: Attack: {stats[0]}, Defense: {stats[1]}, HP: {stats[2]}, Special Attack: {stats[3]}, Special Defense: {stats[4]}, Speed: {stats[5]}."
        else:
            response = f"No base stats found for {pokemon_name}."
    except Exception as e:
        response = f"An error occurred while fetching stats: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 3. Get Pokemon Evolution
@swaig.endpoint("Get Pokemon Evolution",
    pokemon_id=SWAIGArgument("integer", "The ID of the Pokemon", required=True))
def get_pokemon_evolution(pokemon_id, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_name, pokemon_evolution.evolved_species_id, pokemon_evolution.evol_minimum_level
            FROM pokemon
            INNER JOIN pokemon_evolution_matchup
            ON pokemon.pok_id = pokemon_evolution_matchup.evolves_from_species_id
            INNER JOIN pokemon_evolution
            ON pokemon_evolution_matchup.pok_id = pokemon_evolution.evolved_species_id
            WHERE pokemon.pok_id LIKE %s
        """, (pokemon_id,))
        evolutions = cursor.fetchall()
        if evolutions:
            evolution_info = []
            for evolution in evolutions:
                pokemon_name = evolution[0]
                evolved_id = evolution[1]
                min_level = evolution[2]
                level_info = f" at level {min_level}" if min_level else ""
                evolution_info.append(f"{pokemon_name} evolves to Pokémon ID {evolved_id}{level_info}")
            response = "; ".join(evolution_info)
        else:
            response = f"No evolution data found for Pokémon ID {pokemon_id}."
    except Exception as e:
        response = f"An error occurred while fetching evolution: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 4. Check if Pokemon Fainted
@swaig.endpoint("Check if Pokemon Fainted",
    move_name=SWAIGArgument("string", "The move used"),
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def check_if_pokemon_fainted(move_name, pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_id, pokemon.pok_name, moves.move_name
            FROM pokemon
            INNER JOIN base_stats
            ON pokemon.pok_id = base_stats.pok_id
            INNER JOIN pokemon_moves
            ON pokemon.pok_id = pokemon_moves.pok_id
            INNER JOIN moves
            ON moves.move_name LIKE %s
            WHERE pokemon.pok_name LIKE %s AND moves.move_name LIKE %s AND moves.move_power - base_stats.b_hp >= 0
            GROUP BY pokemon.pok_id
        """, (move_name, pokemon_name, move_name))
        result = cursor.fetchone()
        if result:
            response = f"{pokemon_name} has fainted after using {move_name}."
        else:
            response = f"{pokemon_name} did not faint after using {move_name}."
    except Exception as e:
        response = f"An error occurred while checking faint status: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 5. Get Pokemon Habitat
@swaig.endpoint("Get Pokemon Habitat",
    habitat=SWAIGArgument("string", "The habitat name", required=True))
def get_pokemon_habitat(habitat, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_id, pokemon.pok_name, pokemon_habitats.hab_name
            FROM pokemon
            INNER JOIN pokemon_evolution_matchup
            ON pokemon.pok_id = pokemon_evolution_matchup.pok_id
            INNER JOIN pokemon_habitats
            ON pokemon_evolution_matchup.hab_id = pokemon_habitats.hab_id
            WHERE pokemon_habitats.hab_name LIKE %s
        """, (habitat,))
        pokemon_in_habitat = cursor.fetchall()
        if pokemon_in_habitat:
            pokemon_names = [pokemon[1] for pokemon in pokemon_in_habitat]
            response = f"Pokemon in {habitat} habitat: {', '.join(pokemon_names)}."
        else:
            response = f"No Pokemon found in {habitat} habitat."
    except Exception as e:
        response = f"An error occurred while fetching habitat data: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 6. Get Pokemon Hidden Ability
@swaig.endpoint("Get Pokemon Hidden Ability",
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def get_pokemon_hidden_ability(pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_name, abilities.abil_name
            FROM pokemon
            INNER JOIN pokemon_abilities
            ON pokemon.pok_id = pokemon_abilities.pok_id
            INNER JOIN abilities
            ON pokemon_abilities.abil_id = abilities.abil_id
            WHERE pokemon.pok_name LIKE %s AND pokemon_abilities.is_hidden = 1
            GROUP BY abilities.abil_id
        """, (pokemon_name,))
        hidden_ability = cursor.fetchone()
        if hidden_ability:
            response = f"{pokemon_name}'s hidden ability is {hidden_ability[1]}."
        else:
            response = f"No hidden ability found for {pokemon_name}."
    except Exception as e:
        response = f"An error occurred while fetching hidden ability: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 7. Get Pokemon Moves
@swaig.endpoint("Get Pokemon Moves",
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def get_pokemon_moves(pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_id, pokemon.pok_name, moves.move_name
            FROM pokemon
            INNER JOIN pokemon_moves
            ON pokemon.pok_id = pokemon_moves.pok_id
            INNER JOIN moves
            ON pokemon_moves.move_id = moves.move_id
            WHERE pokemon.pok_name LIKE %s
        """, (pokemon_name,))
        moves = cursor.fetchall()
        if moves:
            move_names = [move[2] for move in moves]
            response = f"{pokemon_name} can learn the following moves: {', '.join(move_names)}."
        else:
            response = f"No moves found for {pokemon_name}."
    except Exception as e:
        response = f"An error occurred while fetching moves: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 8. How Pokemon Learn a Move
@swaig.endpoint("How Pokemon Learn a Move",
    move=SWAIGArgument("string", "The move name"),
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def how_pokemon_learn_move(move, pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT learning_method
            FROM pokemon_move_learning
            WHERE move_name = %s AND pokemon_name = %s
        """, (move, pokemon_name))
        learning_method = cursor.fetchone()
        if learning_method:
            response = f"{pokemon_name} learns {move} by {learning_method[0]}."
        else:
            response = f"{pokemon_name} does not learn {move}."
    except Exception as e:
        response = f"An error occurred while fetching learning method: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 9. Get Pokemon Move Type
@swaig.endpoint("Get Pokemon Move Type",
    move_name=SWAIGArgument("string", "The move name", required=True))
def get_pokemon_move_type(move_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT moves.move_name, types.type_name
            FROM moves
            INNER JOIN types
            ON moves.type_id = types.type_id
            WHERE moves.move_name LIKE %s
        """, (move_name,))
        move_type = cursor.fetchone()
        if move_type:
            response = f"{move_name} is a {move_type[1]}-type move."
        else:
            response = f"No type found for move {move_name}."
    except Exception as e:
        response = f"An error occurred while fetching move type: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 10. Get Move Damage Factor
@swaig.endpoint("Get Move Damage Factor",
    move_type=SWAIGArgument("string", "The move type", required=True))
def get_move_damage_factor(move_type, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT types.type_id, types.type_name, type_efficacy.damage_factor, type_efficacy.target_type_id
            FROM types
            INNER JOIN type_efficacy
            ON types.damage_type_id = type_efficacy.damage_type_id
            WHERE types.type_name LIKE %s
        """, (move_type,))
        damage_factors = cursor.fetchall()
        if damage_factors:
            damage_info = []
            for factor in damage_factors:
                damage_info.append(f"Against target type ID {factor[3]}: {factor[2]}")
            response = f"Damage factors for {move_type}-type moves: {'; '.join(damage_info)}."
        else:
            response = f"No damage factor found for {move_type}-type moves."
    except Exception as e:
        response = f"An error occurred while fetching damage factor: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

### 11. Get Pokemon Type
@swaig.endpoint("Get Pokemon Type",
    pokemon_name=SWAIGArgument("string", "The name of the Pokemon", required=True))
def get_pokemon_type(pokemon_name, meta_data_token=None, meta_data=None):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("""
            SELECT pokemon.pok_id, pokemon.pok_name, types.type_name
            FROM pokemon
            INNER JOIN pokemon_types
            ON pokemon.pok_id = pokemon_types.pok_id
            INNER JOIN types
            ON pokemon_types.type_id = types.type_id
            WHERE pokemon.pok_name LIKE %s
        """, (pokemon_name,))
        pokemon_types = cursor.fetchall()
        if pokemon_types:
            type_names = [pokemon_type[2] for pokemon_type in pokemon_types]
            response = f"{pokemon_name} is a {'/'.join(type_names)}-type Pokemon."
        else:
            response = f"No type found for {pokemon_name}."
    except Exception as e:
        response = f"An error occurred while fetching Pokemon type: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    return response, {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG', False))
