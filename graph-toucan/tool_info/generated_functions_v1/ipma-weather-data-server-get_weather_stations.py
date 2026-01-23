from typing import Dict, List, Any
from datetime import datetime, timezone
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather station data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - observation_timestamp (str): ISO 8601 timestamp of observations
        - station_0_name (str): Name of first weather station
        - station_0_temperature (float): Temperature at first station in Celsius
        - station_0_humidity (float): Humidity at first station in percent
        - station_0_pressure (float): Atmospheric pressure at first station in hPa
        - station_0_wind_speed (float): Wind speed at first station in m/s
        - station_0_precipitation (float): Precipitation at first station in mm (optional)
        - station_1_name (str): Name of second weather station
        - station_1_temperature (float): Temperature at second station in Celsius
        - station_1_humidity (float): Humidity at second station in percent
        - station_1_pressure (float): Atmospheric pressure at second station in hPa
        - station_1_wind_speed (float): Wind speed at second station in m/s
        - station_1_precipitation (float): Precipitation at second station in mm (optional)
    """
    # Generate current timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat()
    
    return {
        "observation_timestamp": timestamp,
        "station_0_name": "Lisbon Airport",
        "station_0_temperature": round(20.5 + random.uniform(-5, 5), 1),
        "station_0_humidity": round(65 + random.uniform(-20, 20), 1),
        "station_0_pressure": round(1013.25 + random.uniform(-20, 20), 1),
        "station_0_wind_speed": round(3.5 + random.uniform(0, 10), 1),
        "station_0_precipitation": round(random.uniform(0, 5), 1),
        "station_1_name": "Porto City Center",
        "station_1_temperature": round(18.0 + random.uniform(-5, 5), 1),
        "station_1_humidity": round(70 + random.uniform(-20, 20), 1),
        "station_1_pressure": round(1013.25 + random.uniform(-20, 20), 1),
        "station_1_wind_speed": round(4.0 + random.uniform(0, 12), 1),
        "station_1_precipitation": round(random.uniform(0, 8), 1)
    }

def ipma_weather_data_server_get_weather_stations() -> Dict[str, Any]:
    """
    Obter dados de observação das estações meteorológicas.
    
    Returns:
        Dict containing:
        - observation_timestamp (str): timestamp of the weather observations in ISO 8601 format
        - stations (List[Dict]): list of weather stations, each containing 'name', 'temperature', 
          'humidity', 'pressure', 'wind_speed', 'precipitation' (if available), and other 
          observed meteorological values
    
    Example:
        {
            "observation_timestamp": "2023-11-15T10:30:00+00:00",
            "stations": [
                {
                    "name": "Lisbon Airport",
                    "temperature": 22.5,
                    "humidity": 60.0,
                    "pressure": 1012.3,
                    "wind_speed": 5.2,
                    "precipitation": 0.0
                },
                {
                    "name": "Porto City Center",
                    "temperature": 19.8,
                    "humidity": 75.0,
                    "pressure": 1015.6,
                    "wind_speed": 3.8,
                    "precipitation": 2.1
                }
            ]
        }
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("ipma-weather-data-server-get_weather_stations")
        
        # Construct stations list from indexed fields
        stations: List[Dict[str, Any]] = [
            {
                "name": api_data["station_0_name"],
                "temperature": api_data["station_0_temperature"],
                "humidity": api_data["station_0_humidity"],
                "pressure": api_data["station_0_pressure"],
                "wind_speed": api_data["station_0_wind_speed"],
                "precipitation": api_data["station_0_precipitation"]
            },
            {
                "name": api_data["station_1_name"],
                "temperature": api_data["station_1_temperature"],
                "humidity": api_data["station_1_humidity"],
                "pressure": api_data["station_1_pressure"],
                "wind_speed": api_data["station_1_wind_speed"],
                "precipitation": api_data["station_1_precipitation"]
            }
        ]
        
        # Construct final result matching output schema
        result = {
            "observation_timestamp": api_data["observation_timestamp"],
            "stations": stations
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process weather station data: {str(e)}")