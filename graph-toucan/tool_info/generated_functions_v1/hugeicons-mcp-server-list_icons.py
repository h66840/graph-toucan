from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugeicons icon listing.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - icon_0_name (str): Name of the first icon
        - icon_0_tags (str): Comma-separated tags for the first icon
        - icon_0_categories (str): Comma-separated categories for the first icon
        - icon_0_format (str): File format of the first icon
        - icon_0_available (bool): Availability status of the first icon
        - icon_1_name (str): Name of the second icon
        - icon_1_tags (str): Comma-separated tags for the second icon
        - icon_1_categories (str): Comma-separated categories for the second icon
        - icon_1_format (str): File format of the second icon
        - icon_1_available (bool): Availability status of the second icon
        - total_count (int): Total number of icons available
        - metadata_timestamp (str): Timestamp of the request
        - metadata_version (str): Version of the icon library
        - metadata_filters (str): Filters applied during listing
    """
    return {
        "icon_0_name": "arrow-up",
        "icon_0_tags": "up, direction, navigation",
        "icon_0_categories": "arrows, navigation",
        "icon_0_format": "svg",
        "icon_0_available": True,
        "icon_1_name": "check-circle",
        "icon_1_tags": "success, confirm, done",
        "icon_1_categories": "ui, status",
        "icon_1_format": "svg",
        "icon_1_available": True,
        "total_count": 2500,
        "metadata_timestamp": "2023-10-15T14:30:00Z",
        "metadata_version": "1.5.2",
        "metadata_filters": "none"
    }

def hugeicons_mcp_server_list_icons() -> Dict[str, Any]:
    """
    Get a list of all available Hugeicons icons.
    
    This function retrieves metadata about Hugeicons icons including name, tags, categories,
    file format, and availability. It also returns the total count of icons and additional
    metadata about the response.
    
    Returns:
        Dict containing:
        - icons (List[Dict]): List of icon objects with metadata
        - total_count (int): Total number of icons available
        - metadata (Dict): Additional information about the response
    """
    try:
        api_data = call_external_api("hugeicons-mcp-server-list_icons")
        
        # Construct list of icons from flattened API data
        icons = [
            {
                "name": api_data["icon_0_name"],
                "tags": api_data["icon_0_tags"].split(", "),
                "categories": api_data["icon_0_categories"].split(", "),
                "format": api_data["icon_0_format"],
                "available": api_data["icon_0_available"]
            },
            {
                "name": api_data["icon_1_name"],
                "tags": api_data["icon_1_tags"].split(", "),
                "categories": api_data["icon_1_categories"].split(", "),
                "format": api_data["icon_1_format"],
                "available": api_data["icon_1_available"]
            }
        ]
        
        # Construct metadata dictionary
        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "version": api_data["metadata_version"],
            "filters": api_data["metadata_filters"]
        }
        
        # Assemble final result
        result = {
            "icons": icons,
            "total_count": api_data["total_count"],
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve icon list: {str(e)}")