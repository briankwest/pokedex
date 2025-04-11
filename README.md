### **Table of Contents**

1. [Introduction](#introduction)
2. [Overview](#overview)
3. [Functions/Capabilities](#functions-capabilities)
   - [Get Pokémon Abilities](#get-pokemon-abilities)
   - [Get Pokémon Base Stats](#get-pokemon-base-stats)
   - [Get Pokémon Evolution](#get-pokemon-evolution)
   - [Check if Pokémon Fainted](#check-if-pokemon-fainted)
   - [Get Pokémon Habitat](#get-pokemon-habitat)
   - [Get Pokémon Hidden Ability](#get-pokemon-hidden-ability)
   - [Get Pokémon Moves](#get-pokemon-moves)
   - [How Pokémon Learn a Move](#how-pokemon-learn-a-move)
   - [Get Pokémon Move Type](#get-pokemon-move-type)
   - [Get Move Damage Factor](#get-move-damage-factor)
   - [Get Pokémon Type](#get-pokemon-type)
4. [Environment Variables](#environment-variables)
5. [Sample Prompt for the AI Agent](#sample-prompt-for-the-ai-agent)
6. [Conclusion](#conclusion)
7. [Appendix](#appendix)

---

### **Introduction**

This AI Agent integrates SignalWire AI Gateway (SWAIG) to enable users to retrieve detailed information about Pokémon based on the Pokedex. The agent handles requests to retrieve various Pokémon-related data, such as abilities, stats, types, and moves.

### **Overview**

The AI Agent works as a middleware between the user and the Pokedex API. It leverages SignalWire's SWAIG to handle function calls and return human-readable responses. The agent can handle requests like identifying a Pokémon's abilities, moves, stats, and more, based on the Pokémon’s name or ID.

---

### **Functions/Capabilities**

Each function described below is intended to interact with the Pokémon database. The agent will return results in human-readable format to the user.

#### **Get Pokémon Abilities**
- **Input:** Pokémon's name
- **Output:** List of abilities

```json
{
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu has the abilities: Static, Lightning Rod."
}
```

#### **Get Pokémon Base Stats**
- **Input:** Pokémon's name
- **Output:** Base stats (e.g., attack, defense, hp)

```json
{
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu's base stats: HP: 35, Attack: 55, Defense: 40, Speed: 90."
}
```

#### **Get Pokémon Evolution**
- **Input:** Pokémon's ID
- **Output:** Name and evolution chain

```json
{
  "pokemon_id": 25
}
```

Example Output:
```json
{
  "response": "Pikachu evolves into Pichu and Raichu."
}
```

#### **Check if Pokémon Fainted**
- **Input:** Move name, Pokémon name
- **Output:** Whether the Pokémon has fainted (true/false)

```json
{
  "move": "Thunderbolt",
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu did not faint."
}
```

#### **Get Pokémon Habitat**
- **Input:** Habitat name
- **Output:** List of Pokémon in that habitat

```json
{
  "habitat": "forest"
}
```

Example Output:
```json
{
  "response": "Pokémon in the forest habitat: Pikachu, Bulbasaur, Charmander."
}
```

#### **Get Pokémon Hidden Ability**
- **Input:** Pokémon's name
- **Output:** Hidden ability

```json
{
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu's hidden ability is Lightning Rod."
}
```

#### **Get Pokémon Moves**
- **Input:** Pokémon's name
- **Output:** List of moves

```json
{
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu can learn the following moves: Quick Attack, Thunderbolt, Electro Ball."
}
```

#### **How Pokémon Learn a Move**
- **Input:** Pokémon move name, Pokémon name
- **Output:** Method of learning the move

```json
{
  "move": "Thunderbolt",
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu learns Thunderbolt via leveling up."
}
```

#### **Get Pokémon Move Type**
- **Input:** Move name
- **Output:** Type of the move

```json
{
  "move": "Thunderbolt"
}
```

Example Output:
```json
{
  "response": "Thunderbolt is an Electric-type move."
}
```

#### **Get Move Damage Factor**
- **Input:** Move type
- **Output:** Damage factor

```json
{
  "type": "Electric"
}
```

Example Output:
```json
{
  "response": "Electric-type moves have a damage factor of 1.5."
}
```

#### **Get Pokémon Type**
- **Input:** Pokémon's name
- **Output:** Pokémon's type

```json
{
  "pokemon_name": "Pikachu"
}
```

Example Output:
```json
{
  "response": "Pikachu is an Electric-type Pokémon."
}
```

---

### **Environment Variables**

Ensure to set up the following environment variables for smooth functioning of the AI Agent:

```ini
SIGNALWIRE_PROJECT=your_project_id
SIGNALWIRE_TOKEN=your_auth_token
POKEDEX_API_URL=https://your-pokedex-api.com
```

Make sure these environment variables are managed securely, and don’t expose them in public repositories.

---

### **Sample Prompt for the AI Agent**

```
You are an AI assistant capable of retrieving real-time Pokémon information using SWAIG functions. Your responses must be accurate, human-readable, and formatted to assist users effectively.
```

---

### **Conclusion**

This AI Agent, powered by SignalWire's SWAIG, provides a robust interface for users to interact with Pokémon data. By leveraging the Pokedex API, users can query information about Pokémon abilities, stats, types, and moves with ease.

---

### **Appendix**

- **API Compliance:** Ensure that all functions comply with the Pokémon database API's rate limits and data structure.
- **Error Handling:** Ensure that the AI Agent returns appropriate error messages in a human-readable format if the API request fails or the query is invalid.
- **Rate Limiting:** Handle rate-limiting issues gracefully, alerting users when requests exceed the allowed rate.

---