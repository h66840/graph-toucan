from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for meal search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - meal_name (str): Name of the meal if found
        - category (str): Category or type of the meal
        - area (str): Geographic origin or regional cuisine
        - instructions (str): Step-by-step cooking instructions
        - image (str): URL to an image of the prepared meal
        - error (str): Error message if meal not found or issue occurred
    """
    return {
        "meal_name": "Spaghetti Carbonara",
        "category": "Pasta",
        "area": "Italian",
        "instructions": "1. Cook spaghetti in salted boiling water until al dente. "
                       "2. In a pan, cook diced pancetta until crispy. "
                       "3. In a bowl, whisk eggs and mix with grated Parmesan cheese. "
                       "4. Drain spaghetti and add to pancetta pan. Remove from heat. "
                       "5. Stir in egg and cheese mixture, mixing quickly to avoid scrambling. "
                       "6. Season with black pepper and serve immediately. Nutritional info: 580 kcal per serving.",
        "image": "https://example.com/images/spaghetti_carbonara.jpg",
        "error": ""
    }

def recipe_assistant_server_search_meal(meal_name: str) -> Dict[str, Any]:
    """
    Search for a meal by name and return cooking instructions.
    
    This function simulates querying an external recipe database to retrieve
    details about a specific meal including its category, origin, cooking instructions,
    and image. If the meal is not found, an error message is returned.
    
    Args:
        meal_name (str): The name of the meal to search for.
        
    Returns:
        Dict containing the following keys:
            - meal_name (str): Name of the meal if found
            - category (str): Category or type of the meal (e.g., Pasta, Dessert)
            - area (str): Geographic origin or regional cuisine (e.g., American, Italian)
            - instructions (str): Step-by-step cooking instructions including ingredient combinations,
                                 cooking methods, and nutritional information if provided
            - image (str): URL to an image of the prepared meal
            - error (str): Error message indicating that the meal was not found or another issue occurred
    """
    if not meal_name or not meal_name.strip():
        return {
            "meal_name": "",
            "category": "",
            "area": "",
            "instructions": "",
            "image": "",
            "error": "Meal name is required."
        }
    
    # Simulate external API call
    api_data = call_external_api("recipe-assistant-server-search_meal")
    
    # Construct result matching output schema
    result = {
        "meal_name": api_data["meal_name"],
        "category": api_data["category"],
        "area": api_data["area"],
        "instructions": api_data["instructions"],
        "image": api_data["image"],
        "error": api_data["error"]
    }
    
    # Simple simulation of search logic: return mock data only if query matches closely
    if meal_name.strip().lower() not in api_data["meal_name"].lower():
        result.update({
            "meal_name": "",
            "category": "",
            "area": "",
            "instructions": "",
            "image": "",
            "error": f"Meal '{meal_name}' not found."
        })
    
    return result