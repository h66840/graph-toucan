from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dog breeds.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - breed_0__id (str): First breed's ID
        - breed_0_name (str): First breed's name
        - breed_0_normalized_name (str): First breed's normalized name
        - breed_1__id (str): Second breed's ID
        - breed_1_name (str): Second breed's name
        - breed_1_normalized_name (str): Second breed's normalized name
        - includeImage (bool): Whether image was included in request
    """
    return {
        "breed_0__id": "b001",
        "breed_0_name": "Golden Retriever",
        "breed_0_normalized_name": "golden_retriever",
        "breed_1__id": "b002",
        "breed_1_name": "German Shepherd",
        "breed_1_normalized_name": "german_shepherd",
        "includeImage": False
    }

def pote_get_all_breeds(includeImage: Optional[bool] = None) -> Dict[str, Any]:
    """
    Get a list of all supported dog breeds and their IDs.

    Args:
        includeImage (Optional[bool]): Whether to include cover images in the response.

    Returns:
        Dict containing a list of breed objects, each with '_id', 'name', and 'normalized_name' fields.
        Example:
        {
            "breeds": [
                {
                    "_id": "b001",
                    "name": "Golden Retriever",
                    "normalized_name": "golden_retriever"
                },
                {
                    "_id": "b002",
                    "name": "German Shepherd",
                    "normalized_name": "german_shepherd"
                }
            ]
        }
    """
    try:
        # Call external API to get flat data
        api_data = call_external_api("pote-get-all-breeds")
        
        # Construct breeds list from indexed fields
        breeds: List[Dict[str, str]] = [
            {
                "_id": api_data["breed_0__id"],
                "name": api_data["breed_0_name"],
                "normalized_name": api_data["breed_0_normalized_name"]
            },
            {
                "_id": api_data["breed_1__id"],
                "name": api_data["breed_1_name"],
                "normalized_name": api_data["breed_1_normalized_name"]
            }
        ]
        
        # Prepare result
        result = {
            "breeds": breeds
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve breeds: {e}")