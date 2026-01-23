from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play categories.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - category_0 (str): First Google Play category identifier
        - category_1 (str): Second Google Play category identifier
        - total_count (int): Total number of categories returned
        - metadata_source (str): Source of the data
        - metadata_fetched_at (str): ISO format timestamp when data was fetched
        - metadata_version (str): Version of the data
    """
    return {
        "category_0": "GAME",
        "category_1": "PRODUCTIVITY",
        "total_count": 2,
        "metadata_source": "Google Play Store API",
        "metadata_fetched_at": datetime.now().isoformat(),
        "metadata_version": "1.0"
    }


def app_market_intelligence_google_play_categories() -> Dict[str, Any]:
    """
    Get list of all Google Play categories.

    Returns:
        Dict containing:
        - categories (List[str]): List of Google Play category identifiers
          (e.g., 'GAME', 'PRODUCTIVITY', 'AUTO_AND_VEHICLES')
        - total_count (int): Total number of categories returned
        - metadata (Dict): Additional information about the response with keys:
          - source (str): Data source
          - fetched_at (str): ISO datetime string of when data was fetched
          - version (str): API/data version
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("app-market-intelligence-google-play-categories")

        # Construct categories list from indexed fields
        categories = [
            api_data["category_0"],
            api_data["category_1"]
        ]

        # Construct metadata dictionary from flattened fields
        metadata = {
            "source": api_data["metadata_source"],
            "fetched_at": api_data["metadata_fetched_at"],
            "version": api_data["metadata_version"]
        }

        # Build final result matching output schema
        result = {
            "categories": categories,
            "total_count": api_data["total_count"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve Google Play categories: {str(e)}")