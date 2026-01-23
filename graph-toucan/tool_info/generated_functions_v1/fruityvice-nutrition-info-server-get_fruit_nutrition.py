def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): the name of the fruit
        - family (str): the botanical family of the fruit
        - genus (str): the botanical genus of the fruit
        - order (str): the botanical order of the fruit
        - nutritions_calories (float): calories in the fruit
        - nutritions_fat (float): fat content in grams
        - nutritions_sugar (float): sugar content in grams
        - nutritions_carbohydrates (float): carbohydrate content in grams
        - nutritions_protein (float): protein content in grams
        - id (int): unique identifier for the fruit in the database
    """
    return {
        "name": "apple",
        "family": "Rosaceae",
        "genus": "Malus",
        "order": "Rosales",
        "nutritions_calories": 52.0,
        "nutritions_fat": 0.2,
        "nutritions_sugar": 10.0,
        "nutritions_carbohydrates": 13.8,
        "nutritions_protein": 0.3,
        "id": 1
    }


def fruityvice_nutrition_info_server_get_fruit_nutrition(fruit_name: str) -> dict:
    """
    Get nutritional information and details for a given fruit name.

    Args:
        fruit_name (str): The name of the fruit to get information about (e.g., "apple", "banana", "orange")

    Returns:
        Dictionary containing fruit information including name, family, genus, order, and nutritional data
        with keys: 'name', 'family', 'genus', 'order', 'nutritions' (dict with 'calories', 'fat', 'sugar',
        'carbohydrates', 'protein'), and 'id'.

    Raises:
        ValueError: If fruit_name is empty or not a string
    """
    if not fruit_name:
        raise ValueError("fruit_name cannot be empty")
    if not isinstance(fruit_name, str):
        raise ValueError("fruit_name must be a string")

    # Call external API to get flat data
    api_data = call_external_api("fruityvice-nutrition-info-server-get_fruit_nutrition")

    # Construct nested structure matching output schema
    result = {
        "name": api_data["name"],
        "family": api_data["family"],
        "genus": api_data["genus"],
        "order": api_data["order"],
        "nutritions": {
            "calories": api_data["nutritions_calories"],
            "fat": api_data["nutritions_fat"],
            "sugar": api_data["nutritions_sugar"],
            "carbohydrates": api_data["nutritions_carbohydrates"],
            "protein": api_data["nutritions_protein"]
        },
        "id": api_data["id"]
    }

    return result