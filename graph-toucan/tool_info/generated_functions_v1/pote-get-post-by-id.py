from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for getting a post by ID.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): Title of the post
        - breed (str): Breed of the dog
        - price (str): Price including currency
        - birthday (str): Birth date in MM/DD/YYYY
        - gender_distribution (str): Description of gender split
        - location (str): Location with postal code and city
        - type (str): Type of listing (e.g., Sale)
        - status (str): Current status of the post
        - vaccinated (str): Vaccination status
        - worm_treatment (str): Worm treatment status
        - microchipped (str): Microchipped status
        - pedigree (str): Pedigree documentation status
        - parents_mother (str): Mother dog name and optional link
        - parents_father (str): Father dog name
        - external_link (str): URL to original ad or registry
        - pictures_0 (str): First picture URL
        - pictures_1 (str): Second picture URL
    """
    return {
        "title": "Adorable Labrador Puppies for Sale",
        "breed": "Labrador Retriever",
        "price": "$1,200 (includes deposit)",
        "birthday": "03/15/2023",
        "gender_distribution": "2 males, 3 females",
        "location": "90210 Beverly Hills, CA",
        "type": "Sale",
        "status": "active",
        "vaccinated": "Yes, first round completed",
        "worm_treatment": "Treated twice",
        "microchipped": "No",
        "pedigree": "Full AKC pedigree available",
        "parents_mother": "Bella (ID: M123456)",
        "parents_father": "Max",
        "external_link": "https://example.com/puppies/labrador-123",
        "pictures_0": "https://example.com/images/puppy1.jpg",
        "pictures_1": "https://example.com/images/puppy2.jpg"
    }

def pote_get_post_by_id(postId: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific post by its MongoDB ID.
    
    Args:
        postId (str): The ID of the post to retrieve. Must be a valid MongoDB ObjectId string.
    
    Returns:
        Dict containing detailed post information with the following structure:
        - title (str): Title of the post
        - breed (str): Dog breed
        - price (str): Price with currency
        - birthday (str): Birth date in MM/DD/YYYY
        - gender_distribution (str): Gender split description
        - location (str): Location with postal code and city
        - type (str): Listing type
        - status (str): Post status
        - vaccinated (str): Vaccination info
        - worm_treatment (str): Worm treatment info
        - microchipped (str): Microchipping status
        - pedigree (str): Pedigree documentation status
        - parents (Dict): Contains 'Mother' and 'Father' keys with parent names
        - external_link (str): URL to original advertisement
        - pictures (List[str]): List of image URLs (2 items)
    
    Raises:
        ValueError: If postId is empty or invalid
    """
    if not postId or not isinstance(postId, str) or len(postId.strip()) == 0:
        raise ValueError("postId is required and must be a non-empty string")
    
    # Call external API to get flat data
    api_data = call_external_api("pote-get-post-by-id")
    
    # Construct nested structure matching output schema
    result = {
        "title": api_data["title"],
        "breed": api_data["breed"],
        "price": api_data["price"],
        "birthday": api_data["birthday"],
        "gender_distribution": api_data["gender_distribution"],
        "location": api_data["location"],
        "type": api_data["type"],
        "status": api_data["status"],
        "vaccinated": api_data["vaccinated"],
        "worm_treatment": api_data["worm_treatment"],
        "microchipped": api_data["microchipped"],
        "pedigree": api_data["pedigree"],
        "parents": {
            "Mother": api_data["parents_mother"],
            "Father": api_data["parents_father"]
        },
        "external_link": api_data["external_link"],
        "pictures": [
            api_data["pictures_0"],
            api_data["pictures_1"]
        ]
    }
    
    return result