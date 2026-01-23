from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cultural heritage collections.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - collection_name (str): Name of the cultural institution's collection
        - items_count (int): Total number of items found in the collection
        - item_0_title (str): Title of the first cultural item
        - item_0_artist (str): Artist of the first cultural item
        - item_0_year (int): Year of creation for the first cultural item
        - item_0_type (str): Type/category of the first cultural item
        - item_0_id (str): Unique identifier for the first cultural item
        - item_1_title (str): Title of the second cultural item
        - item_1_artist (str): Artist of the second cultural item
        - item_1_year (int): Year of creation for the second cultural item
        - item_1_type (str): Type/category of the second cultural item
        - item_1_id (str): Unique identifier for the second cultural item
    """
    return {
        "collection_name": "Louvre Museum Collection",
        "items_count": 2,
        "item_0_title": "Mona Lisa",
        "item_0_artist": "Leonardo da Vinci",
        "item_0_year": 1503,
        "item_0_type": "Painting",
        "item_0_id": "LV-1001",
        "item_1_title": "The Wedding at Cana",
        "item_1_artist": "Paolo Veronese",
        "item_1_year": 1563,
        "item_1_type": "Painting",
        "item_1_id": "LV-1002"
    }

def cultural_heritage_server_get_collections_by_institution(institution_name: str) -> List[Dict[str, Any]]:
    """
    Get artworks and cultural items from a specific museum or cultural institution.
    
    Args:
        institution_name (str): Name of the cultural institution (e.g., "Louvre", "British Museum")
    
    Returns:
        List of cultural items from the specified institution, where each item contains:
        - collection_name (str): name of the cultural institution's collection
        - items_count (int): total number of items found in the collection
        - items (List[Dict]): list of cultural items, each with 'title', 'artist', 'year', 'type', and 'id' fields
    
    Raises:
        ValueError: If institution_name is empty or not provided
    """
    if not institution_name or not institution_name.strip():
        raise ValueError("institution_name is required and cannot be empty")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("cultural-heritage-server-get_collections_by_institution")
    
    # Construct the items list from indexed fields
    items = [
        {
            "title": api_data["item_0_title"],
            "artist": api_data["item_0_artist"],
            "year": api_data["item_0_year"],
            "type": api_data["item_0_type"],
            "id": api_data["item_0_id"]
        },
        {
            "title": api_data["item_1_title"],
            "artist": api_data["item_1_artist"],
            "year": api_data["item_1_year"],
            "type": api_data["item_1_type"],
            "id": api_data["item_1_id"]
        }
    ]
    
    # Construct final result structure
    result = [{
        "collection_name": api_data["collection_name"],
        "items_count": api_data["items_count"],
        "items": items
    }]
    
    return result