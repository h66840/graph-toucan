from typing import Dict,Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location_0_name (str): First location name
        - location_0_region_id (int): First location region ID
        - location_0_latitude (float): First location latitude
        - location_0_longitude (float): First location longitude
        - location_1_name (str): Second location name
        - location_1_region_id (int): Second location region ID
        - location_1_latitude (float): Second location latitude
        - location_1_longitude (float): Second location longitude
        - region_0_region_id (int): First region ID
        - region_0_name (str): First region name
        - region_0_location_0_name (str): First region's first location name
        - region_0_location_0_latitude (float): First region's first location latitude
        - region_0_location_0_longitude (float): First region's first location longitude
        - region_0_location_1_name (str): First region's second location name
        - region_0_location_1_latitude (float): First region's second location latitude
        - region_0_location_1_longitude (float): First region's second location longitude
        - region_1_region_id (int): Second region ID
        - region_1_name (str): Second region name
        - region_1_location_0_name (str): Second region's first location name
        - region_1_location_0_latitude (float): Second region's first location latitude
        - region_1_location_0_longitude (float): Second region's first location longitude
        - region_1_location_1_name (str): Second region's second location name
        - region_1_location_1_latitude (float): Second region's second location latitude
        - region_1_location_1_longitude (float): Second region's second location longitude
    """
    return {
        "location_0_name": "Lisboa",
        "location_0_region_id": 1,
        "location_0_latitude": 38.7256,
        "location_0_longitude": -9.1394,
        "location_1_name": "Porto",
        "location_1_region_id": 2,
        "location_1_latitude": 41.1579,
        "location_1_longitude": -8.6291,
        "region_0_region_id": 1,
        "region_0_name": "Lisboa",
        "region_0_location_0_name": "Lisboa",
        "region_0_location_0_latitude": 38.7256,
        "region_0_location_0_longitude": -9.1394,
        "region_0_location_1_name": "Amadora",
        "region_0_location_1_latitude": 38.75,
        "region_0_location_1_longitude": -9.2,
        "region_1_region_id": 2,
        "region_1_name": "Norte",
        "region_1_location_0_name": "Porto",
        "region_1_location_0_latitude": 41.1579,
        "region_1_location_0_longitude": -8.6291,
        "region_1_location_1_name": "Braga",
        "region_1_location_1_latitude": 41.5503,
        "region_1_location_1_longitude": -8.42,
    }


def ipma_weather_data_server_get_locations() -> Dict[str, Any]:
    """
    Listar todas as cidades/locais disponíveis para previsão.

    Returns:
        Dict containing:
            - locations (List[Dict]): list of locations, each with 'name', 'region_id', 'latitude', 'longitude'
            - regions (List[Dict]): list of regions, each with 'region_id', 'name', and 'locations' (list of location dicts)
    
    Raises:
        Exception: If there is any error in fetching or processing the data
    """
    try:
        api_data = call_external_api("ipma-weather-data-server-get_locations")

        # Construct locations list
        locations = [
            {
                "name": api_data["location_0_name"],
                "region_id": api_data["location_0_region_id"],
                "latitude": api_data["location_0_latitude"],
                "longitude": api_data["location_0_longitude"],
            },
            {
                "name": api_data["location_1_name"],
                "region_id": api_data["location_1_region_id"],
                "latitude": api_data["location_1_latitude"],
                "longitude": api_data["location_1_longitude"],
            },
        ]

        # Construct regions list
        regions = [
            {
                "region_id": api_data["region_0_region_id"],
                "name": api_data["region_0_name"],
                "locations": [
                    {
                        "name": api_data["region_0_location_0_name"],
                        "latitude": api_data["region_0_location_0_latitude"],
                        "longitude": api_data["region_0_location_0_longitude"],
                    },
                    {
                        "name": api_data["region_0_location_1_name"],
                        "latitude": api_data["region_0_location_1_latitude"],
                        "longitude": api_data["region_0_location_1_longitude"],
                    },
                ],
            },
            {
                "region_id": api_data["region_1_region_id"],
                "name": api_data["region_1_name"],
                "locations": [
                    {
                        "name": api_data["region_1_location_0_name"],
                        "latitude": api_data["region_1_location_0_latitude"],
                        "longitude": api_data["region_1_location_0_longitude"],
                    },
                    {
                        "name": api_data["region_1_location_1_name"],
                        "latitude": api_data["region_1_location_1_latitude"],
                        "longitude": api_data["region_1_location_1_longitude"],
                    },
                ],
            },
        ]

        return {"locations": locations, "regions": regions}

    except KeyError as e:
        raise Exception(f"Missing expected data field: {e}")
    except Exception as e:
        raise Exception(f"Error processing weather locations data: {e}")