def pokémcp_random_pokemon_by_type(type: str) -> dict:
    """
    Get a random Pokémon of a specific type.
    
    Args:
        type (str): The Pokémon type (e.g., fire, water, grass, etc.). Must be a valid Pokémon type.
    
    Returns:
        dict: A dictionary containing the following keys:
            - name (str): Name of the random Pokémon
            - pokedex_number (int): National Pokédex number of the Pokémon
            - types (List[str]): List of the Pokémon's types (e.g., ['Psychic'], ['Grass', 'Dark'])
            - height (float): Height of the Pokémon in meters
            - weight (float): Weight of the Pokémon in kilograms
            - abilities (List[str]): List of the Pokémon's abilities
            - description (str): Flavor description of the Pokémon, including behavioral or ecological traits
            - success (bool): Whether the request was successful
            - error_message (str): Error message if success is False, otherwise empty string
    """
    # Input validation
    valid_types = {
        "normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison",
        "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
    }
    
    if not type or not isinstance(type, str):
        return {
            "name": "",
            "pokedex_number": 0,
            "types": [],
            "height": 0.0,
            "weight": 0.0,
            "abilities": [],
            "description": "",
            "success": False,
            "error_message": "Type must be a non-empty string."
        }
    
    type_lower = type.strip().lower()
    if type_lower not in valid_types:
        return {
            "name": "",
            "pokedex_number": 0,
            "types": [],
            "height": 0.0,
            "weight": 0.0,
            "abilities": [],
            "description": "",
            "success": False,
            "error_message": f"Invalid Pokémon type: '{type}'. Valid types are {sorted(valid_types)}."
        }

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API for a random Pokémon by type.
        
        Returns:
            Dict with simple fields only (str, int, float, bool):
            - name (str): Pokémon name
            - pokedex_number (int): National Pokédex number
            - type_0 (str): First type of the Pokémon
            - type_1 (str): Second type of the Pokémon (or empty if none)
            - height (float): Height in meters
            - weight (float): Weight in kilograms
            - ability_0 (str): First ability
            - ability_1 (str): Second ability
            - description (str): Flavor text description
            - success (bool): Whether retrieval was successful
            - error_message (str): Error message if any
        """
        # Mock data based on input type
        mock_data = {
            "fire": {
                "name": "Charmander",
                "pokedex_number": 4,
                "type_0": "fire",
                "type_1": "",
                "height": 0.6,
                "weight": 8.5,
                "ability_0": "Blaze",
                "ability_1": "Solar Power",
                "description": "Charmander is a small, bipedal lizard-like Pokémon. It has orange skin and a flame burning at the tip of its tail.",
                "success": True,
                "error_message": ""
            },
            "water": {
                "name": "Squirtle",
                "pokedex_number": 7,
                "type_0": "water",
                "type_1": "",
                "height": 0.5,
                "weight": 9.0,
                "ability_0": "Torrent",
                "ability_1": "Rain Dish",
                "description": "Squirtle is a small turtle Pokémon. It has blue skin and a brown shell on its back.",
                "success": True,
                "error_message": ""
            },
            "grass": {
                "name": "Bulbasaur",
                "pokedex_number": 1,
                "type_0": "grass",
                "type_1": "poison",
                "height": 0.7,
                "weight": 6.9,
                "ability_0": "Overgrow",
                "ability_1": "Chlorophyll",
                "description": "Bulbasaur is a small, quadruped Pokémon with green skin and a large plant bulb on its back.",
                "success": True,
                "error_message": ""
            }
        }
        
        # Default fallback
        data = mock_data.get(type_lower, mock_data["grass"])
        return data.copy()

    try:
        # Call external API simulation
        api_data = call_external_api("pokémcp-random-pokemon-by-type")
        
        # Construct nested output structure
        result = {
            "name": api_data["name"],
            "pokedex_number": api_data["pokedex_number"],
            "types": [api_data["type_0"]],
            "height": api_data["height"],
            "weight": api_data["weight"],
            "abilities": [api_data["ability_0"]],
            "description": api_data["description"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        # Add second type if exists
        if api_data["type_1"]:
            result["types"].append(api_data["type_1"])
            
        # Add second ability if exists
        if api_data["ability_1"]:
            result["abilities"].append(api_data["ability_1"])
            
        return result
        
    except Exception as e:
        return {
            "name": "",
            "pokedex_number": 0,
            "types": [],
            "height": 0.0,
            "weight": 0.0,
            "abilities": [],
            "description": "",
            "success": False,
            "error_message": f"Internal error occurred: {str(e)}"
        }