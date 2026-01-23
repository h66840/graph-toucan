from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching seismic data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - seismic_event_0_magnitude (float): Magnitude of the first seismic event
        - seismic_event_0_latitude (float): Latitude of the first seismic event
        - seismic_event_0_longitude (float): Longitude of the first seismic event
        - seismic_event_0_depth (float): Depth in km of the first seismic event
        - seismic_event_0_timestamp (str): ISO 8601 timestamp of the first event
        - seismic_event_1_magnitude (float): Magnitude of the second seismic event
        - seismic_event_1_latitude (float): Latitude of the second seismic event
        - seismic_event_1_longitude (float): Longitude of the second seismic event
        - seismic_event_1_depth (float): Depth in km of the second seismic event
        - seismic_event_1_timestamp (str): ISO 8601 timestamp of the second event
        - total_count (int): Total number of seismic events returned
        - last_updated (str): ISO 8601 timestamp indicating when the data was last updated
        - metadata_source (str): Source of the seismic data
        - metadata_area (str): Area covered by the query ('continent', 'azores', 'madeira', or 'all')
        - metadata_generated_at (str): ISO 8601 timestamp when the response was generated
    """
    return {
        "seismic_event_0_magnitude": 3.2,
        "seismic_event_0_latitude": 38.7223,
        "seismic_event_0_longitude": -9.1393,
        "seismic_event_0_depth": 10.5,
        "seismic_event_0_timestamp": "2023-10-05T12:34:56Z",
        "seismic_event_1_magnitude": 2.8,
        "seismic_event_1_latitude": 37.1234,
        "seismic_event_1_longitude": -8.9876,
        "seismic_event_1_depth": 8.7,
        "seismic_event_1_timestamp": "2023-10-04T09:21:15Z",
        "total_count": 2,
        "last_updated": "2023-10-05T13:00:00Z",
        "metadata_source": "IPMA Seismic Monitoring Network",
        "metadata_area": "continent",
        "metadata_generated_at": datetime.now(timezone.utc).isoformat()
    }


def ipma_weather_data_server_get_seismic_data(area: Optional[str] = None) -> Dict[str, Any]:
    """
    Obter dados sísmicos recentes da API do IPMA.

    Args:
        area (Optional[str]): Área geográfica para filtrar os dados sísmicos.
                              Pode ser 'continent', 'azores', 'madeira', ou 'all'.
                              Se None, assume 'all'.

    Returns:
        Dict containing:
        - seismic_events (List[Dict]): Lista de eventos sísmicos com magnitude, localização, profundidade e timestamp.
        - total_count (int): Número total de eventos sísmicos retornados.
        - last_updated (str): Timestamp ISO 8601 indicando quando os dados foram atualizados.
        - metadata (Dict): Informações adicionais sobre a fonte, área e contexto da consulta.

    Raises:
        ValueError: Se o parâmetro 'area' não for um dos valores permitidos.
    """
    # Validate input
    valid_areas = {'continent', 'azores', 'madeira', 'all'}
    if area is not None and area not in valid_areas:
        raise ValueError(f"Invalid area: {area}. Must be one of {valid_areas} or None.")

    # Fetch simulated external data
    api_data = call_external_api("ipma-weather-data-server-get_seismic_data")

    # Construct seismic events list
    seismic_events: List[Dict[str, Any]] = [
        {
            "magnitude": api_data["seismic_event_0_magnitude"],
            "latitude": api_data["seismic_event_0_latitude"],
            "longitude": api_data["seismic_event_0_longitude"],
            "depth": api_data["seismic_event_0_depth"],
            "timestamp": api_data["seismic_event_0_timestamp"]
        },
        {
            "magnitude": api_data["seismic_event_1_magnitude"],
            "latitude": api_data["seismic_event_1_latitude"],
            "longitude": api_data["seismic_event_1_longitude"],
            "depth": api_data["seismic_event_1_depth"],
            "timestamp": api_data["seismic_event_1_timestamp"]
        }
    ]

    # Construct metadata
    metadata = {
        "source": api_data["metadata_source"],
        "area": area or api_data["metadata_area"],
        "generated_at": api_data["metadata_generated_at"]
    }

    # Return structured response matching output schema
    return {
        "seismic_events": seismic_events,
        "total_count": api_data["total_count"],
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }