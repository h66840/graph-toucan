
import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock

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
    
    def _original_call_external_api(tool_name: str) -> dict:
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
    api_data = call_external_api("pokémcp-random-pokemon-from-region", **locals())
    
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

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
