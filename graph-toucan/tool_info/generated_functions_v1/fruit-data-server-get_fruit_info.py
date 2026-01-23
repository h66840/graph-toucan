from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching fruit data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): the name of the fruit
        - id (int): unique identifier for the fruit in the database
        - family (str): botanical family of the fruit
        - order (str): taxonomic order of the fruit
        - genus (str): biological genus of the fruit
        - nutritions_calories (float): calories in the fruit
        - nutritions_fat (float): fat content in grams
        - nutritions_sugar (float): sugar content in grams
        - nutritions_carbohydrates (float): carbohydrate content in grams
        - nutritions_protein (float): protein content in grams
    """
    return {
        "name": "Apple",
        "id": 123,
        "family": "Rosaceae",
        "order": "Rosales",
        "genus": "Malus",
        "nutritions_calories": 52.0,
        "nutritions_fat": 0.2,
        "nutritions_sugar": 10.0,
        "nutritions_carbohydrates": 14.0,
        "nutritions_protein": 0.3
    }

def fruit_data_server_get_fruit_info(name: str) -> Dict[str, Any]:
    """
    Kullanıcıdan alınan meyve ismine göre Fruityvice API'den detayları getirir.
    
    Args:
        name (str): the name of the fruit to retrieve information for
    
    Returns:
        Dict containing detailed fruit information with the following structure:
        - name (str): the name of the fruit
        - id (int): unique identifier for the fruit in the database
        - family (str): botanical family of the fruit
        - order (str): taxonomic order of the fruit
        - genus (str): biological genus of the fruit
        - nutritions (Dict): contains nutritional information with keys 'calories', 'fat', 'sugar', 'carbohydrates', 'protein'
    
    Raises:
        ValueError: If the name parameter is empty or not a string
    """
    if not name or not isinstance(name, str):
        raise ValueError("Name parameter must be a non-empty string")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("fruit-data-server-get_fruit_info")
    
    # Construct the result with proper nested structure
    result = {
        "name": api_data["name"],
        "id": api_data["id"],
        "family": api_data["family"],
        "order": api_data["order"],
        "genus": api_data["genus"],
        "nutritions": {
            "calories": api_data["nutritions_calories"],
            "fat": api_data["nutritions_fat"],
            "sugar": api_data["nutritions_sugar"],
            "carbohydrates": api_data["nutritions_carbohydrates"],
            "protein": api_data["nutritions_protein"]
        }
    }
    
    return result