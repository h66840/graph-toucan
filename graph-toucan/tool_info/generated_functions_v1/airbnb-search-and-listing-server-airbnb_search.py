from typing import Dict, List, Any, Optional
import base64
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Airbnb search API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - search_url (str): Full Airbnb search URL with parameters
        - result_0_id (str): First listing ID
        - result_0_url (str): First listing URL
        - result_0_demand_id (str): First listing demandStayListing ID
        - result_0_demand_name (str): First listing name
        - result_0_lat (float): First listing latitude
        - result_0_lng (float): First listing longitude
        - result_0_badges (str): First listing badges as JSON string
        - result_0_structured_content (str): First listing structuredContent as JSON string
        - result_0_rating_label (str): First listing avgRatingA11yLabel
        - result_0_param_overrides (str): First listing listingParamOverrides as JSON string
        - result_0_display_price (str): First listing structuredDisplayPrice
        - result_1_id (str): Second listing ID
        - result_1_url (str): Second listing URL
        - result_1_demand_id (str): Second listing demandStayListing ID
        - result_1_demand_name (str): Second listing name
        - result_1_lat (float): Second listing latitude
        - result_1_lng (float): Second listing longitude
        - result_1_badges (str): Second listing badges as JSON string
        - result_1_structured_content (str): Second listing structuredContent as JSON string
        - result_1_rating_label (str): Second listing avgRatingA11yLabel
        - result_1_param_overrides (str): Second listing listingParamOverrides as JSON string
        - result_1_display_price (str): Second listing structuredDisplayPrice
        - pagination_cursors (str): JSON string of page cursors list
        - pagination_next_cursor (str): Base64-encoded next page cursor
        - error_message (str): Error message if any
        - error_url (str): URL that caused error
        - suggestion_message (str): Suggested action to resolve error
    """
    return {
        "search_url": "https://www.airbnb.com/s/homes?location=Paris%2C+France&checkin=2023-12-01&checkout=2023-12-05&adults=2&children=1&infants=1&pets=1&minPrice=100&maxPrice=500",
        "result_0_id": "1001",
        "result_0_url": "https://www.airbnb.com/rooms/1001",
        "result_0_demand_id": "d1001",
        "result_0_demand_name": "Charming Studio in Paris Center",
        "result_0_lat": 48.8566,
        "result_0_lng": 2.3522,
        "result_0_badges": '["Superhost", "New"]',
        "result_0_structured_content": '{"section1": "value1"}',
        "result_0_rating_label": "4.8 (240 reviews)",
        "result_0_param_overrides": '{"price": "120"}',
        "result_0_display_price": "$120 per night",
        "result_1_id": "1002",
        "result_1_url": "https://www.airbnb.com/rooms/1002",
        "result_1_demand_id": "d1002",
        "result_1_demand_name": "Luxury Apartment Near Eiffel Tower",
        "result_1_lat": 48.8588,
        "result_1_lng": 2.2944,
        "result_1_badges": '["Luxury", "Superhost"]',
        "result_1_structured_content": '{"section1": "value2"}',
        "result_1_rating_label": "4.9 (310 reviews)",
        "result_1_param_overrides": '{"price": "250"}',
        "result_1_display_price": "$250 per night",
        "pagination_cursors": '["cursor1", "cursor2", "cursor3"]',
        "pagination_next_cursor": base64.b64encode(b"next_page_cursor_data").decode('utf-8'),
        "error_message": "",
        "error_url": "",
        "suggestion_message": ""
    }

def airbnb_search_and_listing_server_airbnb_search(
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
        location (str): Location to search for (city, state, etc.) - required
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
        - searchUrl (str): Full Airbnb search URL with query parameters
        - searchResults (List[Dict]): List of listing objects with detailed info
        - paginationInfo (Dict): Pagination metadata including cursors
        - error (str): Error message if request failed
        - url (str): Raw URL attempted when error occurred
        - suggestion (str): Suggested action to resolve errors
    """
    # Validate required parameter
    if not location:
        return {
            "searchUrl": "",
            "searchResults": [],
            "paginationInfo": {"pageCursors": [], "nextPageCursor": ""},
            "error": "Location is required",
            "url": "",
            "suggestion": "Provide a valid location string"
        }
    
    # Validate dates if provided
    if checkin:
        try:
            datetime.strptime(checkin, "%Y-%m-%d")
        except ValueError:
            return {
                "searchUrl": "",
                "searchResults": [],
                "paginationInfo": {"pageCursors": [], "nextPageCursor": ""},
                "error": "Invalid checkin date format. Use YYYY-MM-DD",
                "url": "",
                "suggestion": "Use date format YYYY-MM-DD for checkin"
            }
    
    if checkout:
        try:
            datetime.strptime(checkout, "%Y-%m-%d")
        except ValueError:
            return {
                "searchUrl": "",
                "searchResults": [],
                "paginationInfo": {"pageCursors": [], "nextPageCursor": ""},
                "error": "Invalid checkout date format. Use YYYY-MM-DD",
                "url": "",
                "suggestion": "Use date format YYYY-MM-DD for checkout"
            }
    
    # Build search URL
    base_url = "https://www.airbnb.com/s/homes"
    params = {}
    
    # Use placeId if provided, otherwise use location
    if placeId:
        params["placeId"] = placeId
    else:
        params["location"] = location
    
    if checkin:
        params["checkin"] = checkin
    if checkout:
        params["checkout"] = checkout
    if adults is not None:
        params["adults"] = str(adults)
    if children is not None:
        params["children"] = str(children)
    if infants is not None:
        params["infants"] = str(infants)
    if pets is not None:
        params["pets"] = str(pets)
    if minPrice is not None:
        params["minPrice"] = str(minPrice)
    if maxPrice is not None:
        params["maxPrice"] = str(maxPrice)
    
    # Manually construct query string without using urllib.parse.urlencode
    query_parts = []
    for key, value in params.items():
        # Simple URL encoding by replacing spaces with %20 and handling special chars
        encoded_key = key.replace(' ', '%20').replace('&', '%26').replace('=', '%3D')
        encoded_value = str(value).replace(' ', '%20').replace('&', '%26').replace('=', '%3D')
        query_parts.append(f"{encoded_key}={encoded_value}")
    
    query_string = "&".join(query_parts)
    search_url = f"{base_url}?{query_string}"
    
    # Call external API (simulated)
    api_data = call_external_api("airbnb-search-and-listing-server-airbnb_search")
    
    # Construct search results from flattened API data
    search_results = []
    
    # Process first result if available
    if api_data.get("result_0_id"):
        result_0 = {
            "id": api_data["result_0_id"],
            "url": api_data["result_0_url"],
            "demandId": api_data["result_0_demand_id"],
            "name": api_data["result_0_demand_name"],
            "lat": api_data["result_0_lat"],
            "lng": api_data["result_0_lng"],
            "badges": api_data["result_0_badges"],
            "structuredContent": api_data["result_0_structured_content"],
            "ratingLabel": api_data["result_0_rating_label"],
            "paramOverrides": api_data["result_0_param_overrides"],
            "displayPrice": api_data["result_0_display_price"]
        }
        search_results.append(result_0)
    
    # Process second result if available
    if api_data.get("result_1_id"):
        result_1 = {
            "id": api_data["result_1_id"],
            "url": api_data["result_1_url"],
            "demandId": api_data["result_1_demand_id"],
            "name": api_data["result_1_demand_name"],
            "lat": api_data["result_1_lat"],
            "lng": api_data["result_1_lng"],
            "badges": api_data["result_1_badges"],
            "structuredContent": api_data["result_1_structured_content"],
            "ratingLabel": api_data["result_1_rating_label"],
            "paramOverrides": api_data["result_1_param_overrides"],
            "displayPrice": api_data["result_1_display_price"]
        }
        search_results.append(result_1)
    
    # Handle pagination
    page_cursors = api_data.get("pagination_cursors", "[]")
    next_cursor = api_data.get("pagination_next_cursor", "")
    
    # Return formatted response
    return {
        "searchUrl": search_url,
        "searchResults": search_results,
        "paginationInfo": {
            "pageCursors": page_cursors,
            "nextPageCursor": next_cursor
        },
        "error": api_data.get("error_message", ""),
        "url": api_data.get("error_url", ""),
        "suggestion": api_data.get("suggestion_message", "")
    }