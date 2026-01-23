from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching ratings data from external API for App Store app.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ratings (int): Total number of ratings for the app
        - histogram_1 (int): Count of 1-star ratings
        - histogram_2 (int): Count of 2-star ratings
        - histogram_3 (int): Count of 3-star ratings
        - histogram_4 (int): Count of 4-star ratings
        - histogram_5 (int): Count of 5-star ratings
        - country (str): Country code for which the ratings data was retrieved
        - last_updated (str): ISO 8601 timestamp indicating when the data was fetched
    """
    return {
        "ratings": 4500000,
        "histogram_1": 350000,
        "histogram_2": 280000,
        "histogram_3": 520000,
        "histogram_4": 950000,
        "histogram_5": 2400000,
        "country": "us",
        "last_updated": "2023-10-05T14:48:00Z"
    }

def app_market_intelligence_app_store_ratings(
    appId: Optional[str] = None,
    country: Optional[str] = "us",
    id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get ratings for an App Store app.

    Either appId or id must be provided to identify the app.

    Args:
        appId (Optional[str]): Bundle ID (e.g., 'com.midasplayer.apps.candycrushsaga'). Either this or id must be provided.
        country (Optional[str]): Country code to get ratings from (default: us)
        id (Optional[int]): Numeric App ID (e.g., 553834731). Either this or appId must be provided.

    Returns:
        Dict containing:
        - ratings (int): Total number of ratings for the app
        - histogram (Dict): Distribution of ratings by star level (1-5 stars)
        - country (str): Country code for which the ratings data was retrieved
        - last_updated (str): ISO 8601 timestamp indicating when the ratings data was last updated or fetched

    Raises:
        ValueError: If neither appId nor id is provided
    """
    if not appId and not id:
        raise ValueError("Either appId or id must be provided")

    # Normalize country code
    resolved_country = country.lower() if country else "us"

    # Fetch simulated data from external API
    api_data = call_external_api("app-market-intelligence-app-store-ratings")

    # Construct histogram from flattened fields
    histogram = {
        "1": api_data["histogram_1"],
        "2": api_data["histogram_2"],
        "3": api_data["histogram_3"],
        "4": api_data["histogram_4"],
        "5": api_data["histogram_5"]
    }

    # Build final result matching output schema
    result = {
        "ratings": api_data["ratings"],
        "histogram": histogram,
        "country": resolved_country,
        "last_updated": api_data["last_updated"]
    }

    return result