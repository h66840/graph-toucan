from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for address validation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - is_valid (bool): Whether the address is valid
        - error (str): Error message if validation failed, empty if successful
        - input_address_street_address (str): Parsed street address
        - input_address_city (str): Parsed city
        - input_address_state (str): Parsed state
        - input_address_postal_code (str): Parsed postal code
        - input_address_country (str): Parsed country
        - coordinates_latitude (float): Latitude of the validated address
        - coordinates_longitude (float): Longitude of the validated address
    """
    return {
        "is_valid": True,
        "error": "",
        "input_address_street_address": "1600 Amphitheatre Parkway",
        "input_address_city": "Mountain View",
        "input_address_state": "CA",
        "input_address_postal_code": "94043",
        "input_address_country": "US",
        "coordinates_latitude": 37.4224764,
        "coordinates_longitude": -122.0842499
    }

def mcplatest_server_validate_address_tool(address: str) -> Dict[str, Any]:
    """
    Validate an address and get its coordinates.
    
    Args:
        address (str): Address string in format "Street, City, State, PostalCode, Country"
        
    Returns:
        dict: Validation results containing:
            - is_valid: Whether the address is valid
            - coordinates: Latitude and longitude if valid
            - input_address: Parsed address components
            - error: Error message if the validation request failed
    """
    if not address or not isinstance(address, str):
        return {
            "is_valid": False,
            "error": "Address must be a non-empty string",
            "input_address": {},
            "coordinates": {}
        }

    try:
        # Call external API to simulate address validation
        api_data = call_external_api("mcplatest_server_validate_address_tool")
        
        # Construct nested output structure
        result = {
            "is_valid": api_data["is_valid"],
            "error": api_data["error"],
            "input_address": {
                "street_address": api_data["input_address_street_address"],
                "city": api_data["input_address_city"],
                "state": api_data["input_address_state"],
                "postal_code": api_data["input_address_postal_code"],
                "country": api_data["input_address_country"]
            },
            "coordinates": {
                "latitude": api_data["coordinates_latitude"],
                "longitude": api_data["coordinates_longitude"]
            } if api_data["is_valid"] else {}
        }
        
        return result
        
    except Exception as e:
        return {
            "is_valid": False,
            "error": f"Address validation failed: {str(e)}",
            "input_address": {},
            "coordinates": {}
        }