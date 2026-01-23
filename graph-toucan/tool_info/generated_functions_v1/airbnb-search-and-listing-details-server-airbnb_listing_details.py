from typing import Dict, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Airbnb API for listing details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - listingUrl (str): Direct URL to the Airbnb listing with booking parameters
        - details_name (str): Name/title of the listing
        - details_description (str): Description of the property
        - details_price_per_night (float): Price per night in local currency
        - details_currency (str): Currency code (e.g., USD, EUR)
        - details_rating (float): Average guest rating
        - details_review_count (int): Total number of reviews
        - details_host_name (str): Host's full name
        - details_host_is_superhost (bool): Whether host is a superhost
        - details_location_address (str): Full address of the listing
        - details_location_lat (float): Latitude of the listing
        - details_location_lng (float): Longitude of the listing
        - details_amenity_0 (str): First amenity (e.g., WiFi)
        - details_amenity_1 (str): Second amenity (e.g., Kitchen)
        - details_availability_min_nights (int): Minimum stay required
        - details_availability_max_nights (int): Maximum stay allowed
        - details_guests_included (int): Number of guests included in base price
    """
    return {
        "listingUrl": "https://www.airbnb.com/rooms/12345678?adults=2&children=1&check_in=2023-12-01&check_out=2023-12-05",
        "details_name": "Cozy Downtown Apartment with City View",
        "details_description": "A modern and cozy apartment located in the heart of the city. Perfect for couples or small families.",
        "details_price_per_night": 149.0,
        "details_currency": "USD",
        "details_rating": 4.85,
        "details_review_count": 234,
        "details_host_name": "Julia Smith",
        "details_host_is_superhost": True,
        "details_location_address": "123 Main St, Downtown, New York, NY, USA",
        "details_location_lat": 40.7589,
        "details_location_lng": -73.9851,
        "details_amenity_0": "WiFi",
        "details_amenity_1": "Kitchen",
        "details_availability_min_nights": 1,
        "details_availability_max_nights": 28,
        "details_guests_included": 2
    }

def airbnb_search_and_listing_details_server_airbnb_listing_details(
    id: str,
    adults: Optional[int] = None,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    children: Optional[int] = None,
    infants: Optional[int] = None,
    pets: Optional[int] = None,
    ignoreRobotsText: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Airbnb listing. Provide direct links to the user.
    
    Args:
        id (str): The Airbnb listing ID (required)
        adults (int, optional): Number of adults
        checkin (str, optional): Check-in date in YYYY-MM-DD format
        checkout (str, optional): Check-out date in YYYY-MM-DD format
        children (int, optional): Number of children
        infants (int, optional): Number of infants
        pets (int, optional): Number of pets
        ignoreRobotsText (bool, optional): Ignore robots.txt rules for this request
    
    Returns:
        Dict containing:
        - listingUrl (str): Direct URL to the Airbnb listing with booking parameters included
        - details (Dict): Nested dictionary with comprehensive listing information including:
            - name, description, pricing, currency
            - rating and review count
            - host information (name, superhost status)
            - location (address, latitude, longitude)
            - amenities (list of strings)
            - availability (min/max nights)
            - guests included in base price
    
    Raises:
        ValueError: If required id parameter is missing or empty
        ValueError: If checkin/checkout dates are provided but invalid format
    """
    # Input validation
    if not id:
        raise ValueError("Required parameter 'id' is missing or empty")
    
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
    
    # Call external API (simulated)
    api_data = call_external_api("airbnb-search-and-listing-details-server-airbnb_listing_details")
    
    # Construct nested structure matching output schema
    result = {
        "listingUrl": api_data["listingUrl"],
        "details": {
            "name": api_data["details_name"],
            "description": api_data["details_description"],
            "pricing": {
                "price_per_night": api_data["details_price_per_night"],
                "currency": api_data["details_currency"]
            },
            "reviews": {
                "rating": api_data["details_rating"],
                "review_count": api_data["details_review_count"]
            },
            "host": {
                "name": api_data["details_host_name"],
                "is_superhost": api_data["details_host_is_superhost"]
            },
            "location": {
                "address": api_data["details_location_address"],
                "lat": api_data["details_location_lat"],
                "lng": api_data["details_location_lng"]
            },
            "amenities": [
                api_data["details_amenity_0"],
                api_data["details_amenity_1"]
            ],
            "availability": {
                "min_nights": api_data["details_availability_min_nights"],
                "max_nights": api_data["details_availability_max_nights"]
            },
            "guests_included": api_data["details_guests_included"]
        }
    }
    
    return result