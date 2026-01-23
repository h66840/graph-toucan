from typing import Dict, List, Any
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for TabNews analytics.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - daily_0_date (str): First day in YYYY-MM-DD format
        - daily_0_comment_count (int): Comment count for first day
        - daily_1_date (str): Second day in YYYY-MM-DD format
        - daily_1_comment_count (int): Comment count for second day
        - total_comments (int): Total number of comments across all days
        - time_range_start_date (str): Start date of the period in YYYY-MM-DD
        - time_range_end_date (str): End date of the period in YYYY-MM-DD
        - metadata_generated_at (str): ISO timestamp when data was generated
        - metadata_source (str): Source of the data
        - metadata_timezone (str): Timezone used for the data
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    return {
        "daily_0_date": start_date.strftime("%Y-%m-%d"),
        "daily_0_comment_count": 45,
        "daily_1_date": end_date.strftime("%Y-%m-%d"),
        "daily_1_comment_count": 67,
        "total_comments": 112,
        "time_range_start_date": start_date.strftime("%Y-%m-%d"),
        "time_range_end_date": end_date.strftime("%Y-%m-%d"),
        "metadata_generated_at": datetime.now().isoformat(),
        "metadata_source": "TabNews API",
        "metadata_timezone": "UTC"
    }

def tabnews_integration_get_analytics_child_content_published() -> Dict[str, Any]:
    """
    Fetches daily comment statistics from TabNews, including number of comments per day,
    total comments, time range, and metadata.

    Returns:
        Dict containing:
        - daily_comment_counts (List[Dict]): List of dicts with 'date' and 'comment_count'
        - total_comments (int): Total number of comments across all days
        - time_range (Dict): Contains 'start_date' and 'end_date' as strings
        - metadata (Dict): Additional context including 'generated_at', 'source', and 'timezone'
    
    Example:
        {
            "daily_comment_counts": [
                {"date": "2023-05-01", "comment_count": 45},
                {"date": "2023-05-02", "comment_count": 67}
            ],
            "total_comments": 112,
            "time_range": {
                "start_date": "2023-05-01",
                "end_date": "2023-05-02"
            },
            "metadata": {
                "generated_at": "2023-05-02T10:30:00",
                "source": "TabNews API",
                "timezone": "UTC"
            }
        }
    """
    try:
        # Call external API to get flattened data
        api_data = call_external_api("tabnews-integration-get analytics child content published")
        
        # Construct daily_comment_counts list from indexed fields
        daily_comment_counts = [
            {
                "date": api_data["daily_0_date"],
                "comment_count": api_data["daily_0_comment_count"]
            },
            {
                "date": api_data["daily_1_date"],
                "comment_count": api_data["daily_1_comment_count"]
            }
        ]
        
        # Construct time_range object
        time_range = {
            "start_date": api_data["time_range_start_date"],
            "end_date": api_data["time_range_end_date"]
        }
        
        # Construct metadata object
        metadata = {
            "generated_at": api_data["metadata_generated_at"],
            "source": api_data["metadata_source"],
            "timezone": api_data["metadata_timezone"]
        }
        
        # Build final result matching output schema
        result = {
            "daily_comment_counts": daily_comment_counts,
            "total_comments": api_data["total_comments"],
            "time_range": time_range,
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to process TabNews analytics data: {str(e)}")