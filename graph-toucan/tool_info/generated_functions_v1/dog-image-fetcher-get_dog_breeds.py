from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dog breeds.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the request (e.g., "success")
        - count (int): Total number of breeds returned
        - page (int): Current page number
        - breed_0_id (str): ID of first breed
        - breed_0_name (str): Name of first breed
        - breed_0_temperament (str): Temperament of first breed
        - breed_0_life_span (str): Life span of first breed
        - breed_0_alt_names (str): Alternate names of first breed
        - breed_0_wikipedia_url (str): Wikipedia URL of first breed
        - breed_0_origin (str): Origin of first breed
        - breed_0_weight_metric (str): Weight (metric) of first breed
        - breed_0_height_metric (str): Height (metric) of first breed
        - breed_0_bred_for (str): Bred for purpose of first breed
        - breed_0_breed_group (str): Breed group of first breed
        - breed_0_reference_image_id (str): Reference image ID of first breed
        - breed_1_id (str): ID of second breed
        - breed_1_name (str): Name of second breed
        - breed_1_temperament (str): Temperament of second breed
        - breed_1_life_span (str): Life span of second breed
        - breed_1_alt_names (str): Alternate names of second breed
        - breed_1_wikipedia_url (str): Wikipedia URL of second breed
        - breed_1_origin (str): Origin of second breed
        - breed_1_weight_metric (str): Weight (metric) of second breed
        - breed_1_height_metric (str): Height (metric) of second breed
        - breed_1_bred_for (str): Bred for purpose of second breed
        - breed_1_breed_group (str): Breed group of second breed
        - breed_1_reference_image_id (str): Reference image ID of second breed
    """
    return {
        "status": "success",
        "count": 2,
        "page": 1,
        "breed_0_id": "ab01",
        "breed_0_name": "Afghan Hound",
        "breed_0_temperament": "Dignified, Aloof, Independent, Happy, Clownish",
        "breed_0_life_span": "10 - 13 years",
        "breed_0_alt_names": "Sag-e-Tazi",
        "breed_0_wikipedia_url": "https://en.wikipedia.org/wiki/Afghan_Hound",
        "breed_0_origin": "Afghanistan",
        "breed_0_weight_metric": "23 - 27",
        "breed_0_height_metric": "61 - 74",
        "breed_0_bred_for": "Hunting, Tracking",
        "breed_0_breed_group": "Hound Group",
        "breed_0_reference_image_id": "abc123",
        "breed_1_id": "ae02",
        "breed_1_name": "Aegean",
        "breed_1_temperament": "Affectionate, Social, Intelligent, Playful",
        "breed_1_life_span": "9 - 13 years",
        "breed_1_alt_names": "",
        "breed_1_wikipedia_url": "https://en.wikipedia.org/wiki/Aegean_cat",
        "breed_1_origin": "Greece",
        "breed_1_weight_metric": "3 - 5",
        "breed_1_height_metric": "25 - 32",
        "breed_1_bred_for": "Companionship, Pest control",
        "breed_1_breed_group": "Domestic",
        "breed_1_reference_image_id": "def456"
    }

def dog_image_fetcher_get_dog_breeds(limit: Optional[int] = None, page: Optional[int] = None, search: Optional[str] = None) -> Dict[str, Any]:
    """
    Get list of dog breeds with detailed information.

    Args:
        limit (int, optional): Number of breeds to return (1-100). Defaults to 2.
        page (int, optional): Page number for pagination. Defaults to 1.
        search (str, optional): Search term to filter breeds by name. Ignored in simulation.

    Returns:
        Dict containing:
        - status (str): status of the request (e.g., "success")
        - count (int): total number of breeds returned in this response
        - page (int): current page number of the results
        - breeds (List[Dict]): list of breed objects with detailed fields including:
            * id (str)
            * name (str)
            * temperament (str)
            * life_span (str)
            * alt_names (str)
            * wikipedia_url (str)
            * origin (str)
            * weight_metric (str)
            * height_metric (str)
            * bred_for (str)
            * breed_group (str)
            * reference_image_id (str)
    
    Note:
        This is a simulated implementation. In a real scenario, this would call an external API.
        For demonstration, returns 2 hardcoded breeds with data mapped from flattened API response.
    """
    # Validate inputs
    if limit is not None:
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValueError("limit must be an integer between 1 and 100")
    
    if page is not None:
        if not isinstance(page, int) or page < 1:
            raise ValueError("page must be a positive integer")
    
    # Use defaults if not provided
    effective_limit = limit if limit is not None else 2
    effective_page = page if page is not None else 1

    # Call external API (simulated)
    api_data = call_external_api("dog-image-fetcher-get_dog_breeds")
    
    # Construct breeds list from flattened data
    breeds = []
    
    # Process up to 2 breeds (as per simulated API) and respect limit
    for i in range(min(2, effective_limit)):
        breed_data = {
            "id": api_data.get(f"breed_{i}_id"),
            "name": api_data.get(f"breed_{i}_name"),
            "temperament": api_data.get(f"breed_{i}_temperament"),
            "life_span": api_data.get(f"breed_{i}_life_span"),
            "alt_names": api_data.get(f"breed_{i}_alt_names"),
            "wikipedia_url": api_data.get(f"breed_{i}_wikipedia_url"),
            "origin": api_data.get(f"breed_{i}_origin"),
            "weight_metric": api_data.get(f"breed_{i}_weight_metric"),
            "height_metric": api_data.get(f"breed_{i}_height_metric"),
            "bred_for": api_data.get(f"breed_{i}_bred_for"),
            "breed_group": api_data.get(f"breed_{i}_breed_group"),
            "reference_image_id": api_data.get(f"breed_{i}_reference_image_id")
        }
        breeds.append(breed_data)
    
    # Construct final result
    result = {
        "status": api_data["status"],
        "count": len(breeds),
        "page": effective_page,
        "breeds": breeds
    }
    
    return result