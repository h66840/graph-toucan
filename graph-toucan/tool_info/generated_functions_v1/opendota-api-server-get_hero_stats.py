from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for hero statistics.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hero_0_name (str): Name of the first hero
        - hero_0_win_rate (float): Win rate in percentage for the first hero
        - hero_0_roles (str): Comma-separated roles for the first hero
        - hero_0_primary_attribute (str): Primary attribute of the first hero
        - hero_0_attack_type (str): Attack type of the first hero
        - hero_0_win_rates_by_bracket (str): JSON-like string of win rates by bracket for the first hero
        - hero_0_pro_pick_rate (float): Pro pick rate of the first hero
        - hero_0_pro_win_rate (float): Pro win rate of the first hero
        - hero_0_pro_ban_rate (float): Pro ban rate of the first hero
        - hero_1_name (str): Name of the second hero
        - hero_1_win_rate (float): Win rate in percentage for the second hero
        - hero_1_roles (str): Comma-separated roles for the second hero
        - hero_1_primary_attribute (str): Primary attribute of the second hero
        - hero_1_attack_type (str): Attack type of the second hero
        - hero_1_win_rates_by_bracket (str): JSON-like string of win rates by bracket for the second hero
        - hero_1_pro_pick_rate (float): Pro pick rate of the second hero
        - hero_1_pro_win_rate (float): Pro win rate of the second hero
        - hero_1_pro_ban_rate (float): Pro ban rate of the second hero
    """
    return {
        "hero_0_name": "Anti-Mage",
        "hero_0_win_rate": 52.3,
        "hero_0_roles": "Carry,Escape,Nuker",
        "hero_0_primary_attribute": "agility",
        "hero_0_attack_type": "Melee",
        "hero_0_win_rates_by_bracket": '{"1": 51.2, "2": 52.1, "3": 53.4}',
        "hero_0_pro_pick_rate": 8.7,
        "hero_0_pro_win_rate": 54.6,
        "hero_0_pro_ban_rate": 12.3,
        "hero_1_name": "Pudge",
        "hero_1_win_rate": 49.8,
        "hero_1_roles": "Durable,Initiator,Disabler,Nuker",
        "hero_1_primary_attribute": "strength",
        "hero_1_attack_type": "Melee",
        "hero_1_win_rates_by_bracket": '{"1": 48.9, "2": 49.5, "3": 50.2}',
        "hero_1_pro_pick_rate": 6.5,
        "hero_1_pro_win_rate": 47.8,
        "hero_1_pro_ban_rate": 18.9,
    }

def opendota_api_server_get_hero_stats(hero_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get statistics for heroes from OpenDota API.
    
    Args:
        hero_id (Optional[int]): Optional hero ID to get stats for a specific hero.
                                 If None, returns stats for multiple heroes.
    
    Returns:
        List[Dict]: List of hero statistics, each containing:
            - name (str): Hero name
            - win_rate (float): Win rate in percentage
            - roles (Optional[List[str]]): List of roles the hero plays
            - primary_attribute (Optional[str]): Primary attribute of the hero
            - attack_type (Optional[str]): Attack type (Melee or Ranged)
            - win_rates_by_bracket (Optional[Dict[str, float]]): Win rates by skill bracket
            - pro_pick_rate (Optional[float]): Professional pick rate
            - pro_win_rate (Optional[float]): Professional win rate
            - pro_ban_rate (Optional[float]): Professional ban rate
    """
    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_hero_stats")
    
    # Construct the result list by mapping flat fields to nested structure
    heroes = []
    
    for i in range(2):  # We have two heroes in the simulated data
        hero_key_prefix = f"hero_{i}"
        
        # Only include specific hero if hero_id is provided (in this simulation, we ignore actual hero_id logic)
        # In real implementation, this would filter based on actual hero ID
        hero = {
            "name": api_data[f"{hero_key_prefix}_name"],
            "win_rate": api_data[f"{hero_key_prefix}_win_rate"],
            "roles": api_data[f"{hero_key_prefix}_roles"].split(",") if api_data.get(f"{hero_key_prefix}_roles") else None,
            "primary_attribute": api_data.get(f"{hero_key_prefix}_primary_attribute"),
            "attack_type": api_data.get(f"{hero_key_prefix}_attack_type"),
            "pro_pick_rate": api_data.get(f"{hero_key_prefix}_pro_pick_rate"),
            "pro_win_rate": api_data.get(f"{hero_key_prefix}_pro_win_rate"),
            "pro_ban_rate": api_data.get(f"{hero_key_prefix}_pro_ban_rate"),
        }
        
        # Parse win_rates_by_bracket from JSON-like string to dict
        win_rates_str = api_data.get(f"{hero_key_prefix}_win_rates_by_bracket")
        if win_rates_str:
            try:
                import json
                hero["win_rates_by_bracket"] = json.loads(win_rates_str)
            except (json.JSONDecodeError, TypeError):
                hero["win_rates_by_bracket"] = {}
        else:
            hero["win_rates_by_bracket"] = None
            
        heroes.append(hero)
    
    # If hero_id was specified, filter results (simulated - in real API this would affect the response)
    # Here we just return all since we don't have real IDs mapped
    return heroes