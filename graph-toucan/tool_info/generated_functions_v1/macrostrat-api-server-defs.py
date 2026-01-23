from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Macrostrat server definitions.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first result entry
        - result_0_name (str): Name of the first result entry
        - result_0_definition (str): Definition of the first result entry
        - result_0_metadata_extra (str): Additional metadata for the first result
        - result_1_id (int): ID of the second result entry
        - result_1_name (str): Name of the second result entry
        - result_1_definition (str): Definition of the second result entry
        - result_1_metadata_extra (str): Additional metadata for the second result
        - total_count (int): Total number of records available
        - metadata_source_version (str): Version of the data source
        - metadata_update_timestamp (str): Timestamp of last update
        - metadata_api_endpoint (str): The API endpoint used
        - metadata_applied_filters (str): Filters applied in the query
        - pagination_offset (int): Pagination offset
        - pagination_limit (int): Pagination limit
        - pagination_page (int): Current page number
        - pagination_has_next (bool): Whether a next page exists
        - success (bool): Whether the request was successful
        - error_message (str): Error message if success is False
    """
    return {
        "result_0_id": 101,
        "result_0_name": "sandstone",
        "result_0_definition": "A sedimentary rock composed mainly of sand-sized minerals or rock grains.",
        "result_0_metadata_extra": "classified as clastic sedimentary rock",
        "result_1_id": 102,
        "result_1_name": "shale",
        "result_1_definition": "A fine-grained sedimentary rock that forms from mud that is a mix of flakes of clay minerals.",
        "result_1_metadata_extra": "typically laminated and fissile",
        "total_count": 150,
        "metadata_source_version": "v3.2",
        "metadata_update_timestamp": "2023-10-05T12:00:00Z",
        "metadata_api_endpoint": "/defs/lithology",
        "metadata_applied_filters": "class=siliciclastic",
        "pagination_offset": 0,
        "pagination_limit": 2,
        "pagination_page": 1,
        "pagination_has_next": True,
        "success": True,
        "error_message": ""
    }

def macrostrat_api_server_defs(endpoint: str, parameters: str) -> Dict[str, Any]:
    """
    Queries the Macrostrat API server definitions endpoint to retrieve standardized fields and dictionaries.
    
    Args:
        endpoint (str): The endpoint to query (e.g., 'lithology', 'stratigraphy', 'timescale').
        parameters (str): Parameters to pass to the endpoint (e.g., filters, options).
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionary objects with standardized fields like ID, name, definition, metadata.
        - total_count (int): Total number of records available for the queried endpoint.
        - metadata (Dict): Additional info including source version, update timestamp, API endpoint, and applied filters.
        - success (bool): Indicates whether the request was processed successfully.
        - error_message (str): Descriptive error message if success is False.
        - pagination (Dict): Pagination info with offset, limit, page, and has_next flag.
    """
    # Input validation
    if not endpoint:
        return {
            "results": [],
            "total_count": 0,
            "metadata": {},
            "success": False,
            "error_message": "Endpoint is required.",
            "pagination": {}
        }
    
    if not parameters:
        return {
            "results": [],
            "total_count": 0,
            "metadata": {},
            "success": False,
            "error_message": "Parameters are required.",
            "pagination": {}
        }

    try:
        # Call simulated external API
        api_data = call_external_api("macrostrat-api-server-defs")
        
        # Construct results list from indexed flat fields
        results = [
            {
                "id": api_data["result_0_id"],
                "name": api_data["result_0_name"],
                "definition": api_data["result_0_definition"],
                "metadata": {"extra": api_data["result_0_metadata_extra"]}
            },
            {
                "id": api_data["result_1_id"],
                "name": api_data["result_1_name"],
                "definition": api_data["result_1_definition"],
                "metadata": {"extra": api_data["result_1_metadata_extra"]}
            }
        ]
        
        # Construct metadata dictionary
        metadata = {
            "source_version": api_data["metadata_source_version"],
            "update_timestamp": api_data["metadata_update_timestamp"],
            "api_endpoint": api_data["metadata_api_endpoint"],
            "applied_filters": api_data["metadata_applied_filters"]
        }
        
        # Construct pagination dictionary
        pagination = {
            "offset": api_data["pagination_offset"],
            "limit": api_data["pagination_limit"],
            "page": api_data["pagination_page"],
            "has_next": api_data["pagination_has_next"]
        }
        
        # Final response structure
        response = {
            "results": results,
            "total_count": api_data["total_count"],
            "metadata": metadata,
            "success": api_data["success"],
            "error_message": api_data["error_message"],
            "pagination": pagination
        }
        
        return response
        
    except Exception as e:
        return {
            "results": [],
            "total_count": 0,
            "metadata": {},
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}",
            "pagination": {}
        }