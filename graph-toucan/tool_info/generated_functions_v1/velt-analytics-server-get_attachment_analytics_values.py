from typing import Dict, List, Any
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching attachment analytics data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - attachment_0_type (str): Type of the first attachment
        - attachment_0_total_size_bytes (int): Total size in bytes for the first attachment type
        - attachment_1_type (str): Type of the second attachment
        - attachment_1_total_size_bytes (int): Total size in bytes for the second attachment type
        - time_range_start_date (str): Start date of the analytics period in ISO format
        - time_range_end_date (str): End date of the analytics period in ISO format
        - time_range_range_type (str): Type of date range (e.g., 'last_7_days')
        - total_attachments_count (int): Total number of attachments analyzed
        - total_storage_used_bytes (int): Total storage used across all attachments in bytes
        - generated_at (str): Timestamp when the analytics were generated (ISO format)
        - metadata_resolution (str): Resolution of the analytics (e.g., 'daily')
        - metadata_status (str): Status of the analytics generation (e.g., 'complete')
    """
    return {
        "attachment_0_type": "pdf",
        "attachment_0_total_size_bytes": 10485760,
        "attachment_1_type": "jpg",
        "attachment_1_total_size_bytes": 20971520,
        "time_range_start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "time_range_end_date": datetime.now().strftime("%Y-%m-%d"),
        "time_range_range_type": "last_7_days",
        "total_attachments_count": 150,
        "total_storage_used_bytes": 31457280,
        "generated_at": datetime.now().isoformat(),
        "metadata_resolution": "daily",
        "metadata_status": "complete",
    }


def velt_analytics_server_get_attachment_analytics_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get attachment analytics from Velt showing total size by attachment type.

    Args:
        data (Dict[str, Any]): Input data object containing parameters for analytics.
            Expected keys may include filters like date ranges or attachment types.

    Returns:
        Dict[str, Any]: Analytics result containing:
            - attachment_types (List[Dict]): List of dicts with 'type' and 'total_size_bytes'
            - time_range (Dict): Contains 'start_date', 'end_date', and 'range_type'
            - total_attachments_count (int): Total number of attachments analyzed
            - total_storage_used_bytes (int): Total storage used in bytes
            - generated_at (str): ISO timestamp when result was generated
            - metadata (Dict): Additional context like 'resolution' and 'status'

    Raises:
        ValueError: If required data is missing or invalid
        TypeError: If input types are incorrect
    """
    if not isinstance(data, dict):
        raise TypeError("Input 'data' must be a dictionary")

    # Fetch simulated external API data
    api_data = call_external_api("velt-analytics-server-get_attachment_analytics_values")

    # Construct attachment types list from indexed fields
    attachment_types: List[Dict[str, Any]] = [
        {
            "type": api_data["attachment_0_type"],
            "total_size_bytes": api_data["attachment_0_total_size_bytes"]
        },
        {
            "type": api_data["attachment_1_type"],
            "total_size_bytes": api_data["attachment_1_total_size_bytes"]
        }
    ]

    # Construct time range object
    time_range = {
        "start_date": api_data["time_range_start_date"],
        "end_date": api_data["time_range_end_date"],
        "range_type": api_data["time_range_range_type"]
    }

    # Construct metadata object
    metadata = {
        "resolution": api_data["metadata_resolution"],
        "status": api_data["metadata_status"]
    }

    # Build final result
    result = {
        "attachment_types": attachment_types,
        "time_range": time_range,
        "total_attachments_count": api_data["total_attachments_count"],
        "total_storage_used_bytes": api_data["total_storage_used_bytes"],
        "generated_at": api_data["generated_at"],
        "metadata": metadata
    }

    return result