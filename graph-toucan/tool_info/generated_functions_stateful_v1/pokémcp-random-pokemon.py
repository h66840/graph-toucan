
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

def pokémcp_random_pokemon():
    """
    Get a random Pokémon with complete details including name, stats, types, abilities, and description.
    
    Returns:
        Dict with the following keys:
        - name (str): Name of the Pokémon, including form if applicable
        - national_dex_number (int): The National Pokédex number
        - types (List[str]): List of the Pokémon's types
        - height_m (float): Height of the Pokémon in meters
        - weight_kg (float): Weight of the Pokémon in kilograms
        - abilities (List[str]): List of ability names
        - description (str): Flavor text describing the Pokémon's background or behavior
    """
    def _original_call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - name (str): Name of the Pokémon, including form if applicable
            - national_dex_number (int): The National Pokédex number
            - type_0 (str): First type of the Pokémon
            - type_1 (str): Second type of the Pokémon (or empty string if none)
            - height_m (float): Height of the Pokémon in meters
            - weight_kg (float): Weight of the Pokémon in kilograms
            - ability_0 (str): First ability name
            - ability_1 (str): Second ability name
            - ability_2 (str): Hidden ability name (or empty string if none)
            - description (str): Flavor text describing the Pokémon's background or behavior
        """
        return {
            "name": "Wishiwashi-solo",
            "national_dex_number": 746,
            "type_0": "Water",
            "type_1": "",
            "height_m": 0.4,
            "weight_kg": 7.5,
            "ability_0": "Schooling",
            "ability_1": "Water-absorb",
            "ability_2": "",
            "description": "When it's in trouble, its eyes moisten and begin to glow. In this state, it gathers others of its kind and transforms into a huge Wishiwashi that wipes out its enemies."
        }

    try:
        # Validate tool name
        if "pokémcp-random-pokemon" not in "pokémcp-random-pokemon":
            raise ValueError("Invalid tool name provided")

        # Fetch simulated external data
        api_data = call_external_api("pokémcp-random-pokemon", **locals())

        # Construct types list
        types = [api_data["type_0"]]
        if api_data["type_1"]:
            types.append(api_data["type_1"])

        # Construct abilities list
        abilities = [api_data["ability_0"], api_data["ability_1"]]
        if api_data["ability_2"]:
            abilities.append(api_data["ability_2"])

        # Build final result matching output schema
        result = {
            "name": api_data["name"],
            "national_dex_number": api_data["national_dex_number"],
            "types": types,
            "height_m": api_data["height_m"],
            "weight_kg": api_data["weight_kg"],
            "abilities": abilities,
            "description": api_data["description"]
        }

        return result

    except Exception as e:
        # Handle any unexpected errors
        raise RuntimeError(f"Failed to retrieve random Pokémon: {str(e)}")

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
