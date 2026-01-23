from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Airbnb search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - searchUrl (str): URL to the Airbnb search results page for the given location and filters
        - error (str): Error message if the request was blocked or failed
        - url (str): Fallback or alternative URL when an error occurs
    """
    return {
        "searchUrl": "https://www.airbnb.com/s/Paris/homes?check_in=2023-10-01&check_out=2023-10-08&adults=2&children=1&infants=0&pets=1&price_min=100&price_max=500",
        "error": "",
        "url": "https://www.airbnb.com/s/Paris/homes"
    }

def airbnb_search_and_listing_details_server_airbnb_search(
    location: str,
    adults: Optional[int] = None,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    children: Optional[int] = None,
    cursor: Optional[str] = None,
    ignoreRobotsText: Optional[bool] = None,
    infants: Optional[int] = None,
    maxPrice: Optional[float] = None,
    minPrice: Optional[float] = None,
    pets: Optional[int] = None,
    placeId: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for Airbnb listings with various filters and pagination. Provide direct links to the user.

    Args:
        location (str): Location to search for (city, state, etc.)
        adults (int, optional): Number of adults
        checkin (str, optional): Check-in date (YYYY-MM-DD)
        checkout (str, optional): Check-out date (YYYY-MM-DD)
        children (int, optional): Number of children
        cursor (str, optional): Base64-encoded string used for Pagination
        ignoreRobotsText (bool, optional): Ignore robots.txt rules for this request
        infants (int, optional): Number of infants
        maxPrice (float, optional): Maximum price for the stay
        minPrice (float, optional): Minimum price for the stay
        pets (int, optional): Number of pets
        placeId (str, optional): Google Maps Place ID (overrides the location parameter)

    Returns:
        Dict containing:
        - searchUrl (str): URL to the Airbnb search results page for the given location and filters
        - error (str): Error message if the request was blocked or failed
        - url (str): Fallback or alternative URL provided when an error occurs
    """
    # Input validation
    if not location:
        return {
            "searchUrl": "",
            "error": "Location is required",
            "url": ""
        }

    # Call external API simulation
    api_data = call_external_api("airbnb-search-and-listing-details-server-airbnb_search")
    
    # Construct result following output schema
    result = {
        "searchUrl": api_data["searchUrl"],
        "error": api_data["error"],
        "url": api_data["url"]
    }
    
    # Apply business logic to customize the URL based on inputs if needed
    base_url = "https://www.airbnb.com/s/"
    location_part = placeId if placeId else location.replace(" ", "-")
    params = []
    
    if checkin:
        params.append(f"check_in={checkin}")
    if checkout:
        params.append(f"check_out={checkout}")
    if adults:
        params.append(f"adults={adults}")
    if children:
        params.append(f"children={children}")
    if infants:
        params.append(f"infants={infants}")
    if pets:
        params.append(f"pets={pets}")
    if minPrice:
        params.append(f"price_min={int(minPrice)}")
    if maxPrice:
        params.append(f"price_max={int(maxPrice)}")
    
    query_string = "&".join(params)
    constructed_url = f"{base_url}{location_part}/homes?{query_string}" if params else f"{base_url}{location_part}/homes"
    
    # Update result with constructed URL
    if not result["error"]:
        result["searchUrl"] = constructed_url
        result["url"] = constructed_url
    
    return result