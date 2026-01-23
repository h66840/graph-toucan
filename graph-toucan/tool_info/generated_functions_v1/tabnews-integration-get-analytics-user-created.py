from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for TabNews user creation analytics.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - daily_user_count_0_date (str): Date of first daily count entry
        - daily_user_count_0_count (int): User count for first date
        - daily_user_count_1_date (str): Date of second daily count entry
        - daily_user_count_1_count (int): User count for second date
        - total_users_created (int): Total number of users created across all days
        - time_range_start_date (str): Start date of the time range
        - time_range_end_date (str): End date of the time range
        - metadata_timestamp (str): Generation timestamp of the data
        - metadata_source (str): Source of the data
        - metadata_resolution (str): Data resolution (e.g., 'daily')
    """
    return {
        "daily_user_count_0_date": "2023-04-01",
        "daily_user_count_0_count": 150,
        "daily_user_count_1_date": "2023-04-02",
        "daily_user_count_1_count": 175,
        "total_users_created": 325,
        "time_range_start_date": "2023-04-01",
        "time_range_end_date": "2023-04-02",
        "metadata_timestamp": "2023-04-03T10:00:00Z",
        "metadata_source": "tabnews-analytics-service",
        "metadata_resolution": "daily"
    }

def tabnews_integration_get_analytics_user_created() -> Dict[str, Any]:
    """
    Fetches and returns analytics on user creation per day from TabNews.
    
    This function retrieves user creation statistics including daily counts,
    total users created, time range covered, and metadata about the data.
    
    Returns:
        Dict containing:
        - daily_user_counts (List[Dict]): List of daily user creation statistics,
          each with 'date' and 'count'
        - total_users_created (int): Total number of users created across all days
        - time_range (Dict): Object containing 'start_date' and 'end_date' strings
        - metadata (Dict): Additional info like timestamp, source, resolution
    """
    try:
        api_data = call_external_api("tabnews-integration-get analytics user created")
        
        # Construct daily user counts list
        daily_user_counts = [
            {
                "date": api_data["daily_user_count_0_date"],
                "count": api_data["daily_user_count_0_count"]
            },
            {
                "date": api_data["daily_user_count_1_date"],
                "count": api_data["daily_user_count_1_count"]
            }
        ]
        
        # Construct time range object
        time_range = {
            "start_date": api_data["time_range_start_date"],
            "end_date": api_data["time_range_end_date"]
        }
        
        # Construct metadata object
        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "source": api_data["metadata_source"],
            "resolution": api_data["metadata_resolution"]
        }
        
        # Build final result
        result = {
            "daily_user_counts": daily_user_counts,
            "total_users_created": api_data["total_users_created"],
            "time_range": time_range,
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process user creation analytics: {str(e)}")