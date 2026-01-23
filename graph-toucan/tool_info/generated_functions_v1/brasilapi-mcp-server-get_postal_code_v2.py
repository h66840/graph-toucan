from typing import Dict, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for postal code information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - cep (str): 8-digit postal code without hyphen
        - state (str): Two-letter state abbreviation
        - city (str): Full name of the city
        - neighborhood (str): Name of the neighborhood or district
        - street (str): Full name of the street or public square
        - service (str): Name of the data source service used
        - location_type (str): Type of location, always "Point"
        - location_coordinates_latitude (str): Latitude as string
        - location_coordinates_longitude (str): Longitude as string
    """
    return {
        "cep": "01310930",
        "state": "SP",
        "city": "São Paulo",
        "neighborhood": "Bela Vista",
        "street": "Avenida Paulista",
        "service": "open-cep",
        "location_type": "Point",
        "location_coordinates_latitude": "-23.5723",
        "location_coordinates_longitude": "-46.6555",
    }


def brasilapi_mcp_server_get_postal_code_v2(cep: str) -> Dict[str, Any]:
    """
    Version 2 of get a location data given a CEP (postal code).

    Args:
        cep (str): The CEP to query. Must be a valid 8-digit string (with or without hyphen).

    Returns:
        Dict[str, Any]: A dictionary containing the postal code information with the following keys:
            - cep (str): 8-digit postal code without hyphen
            - state (str): Two-letter state abbreviation
            - city (str): Full name of the city
            - neighborhood (str): Name of the neighborhood or district
            - street (str): Full name of the street or public square
            - service (str): Name of the data source service used
            - location (Dict): Contains 'type' and 'coordinates' fields; 'type' is always "Point";
                              'coordinates' is a dict with optional 'latitude' and 'longitude' as strings

    Raises:
        ValueError: If the provided CEP is not a valid string or empty.
    """
    if not cep or not isinstance(cep, str):
        raise ValueError("CEP must be a non-empty string.")

    # Normalize CEP by removing hyphens and spaces
    normalized_cep = cep.replace("-", "").strip()

    if len(normalized_cep) != 8 or not normalized_cep.isdigit():
        raise ValueError("CEP must contain exactly 8 digits.")

    # Fetch simulated external data
    api_data = call_external_api("brasilapi-mcp-server-get_postal_code_v2")

    # Construct nested structure matching output schema
    result = {
        "cep": api_data["cep"],
        "state": api_data["state"],
        "city": api_data["city"],
        "neighborhood": api_data["neighborhood"],
        "street": api_data["street"],
        "service": api_data["service"],
        "location": {
            "type": api_data["location_type"],
            "coordinates": {
                "latitude": api_data["location_coordinates_latitude"],
                "longitude": api_data["location_coordinates_longitude"],
            },
        },
    }

    return result