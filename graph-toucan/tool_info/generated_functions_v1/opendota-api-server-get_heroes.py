from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Dota 2 heroes.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hero_0_name (str): Name of the first hero
        - hero_0_id (int): ID of the first hero
        - hero_0_primary_attribute (str): Primary attribute of the first hero
        - hero_0_attack_type (str): Attack type of the first hero
        - hero_0_role_0 (str): First role of the first hero
        - hero_0_role_1 (str): Second role of the first hero
        - hero_1_name (str): Name of the second hero
        - hero_1_id (int): ID of the second hero
        - hero_1_primary_attribute (str): Primary attribute of the second hero
        - hero_1_attack_type (str): Attack type of the second hero
        - hero_1_role_0 (str): First role of the second hero
        - hero_1_role_1 (str): Second role of the second hero
    """
    return {
        "hero_0_name": "Anti-Mage",
        "hero_0_id": 1,
        "hero_0_primary_attribute": "agility",
        "hero_0_attack_type": "Melee",
        "hero_0_role_0": "Carry",
        "hero_0_role_1": "Escape",
        "hero_1_name": "Axe",
        "hero_1_id": 2,
        "hero_1_primary_attribute": "strength",
        "hero_1_attack_type": "Melee",
        "hero_1_role_0": "Initiator",
        "hero_1_role_1": "Durable",
    }

def opendota_api_server_get_heroes() -> List[Dict[str, Any]]:
    """
    Get list of all Dota 2 heroes.

    Returns:
        List of all heroes with basic information. Each hero contains:
        - name (str): Hero's name
        - id (int): Hero's unique identifier
        - primary_attribute (str): Primary attribute (e.g., strength, agility, intelligence)
        - attack_type (str): Attack type (Melee or Ranged)
        - roles (List[str]): List of roles the hero typically plays
    """
    try:
        api_data = call_external_api("opendota-api-server-get_heroes")
        
        heroes = []
        
        # Construct first hero
        hero_0 = {
            "name": api_data["hero_0_name"],
            "id": api_data["hero_0_id"],
            "primary_attribute": api_data["hero_0_primary_attribute"],
            "attack_type": api_data["hero_0_attack_type"],
            "roles": [
                api_data["hero_0_role_0"],
                api_data["hero_0_role_1"]
            ]
        }
        heroes.append(hero_0)
        
        # Construct second hero
        hero_1 = {
            "name": api_data["hero_1_name"],
            "id": api_data["hero_1_id"],
            "primary_attribute": api_data["hero_1_primary_attribute"],
            "attack_type": api_data["hero_1_attack_type"],
            "roles": [
                api_data["hero_1_role_0"],
                api_data["hero_1_role_1"]
            ]
        }
        heroes.append(hero_1)
        
        return heroes
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve heroes data: {str(e)}")