from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching organization analytics data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - organization_0_organization_id (str): ID of first top organization
        - organization_0_name (str): Name of first top organization
        - organization_0_total_count (int): Total activity count for first org
        - organization_0_comments_count (int): Comment count for first org
        - organization_0_huddles_count (int): Huddles count for first org
        - organization_0_arrows_count (int): Arrows count for first org
        - organization_0_notifications_count (int): Notifications count for first org
        - organization_0_recordings_count (int): Recordings count for first org
        - organization_1_organization_id (str): ID of second top organization
        - organization_1_name (str): Name of second top organization
        - organization_1_total_count (int): Total activity count for second org
        - organization_1_comments_count (int): Comment count for second org
        - organization_1_huddles_count (int): Huddles count for second org
        - organization_1_arrows_count (int): Arrows count for second org
        - organization_1_notifications_count (int): Notifications count for second org
        - organization_1_recordings_count (int): Recordings count for second org
        - total_results (int): Total number of organizations matching criteria
        - date_range_start_date (str): Start date in ISO format
        - date_range_end_date (str): End date in ISO format
        - parameters_used_topNumber (int): Number of top organizations requested
        - parameters_used_orderBy (str): Field used for ordering results
        - parameters_used_asc (bool): Whether sorting is ascending
        - parameters_used_lastDaysCount (int or None): Number of recent days considered
        - parameters_used_custom_date_range (bool): Whether custom date range was used
        - generated_at (str): Timestamp when report was generated (ISO format)
        - success (bool): Whether request was processed successfully
    """
    now = datetime.utcnow()
    start_date = (now - timedelta(days=30)).isoformat()
    end_date = now.isoformat()
    generated_at = now.isoformat()
    
    return {
        "organization_0_organization_id": "org_1a2b3c",
        "organization_0_name": "Alpha Technologies",
        "organization_0_total_count": 1542,
        "organization_0_comments_count": 890,
        "organization_0_huddles_count": 320,
        "organization_0_arrows_count": 180,
        "organization_0_notifications_count": 95,
        "organization_0_recordings_count": 57,
        
        "organization_1_organization_id": "org_4d5e6f",
        "organization_1_name": "Beta Innovations",
        "organization_1_total_count": 1234,
        "organization_1_comments_count": 720,
        "organization_1_huddles_count": 280,
        "organization_1_arrows_count": 150,
        "organization_1_notifications_count": 84,
        "organization_1_recordings_count": 46,
        
        "total_results": 42,
        "date_range_start_date": start_date,
        "date_range_end_date": end_date,
        "parameters_used_topNumber": 2,
        "parameters_used_orderBy": "total_count",
        "parameters_used_asc": False,
        "parameters_used_lastDaysCount": 30,
        "parameters_used_custom_date_range": False,
        "generated_at": generated_at,
        "success": True
    }

def velt_analytics_server_get_organization_top_number_analytics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get organization analytics from Velt.
    
    This function retrieves top organizations based on activity metrics within a specified time period.
    It returns detailed analytics including various interaction counts and metadata about the query.
    
    Args:
        data (Dict[str, Any]): Input parameters for the analytics query. Expected keys include:
            - topNumber (int): Number of top organizations to return
            - orderBy (str): Field to order results by
            - asc (bool): Whether to sort in ascending order
            - lastDaysCount (Optional[int]): Number of recent days to include in analysis
            - startDate (Optional[str]): Custom start date in ISO format
            - endDate (Optional[str]): Custom end date in ISO format
    
    Returns:
        Dict containing:
            - organizations (List[Dict]): List of top organizations with their analytics metrics
            - total_results (int): Total number of organizations that matched criteria
            - date_range (Dict): Contains start_date and end_date in ISO format
            - parameters_used (Dict): Summary of key analysis parameters applied
            - generated_at (str): Timestamp when the analytics report was generated (ISO format)
            - success (bool): Whether the request was processed successfully
    """
    # Validate input
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary")
    
    # Extract parameters with defaults
    top_number = data.get("topNumber", 2)
    order_by = data.get("orderBy", "total_count")
    asc = data.get("asc", False)
    last_days_count = data.get("lastDaysCount")
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    
    # Validate parameters
    if not isinstance(top_number, int) or top_number <= 0:
        raise ValueError("topNumber must be a positive integer")
    if not isinstance(order_by, str):
        raise ValueError("orderBy must be a string")
    if not isinstance(asc, bool):
        raise ValueError("asc must be a boolean")
    if last_days_count is not None and (not isinstance(last_days_count, int) or last_days_count <= 0):
        raise ValueError("lastDaysCount must be a positive integer or null")
    if start_date is not None and not isinstance(start_date, str):
        raise ValueError("startDate must be a string in ISO format or null")
    if end_date is not None and not isinstance(end_date, str):
        raise ValueError("endDate must be a string in ISO format or null")
    
    # Call external API to get data
    api_data = call_external_api("velt-analytics-server-get_organization_top_number_analytics")
    
    # Construct organizations list from flattened API response
    organizations: List[Dict[str, Any]] = []
    
    for i in range(2):  # We have data for 2 organizations (0 and 1)
        org_id_key = f"organization_{i}_organization_id"
        if org_id_key not in api_data:
            continue
            
        org = {
            "organization_id": api_data[org_id_key],
            "name": api_data.get(f"organization_{i}_name"),
            "total_count": api_data[f"organization_{i}_total_count"],
            "comments_count": api_data[f"organization_{i}_comments_count"],
            "huddles_count": api_data[f"organization_{i}_huddles_count"],
            "arrows_count": api_data[f"organization_{i}_arrows_count"],
            "notifications_count": api_data[f"organization_{i}_notifications_count"],
            "recordings_count": api_data[f"organization_{i}_recordings_count"]
        }
        organizations.append(org)
    
    # Construct result following output schema
    result = {
        "organizations": organizations,
        "total_results": api_data["total_results"],
        "date_range": {
            "start_date": api_data["date_range_start_date"],
            "end_date": api_data["date_range_end_date"]
        },
        "parameters_used": {
            "topNumber": api_data["parameters_used_topNumber"],
            "orderBy": api_data["parameters_used_orderBy"],
            "asc": api_data["parameters_used_asc"],
            "lastDaysCount": api_data["parameters_used_lastDaysCount"],
            "custom_date_range": api_data["parameters_used_custom_date_range"]
        },
        "generated_at": api_data["generated_at"],
        "success": api_data["success"]
    }
    
    return result