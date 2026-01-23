from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Airbnb listing details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - listingUrl (str): Direct URL to the Airbnb listing with booking parameters
        - details_0_id (str): ID of the first detail section
        - details_0_title (str): Title of the first detail section
        - details_0_houseRulesSections (str): Formatted text of house rules for first section
        - details_0_lat (float): Latitude of the property for first section
        - details_0_lng (float): Longitude of the property for first section
        - details_0_subtitle (str): Subtitle for location in first section
        - details_0_highlights (str): Highlights for first section
        - details_0_htmlDescription_htmlText (str): HTML description text for first section
        - details_0_seeAllAmenitiesGroups (str): Amenities groups for first section
        - details_1_id (str): ID of the second detail section
        - details_1_title (str): Title of the second detail section
        - details_1_houseRulesSections (str): Formatted text of house rules for second section
        - details_1_lat (float): Latitude of the property for second section
        - details_1_lng (float): Longitude of the property for second section
        - details_1_subtitle (str): Subtitle for location in second section
        - details_1_highlights (str): Highlights for second section
        - details_1_htmlDescription_htmlText (str): HTML description text for second section
        - details_1_seeAllAmenitiesGroups (str): Amenities groups for second section
    """
    return {
        "listingUrl": "https://www.airbnb.com/rooms/12345678?adults=2&children=1&check_in=2023-12-01&check_out=2023-12-05",
        "details_0_id": "POLICIES_DEFAULT",
        "details_0_title": "Things to know",
        "details_0_houseRulesSections": "Check-in: 3 PM - 11 PM, Checkout: 11 AM, No smoking, Pets allowed with fee, Self check-in with smart lock",
        "details_0_lat": 37.7749,
        "details_0_lng": -122.4194,
        "details_0_subtitle": "San Francisco, California",
        "details_0_highlights": "Top 10% of homes, Self check-in, Extra spacious",
        "details_0_htmlDescription_htmlText": "<p>Beautiful downtown loft with skyline views. Guests have full access to the unit and building amenities including gym and rooftop deck.</p>",
        "details_0_seeAllAmenitiesGroups": "Bathroom: Shower, Toilet, Towels; Bedroom: Queen bed, Extra pillows; Kitchen: Refrigerator, Microwave, Coffee maker",
        
        "details_1_id": "AMENITIES_DEFAULT",
        "details_1_title": "What this place offers",
        "details_1_houseRulesSections": "Guest max: 4, Infants allowed, Quiet hours after 10 PM",
        "details_1_lat": 37.7749,
        "details_1_lng": -122.4194,
        "details_1_subtitle": "San Francisco, California",
        "details_1_highlights": "Free parking, Pool, Hot tub",
        "details_1_htmlDescription_htmlText": "<p>Modern apartment with full kitchen and private balcony. Ideal for couples or small families.</p>",
        "details_1_seeAllAmenitiesGroups": "Parking: Free on premises; Pool and Spa: Private pool, Hot tub; Entertainment: TV, High-speed WiFi"
    }

def airbnb_search_and_listing_server_airbnb_listing_details(
    id: str,
    adults: Optional[int] = None,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    children: Optional[int] = None,
    ignoreRobotsText: Optional[bool] = None,
    infants: Optional[int] = None,
    pets: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Airbnb listing. Provide direct links to the user.
    
    Args:
        id (str): The Airbnb listing ID (required)
        adults (int, optional): Number of adults
        checkin (str, optional): Check-in date in YYYY-MM-DD format
        checkout (str, optional): Check-out date in YYYY-MM-DD format
        children (int, optional): Number of children
        ignoreRobotsText (bool, optional): Whether to ignore robots.txt rules
        infants (int, optional): Number of infants
        pets (int, optional): Number of pets
        
    Returns:
        Dict containing:
        - listingUrl (str): Direct URL to the Airbnb listing with booking parameters
        - details (List[Dict]): List of detail sections with structured information about policies, 
          location, highlights, description, and amenities
        
    Raises:
        ValueError: If required id parameter is missing or invalid
        TypeError: If date parameters are not in valid YYYY-MM-DD format
    """
    # Input validation
    if not id or not isinstance(id, str) or not id.strip():
        raise ValueError("Required parameter 'id' must be a non-empty string")
    
    id = id.strip()
    
    # Validate date formats if provided
    if checkin:
        try:
            datetime.strptime(checkin, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Check-in date must be in YYYY-MM-DD format")
    
    if checkout:
        try:
            datetime.strptime(checkout, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Check-out date must be in YYYY-MM-DD format")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("airbnb-search-and-listing-server-airbnb_listing_details")
    
    # Construct details list from flattened API response
    details = []
    
    for i in range(2):  # We expect 2 items as per the API simulation
        detail = {
            "id": api_data.get(f"details_{i}_id"),
            "title": api_data.get(f"details_{i}_title"),
            "houseRulesSections": api_data.get(f"details_{i}_houseRulesSections"),
            "lat": api_data.get(f"details_{i}_lat"),
            "lng": api_data.get(f"details_{i}_lng"),
            "subtitle": api_data.get(f"details_{i}_subtitle"),
            "highlights": api_data.get(f"details_{i}_highlights"),
            "htmlDescription": {
                "htmlText": api_data.get(f"details_{i}_htmlDescription_htmlText")
            },
            "seeAllAmenitiesGroups": api_data.get(f"details_{i}_seeAllAmenitiesGroups")
        }
        # Remove None values
        detail = {k: v for k, v in detail.items() if v is not None}
        details.append(detail)
    
    # Construct final result
    result = {
        "listingUrl": api_data["listingUrl"],
        "details": details
    }
    
    return result