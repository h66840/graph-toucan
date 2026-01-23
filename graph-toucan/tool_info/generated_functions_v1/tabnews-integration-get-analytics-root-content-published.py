from typing import Dict, List, Any
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching analytics data from TabNews API for published root content.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - daily_post_counts_0_date (str): Date of first day in YYYY-MM-DD format
        - daily_post_counts_0_count (int): Number of posts on first day
        - daily_post_counts_1_date (str): Date of second day in YYYY-MM-DD format
        - daily_post_counts_1_count (int): Number of posts on second day
        - total_posts (int): Total number of posts across all days
        - time_range_start_date (str): Start date of data range in YYYY-MM-DD format
        - time_range_end_date (str): End date of data range in YYYY-MM-DD format
        - updated_at (str): ISO 8601 timestamp when data was last updated
    """
    # Generate realistic mock data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1)
    
    return {
        "daily_post_counts_0_date": start_date.isoformat(),
        "daily_post_counts_0_count": 42,
        "daily_post_counts_1_date": end_date.isoformat(),
        "daily_post_counts_1_count": 58,
        "total_posts": 100,
        "time_range_start_date": start_date.isoformat(),
        "time_range_end_date": end_date.isoformat(),
        "updated_at": datetime.now().isoformat()
    }

def tabnews_integration_get_analytics_root_content_published() -> Dict[str, Any]:
    """
    Retrieves analytics on the number of posts published per day on TabNews.
    
    This function simulates integration with TabNews analytics API to get
    daily post counts for root content (top-level posts, not comments).
    
    Returns:
        Dict containing:
        - daily_post_counts (List[Dict]): List of objects with 'date' (str) and 'count' (int)
        - total_posts (int): Total number of posts across all days
        - time_range (Dict): Contains 'start_date' and 'end_date' in YYYY-MM-DD format
        - updated_at (str): ISO 8601 timestamp when data was last updated
    
    Example:
        {
            "daily_post_counts": [
                {"date": "2023-11-01", "count": 42},
                {"date": "2023-11-02", "count": 58}
            ],
            "total_posts": 100,
            "time_range": {
                "start_date": "2023-11-01",
                "end_date": "2023-11-02"
            },
            "updated_at": "2023-11-02T10:30:45.123456"
        }
    """
    try:
        # Fetch data from external API (mocked)
        api_data = call_external_api("tabnews-integration-get analytics root content published")
        
        # Construct daily_post_counts list from indexed fields
        daily_post_counts = [
            {
                "date": api_data["daily_post_counts_0_date"],
                "count": api_data["daily_post_counts_0_count"]
            },
            {
                "date": api_data["daily_post_counts_1_date"],
                "count": api_data["daily_post_counts_1_count"]
            }
        ]
        
        # Construct time_range object
        time_range = {
            "start_date": api_data["time_range_start_date"],
            "end_date": api_data["time_range_end_date"]
        }
        
        # Build final result structure matching output schema
        result = {
            "daily_post_counts": daily_post_counts,
            "total_posts": api_data["total_posts"],
            "time_range": time_range,
            "updated_at": api_data["updated_at"]
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process TabNews analytics data: {str(e)}")