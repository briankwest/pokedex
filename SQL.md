### **SWAIG Functions with Corresponding SQL Queries**

#### **1. Get Pokémon Abilities**
- **SQL Query:**
```sql
SELECT pokemon.pok_id, pokemon.pok_name, abilities.abil_name
FROM pokemon
INNER JOIN pokemon_abilities
ON pokemon.pok_id = pokemon_abilities.pok_id
INNER JOIN abilities
ON pokemon_abilities.abil_id = abilities.abil_id
WHERE pokemon.pok_name LIKE var1;
```
- **Procedure:** `output_pokemon_abilities`

#### **2. Get Pokémon Base Stats**
- **SQL Query:**
```sql
SELECT base_stats.b_atk, base_stats.b_def, base_stats.b_hp, base_stats.b_sp_atk, base_stats.b_sp_def, base_stats.b_speed
FROM pokemon
INNER JOIN base_stats
ON pokemon.pok_id = base_stats.pok_id
WHERE pokemon.pok_name LIKE var1;
```
- **Procedure:** `output_pokemon_base_stats`

#### **3. Get Pokémon Evolution**
- **SQL Query:**
```sql
SELECT pokemon.pok_name, pokemon_evolution.evolved_species_id, pokemon_evolution.evol_minimum_level
FROM pokemon
INNER JOIN pokemon_evolution_matchup
ON pokemon.pok_id = pokemon_evolution_matchup.evolves_from_species_id
INNER JOIN pokemon_evolution
ON pokemon_evolution_matchup.pok_id = pokemon_evolution.evolved_species_id
WHERE pokemon.pok_id LIKE var1;
```
- **Procedure:** `output_pokemon_evol`

#### **4. Check if Pokémon Fainted**
- **SQL Query:**
```sql
SELECT pokemon.pok_id, pokemon.pok_name, moves.move_name
FROM pokemon
INNER JOIN base_stats
ON pokemon.pok_id = base_stats.pok_id
INNER JOIN pokemon_moves
ON pokemon.pok_id = pokemon_moves.pok_id
INNER JOIN moves
ON moves.move_name LIKE var1
WHERE pokemon.pok_name LIKE var2 AND moves.move_name LIKE var1 AND moves.move_power - base_stats.b_hp >= 0
GROUP BY pokemon.pok_id;
```
- **Procedure:** `output_pokemon_fainted`

#### **5. Get Pokémon Habitat**
- **SQL Query:**
```sql
SELECT pokemon.pok_id, pokemon.pok_name, pokemon_habitats.hab_name
FROM pokemon
INNER JOIN pokemon_evolution_matchup
ON pokemon.pok_id = pokemon_evolution_matchup.pok_id
INNER JOIN pokemon_habitats
ON pokemon_evolution_matchup.hab_id = pokemon_habitats.hab_id
WHERE pokemon_habitats.hab_name LIKE var1;
```
- **Procedure:** `output_pokemon_habitat`

#### **6. Get Pokémon Hidden Ability**
- **SQL Query:**
```sql
SELECT pokemon.pok_name, abilities.abil_name
FROM pokemon
INNER JOIN pokemon_abilities
ON pokemon.pok_id = pokemon_abilities.pok_id
INNER JOIN abilities
ON pokemon_abilities.abil_id = abilities.abil_id
WHERE pokemon.pok_name LIKE var1 AND pokemon_abilities.is_hidden = 1
GROUP BY abilities.abil_id;
```
- **Procedure:** `output_pokemon_hidden_abil`

#### **7. Get Pokémon Moves**
- **SQL Query:**
```sql
SELECT pokemon.pok_id, pokemon.pok_name, moves.move_name
FROM pokemon
INNER JOIN pokemon_moves
ON pokemon.pok_id = pokemon_moves.pok_id
INNER JOIN moves
ON pokemon_moves.move_id = moves.move_id
WHERE pokemon.pok_name LIKE var1;
```
- **Procedure:** `output_pokemon_moves`

#### **8. How Pokémon Learn a Move**
- **SQL Query:**
```sql
SELECT learning_method
FROM pokemon_move_learning
WHERE move_name = var1 AND pokemon_name = var2;
```
- **Procedure:** `output_pokemon_moves_method`

#### **9. Get Pokémon Move Type**
- **SQL Query:**
```sql
SELECT moves.move_name, types.type_name
FROM moves
INNER JOIN types
ON moves.type_id = types.type_id
WHERE moves.move_name LIKE var1;
```
- **Procedure:** `output_pokemon_moves_types`

#### **10. Get Move Damage Factor**
- **SQL Query:**
```sql
SELECT types.type_id, types.type_name, type_efficacy.damage_factor, type_efficacy.target_type_id
FROM types
INNER JOIN type_efficacy
ON types.damage_type_id = type_efficacy.damage_type_id
WHERE types.type_name LIKE var1;
```
- **Procedure:** `output_pokemon_type_efficacy`

#### **11. Get Pokémon Type**
- **SQL Query:**
```sql
SELECT pokemon.pok_id, pokemon.pok_name, types.type_name
FROM pokemon
INNER JOIN pokemon_types
ON pokemon.pok_id = pokemon_types.pok_id
INNER JOIN types
ON pokemon_types.type_id = types.type_id
WHERE types.type_name LIKE var1;
```
- **Procedure:** `output_pokemon_types`

---

### Summary of Queries & Functions

Each function corresponds to a SQL query and a stored procedure for retrieving specific Pokémon data (e.g., abilities, base stats, habitat, moves, etc.). The SQL queries leverage `INNER JOIN` operations to combine data from various related tables such as `pokemon`, `base_stats`, `abilities`, `moves`, etc.

For each SWAIG function, the corresponding stored procedure is executed with a `LIKE` clause, which allows for the dynamic querying of data based on the user's input (e.g., Pokémon name, type, or move).

### How to Use the Procedures
Each procedure defined in the SQL dump (e.g., `output_pokemon_types`, `output_pokemon_habitat`) should be called as follows:
```sql
CALL output_pokemon_types('charizard');
```

