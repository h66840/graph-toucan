from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Met Museum object retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): Title of the museum object
        - artist (str): Name of the artist who created the object
        - artist_bio (str): Biographical information about the artist
        - department (str): Department within the Metropolitan Museum of Art
        - credit_line (str): Acquisition information
        - medium (str): Medium or materials used
        - dimensions (str): Physical dimensions of the object
        - primary_image_url (str): URL to the high-resolution primary image
        - tag_0 (str): First thematic or descriptive tag
        - tag_1 (str): Second thematic or descriptive tag
    """
    return {
        "title": "Portrait of a Young Woman",
        "artist": "Rembrandt van Rijn",
        "artist_bio": "Dutch, Leiden 1606–1669 Amsterdam",
        "department": "European Paintings",
        "credit_line": "Rogers Fund, 1907",
        "medium": "Oil on canvas",
        "dimensions": "37 1/2 × 31 1/2 in. (95.3 × 80 cm)",
        "primary_image_url": "https://images.metmuseum.org/CRDImages/ad/original/DP123456.jpg",
        "tag_0": "portrait",
        "tag_1": "woman"
    }

def met_museum_server_get_museum_object(objectId: int, returnImage: Optional[bool] = None) -> Dict[str, Any]:
    """
    Get a museum object by its ID from the Metropolitan Museum of Art Collection.
    
    Args:
        objectId (int): The ID of the museum object to retrieve (required)
        returnImage (Optional[bool]): Whether to return the image (if available) and add it to server resources
    
    Returns:
        Dict containing the following keys:
        - title (str): Title of the museum object
        - artist (str): Name of the artist who created the object
        - artist_bio (str): Biographical information about the artist
        - department (str): Department within the museum that houses the object
        - credit_line (str): Information about how the object was acquired
        - medium (str): Medium or materials used in creation
        - dimensions (str): Physical dimensions of the object
        - primary_image_url (str): URL to the high-resolution primary image
        - tags (List[str]): List of thematic or descriptive tags associated with the object
    
    Raises:
        ValueError: If objectId is not a positive integer
    """
    # Input validation
    if not isinstance(objectId, int) or objectId <= 0:
        raise ValueError("objectId must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("met-museum-server-get-museum-object")
    
    # Construct tags list from indexed fields
    tags = []
    if "tag_0" in api_data and api_data["tag_0"]:
        tags.append(api_data["tag_0"])
    if "tag_1" in api_data and api_data["tag_1"]:
        tags.append(api_data["tag_1"])
    
    # Build result dictionary matching output schema
    result = {
        "title": api_data["title"],
        "artist": api_data["artist"],
        "artist_bio": api_data["artist_bio"],
        "department": api_data["department"],
        "credit_line": api_data["credit_line"],
        "medium": api_data["medium"],
        "dimensions": api_data["dimensions"],
        "primary_image_url": api_data["primary_image_url"],
        "tags": tags
    }
    
    # If returnImage is False, remove the image URL
    if returnImage is False:
        result["primary_image_url"] = ""
    
    return result