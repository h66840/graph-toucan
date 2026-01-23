from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching feature analytics data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - feature_0_name (str): Name of the first feature
        - feature_0_create_count (int): Create operations count for first feature
        - feature_0_read_count (int): Read operations count for first feature
        - feature_0_update_count (int): Update operations count for first feature
        - feature_0_delete_count (int): Delete operations count for first feature
        - feature_0_total_count (int): Total operations count for first feature
        - feature_1_name (str): Name of the second feature
        - feature_1_create_count (int): Create operations count for second feature
        - feature_1_read_count (int): Read operations count for second feature
        - feature_1_update_count (int): Update operations count for second feature
        - feature_1_delete_count (int): Delete operations count for second feature
        - feature_1_total_count (int): Total operations count for second feature
        - total_operations (int): Total number of CRUD operations across all features
        - date_range_start_date (str): Start date of analytics period in ISO format
        - date_range_end_date (str): End date of analytics period in ISO format
    """
    return {
        "feature_0_name": "comments",
        "feature_0_create_count": 1450,
        "feature_0_read_count": 8920,
        "feature_0_update_count": 320,
        "feature_0_delete_count": 89,
        "feature_0_total_count": 10779,
        "feature_1_name": "huddles",
        "feature_1_create_count": 780,
        "feature_1_read_count": 4320,
        "feature_1_update_count": 156,
        "feature_1_delete_count": 45,
        "feature_1_total_count": 5301,
        "total_operations": 16080,
        "date_range_start_date": "2023-10-01",
        "date_range_end_date": "2023-10-31"
    }

def velt_analytics_server_get_feature_analytics_count(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get comprehensive feature analytics data from Velt, showing CRUD operation counts for each feature.
    
    This function retrieves detailed analytics about how different Velt features are being used.
    It provides granular insights into user interactions with various Velt features by querying
    simulated analytics data.
    
    Args:
        data (Dict[str, Any]): Input parameters for the query including:
            - date (Optional[str]): Specific date for analytics (ISO format)
            - lastDaysCount (Optional[int]): Number of recent days to include
            - startDate (Optional[str]): Start date for custom range (ISO format)
            - endDate (Optional[str]): End date for custom range (ISO format)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - features (List[Dict]): List of feature usage analytics with name and CRUD counts
            - total_operations (int): Total number of CRUD operations across all features
            - date_range (Dict): Dictionary with start_date and end_date in ISO format
    
    Raises:
        ValueError: If invalid date formats are provided or conflicting parameters are used
    """
    # Input validation
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary")
    
    # Validate date parameters if provided
    if "date" in data and data["date"]:
        try:
            datetime.fromisoformat(data["date"].replace("Z", ""))
        except ValueError:
            raise ValueError(f"Invalid date format: {data['date']}. Expected ISO format.")
    
    if "startDate" in data and data["startDate"]:
        try:
            datetime.fromisoformat(data["startDate"].replace("Z", ""))
        except ValueError:
            raise ValueError(f"Invalid startDate format: {data['startDate']}. Expected ISO format.")
    
    if "endDate" in data and data["endDate"]:
        try:
            datetime.fromisoformat(data["endDate"].replace("Z", ""))
        except ValueError:
            raise ValueError(f"Invalid endDate format: {data['endDate']}. Expected ISO format.")
    
    # Call external API to get the data (with only simple fields)
    api_data = call_external_api("velt-analytics-server-get_feature_analytics_count")
    
    # Construct the nested output structure from flat API data
    features = [
        {
            "name": api_data["feature_0_name"],
            "create_count": api_data["feature_0_create_count"],
            "read_count": api_data["feature_0_read_count"],
            "update_count": api_data["feature_0_update_count"],
            "delete_count": api_data["feature_0_delete_count"],
            "total_count": api_data["feature_0_total_count"]
        },
        {
            "name": api_data["feature_1_name"],
            "create_count": api_data["feature_1_create_count"],
            "read_count": api_data["feature_1_read_count"],
            "update_count": api_data["feature_1_update_count"],
            "delete_count": api_data["feature_1_delete_count"],
            "total_count": api_data["feature_1_total_count"]
        }
    ]
    
    result = {
        "features": features,
        "total_operations": api_data["total_operations"],
        "date_range": {
            "start_date": api_data["date_range_start_date"],
            "end_date": api_data["date_range_end_date"]
        }
    }
    
    return result