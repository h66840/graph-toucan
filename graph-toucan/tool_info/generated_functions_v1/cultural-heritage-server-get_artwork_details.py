from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external cultural heritage API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): title of the artwork
        - artist (str): name of the artist who created the artwork
        - year_created (str): year or date range when the artwork was created
        - art_type (str): type of artwork (e.g., Painting, Sculpture)
        - medium (str): medium used in the creation (e.g., Oil on poplar panel)
        - dimensions (str): physical dimensions of the artwork (e.g., 77 cm × 53 cm)
        - institution (str): institution where the artwork is currently housed
        - country (str): country where the artwork is located
        - description (str): descriptive summary of the artwork and its significance
        - image_url (str): URL to an image of the artwork
        - artwork_id (str): unique identifier for the artwork within the system
        - error_message (str): message indicating the requested artwork was not found, present only if lookup failed
    """
    return {
        "title": "Mona Lisa",
        "artist": "Leonardo da Vinci",
        "year_created": "1503–1506, 1517",
        "art_type": "Painting",
        "medium": "Oil on poplar panel",
        "dimensions": "77 cm × 53 cm",
        "institution": "Musée du Louvre",
        "country": "France",
        "description": "The Mona Lisa is a half-length portrait painting by Italian artist Leonardo da Vinci. "
                      "Considered an archetypal masterpiece of the Italian Renaissance, it has been described as "
                      "the best known, the most visited, the most written about, the most sung about, "
                      "the most parodied work of art in the world.",
        "image_url": "https://example.com/images/mona-lisa.jpg",
        "artwork_id": "INV.779",
        "error_message": ""
    }

def cultural_heritage_server_get_artwork_details(artwork_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific artwork or cultural item.
    
    Args:
        artwork_id (str): Unique identifier of the artwork
        
    Returns:
        Dict containing detailed information about the artwork including:
        - title (str): title of the artwork
        - artist (str): name of the artist who created the artwork
        - year_created (str): year or date range when the artwork was created
        - art_type (str): type of artwork (e.g., Painting, Sculpture)
        - medium (str): medium used in the creation (e.g., Oil on poplar panel)
        - dimensions (str): physical dimensions of the artwork (e.g., 77 cm × 53 cm)
        - institution (str): institution where the artwork is currently housed
        - country (str): country where the artwork is located
        - description (str): descriptive summary of the artwork and its significance
        - image_url (str): URL to an image of the artwork
        - artwork_id (str): unique identifier for the artwork within the system
        - error_message (str, optional): message indicating the requested artwork was not found
        
    Note:
        If the artwork is not found, the response will contain an error_message field
        and other fields may be empty or contain placeholder values.
    """
    if not artwork_id or not artwork_id.strip():
        return {
            "title": "",
            "artist": "",
            "year_created": "",
            "art_type": "",
            "medium": "",
            "dimensions": "",
            "institution": "",
            "country": "",
            "description": "",
            "image_url": "",
            "artwork_id": "",
            "error_message": "Artwork ID is required"
        }
    
    # Call external API to get data (returns flat structure)
    api_data = call_external_api("cultural-heritage-server-get_artwork_details")
    
    # Construct the nested response structure from flat API data
    result = {
        "title": api_data.get("title", ""),
        "artist": api_data.get("artist", ""),
        "year_created": api_data.get("year_created", ""),
        "art_type": api_data.get("art_type", ""),
        "medium": api_data.get("medium", ""),
        "dimensions": api_data.get("dimensions", ""),
        "institution": api_data.get("institution", ""),
        "country": api_data.get("country", ""),
        "description": api_data.get("description", ""),
        "image_url": api_data.get("image_url", ""),
        "artwork_id": api_data.get("artwork_id", ""),
    }
    
    # Add error message if present
    error_message = api_data.get("error_message", "")
    if error_message:
        result["error_message"] = error_message
    
    return result