def pokémcp_random_pokemon_from_region(region: str) -> dict:
    """
    Get a random Pokémon from a specific region.
    
    Args:
        region (str): The Pokémon region (e.g., kanto, johto, hoenn, etc.). Required.
    
    Returns:
        dict: Information about the randomly selected Pokémon with the following keys:
            - name (str): Name of the Pokémon
            - pokedex_number (int): National Pokédex number
            - region (str): Region from which the Pokémon originates
            - types (List[str]): List of the Pokémon's types
            - height (float): Height in meters
            - weight (float): Weight in kilograms
            - abilities (List[str]): List of the Pokémon's abilities
            - description (str): Descriptive flavor text about the Pokémon
    
    Raises:
        ValueError: If region is not provided or empty.
    """
    if not region or not region.strip():
        raise ValueError("Parameter 'region' is required and cannot be empty.")
    
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API for Pokémon information.
        
        Returns:
            Dict with simple scalar fields only (str, int, float, bool):
            - name (str): Name of the Pokémon
            - pokedex_number (int): National Pokédex number
            - region (str): Region name
            - types_0 (str): First type of the Pokémon
            - types_1 (str): Second type of the Pokémon (if applicable, otherwise empty string)
            - height (float): Height in meters
            - weight (float): Weight in kilograms
            - abilities_0 (str): First ability of the Pokémon
            - abilities_1 (str): Second ability of the Pokémon
            - description (str): Flavor text description
        """
        # Simulated response data based on tool name
        if tool_name == "pokémcp-random-pokemon-from-region":
            return {
                "name": "Pikachu",
                "pokedex_number": 25,
                "region": region.strip().lower(),
                "types_0": "Electric",
                "types_1": "",
                "height": 0.4,
                "weight": 6.0,
                "abilities_0": "Static",
                "abilities_1": "Lightning Rod",
                "description": "When several of these Pokémon gather, their electricity could build and cause lightning storms."
            }
        return {}
    
    # Fetch simulated API data
    api_data = call_external_api("pokémcp-random-pokemon-from-region")
    
    # Construct types list
    types = [api_data["types_0"]]
    if api_data["types_1"]:
        types.append(api_data["types_1"])
    
    # Construct abilities list
    abilities = [api_data["abilities_0"], api_data["abilities_1"]]
    
    # Build final result matching output schema
    result = {
        "name": api_data["name"],
        "pokedex_number": api_data["pokedex_number"],
        "region": api_data["region"],
        "types": types,
        "height": api_data["height"],
        "weight": api_data["weight"],
        "abilities": abilities,
        "description": api_data["description"]
    }
    
    return result