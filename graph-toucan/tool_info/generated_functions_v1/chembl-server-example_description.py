from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching description data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - description_0_identifier (str): Identifier of the first described entity
        - description_0_text (str): Description text for the first entity
        - description_0_source (str): Source of the first description
        - description_0_metadata (str): Metadata for the first description as JSON string
        - description_1_identifier (str): Identifier of the second described entity
        - description_1_text (str): Description text for the second entity
        - description_1_source (str): Source of the second description
        - description_1_metadata (str): Metadata for the second description as JSON string
        - count (int): Total number of descriptions returned
        - description_type (str): The type of description requested
        - metadata_version (str): Data source version
        - metadata_timestamp (str): Timestamp of the response
        - metadata_warnings (str): Warnings if any entries were omitted, as JSON string
    """
    return {
        "description_0_identifier": "CHEMBL1234",
        "description_0_text": "This compound is a potent inhibitor of kinase activity.",
        "description_0_source": "ChEMBL database",
        "description_0_metadata": '{"confidence": 0.95, "curated_by": "expert"}',
        "description_1_identifier": "CHEMBL5678",
        "description_1_text": "This target is associated with inflammatory diseases.",
        "description_1_source": "UniProt",
        "description_1_metadata": '{"confidence": 0.87, "curated_by": "automated"}',
        "count": 2,
        "description_type": "compound",
        "metadata_version": "29.0",
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_warnings": '["partial_match"]'
    }

def chembl_server_example_description(description_type: str) -> Dict[str, Any]:
    """
    Get description data for the specified type.
    
    Args:
        description_type (str): The type of description to retrieve (e.g., 'target', 'compound', 'assay')
        
    Returns:
        Dict containing:
        - descriptions (List[Dict]): List of description objects with identifier, text, source, and metadata
        - count (int): Total number of descriptions returned
        - description_type (str): The requested description type
        - metadata (Dict): Additional information about the response including version, timestamp, and warnings
    """
    if not description_type:
        raise ValueError("description_type is required and cannot be empty")
        
    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_description")
    
    # Construct descriptions list from indexed fields
    descriptions = [
        {
            "identifier": api_data["description_0_identifier"],
            "text": api_data["description_0_text"],
            "source": api_data["description_0_source"],
            "metadata": api_data["description_0_metadata"]
        },
        {
            "identifier": api_data["description_1_identifier"],
            "text": api_data["description_1_text"],
            "source": api_data["description_1_source"],
            "metadata": api_data["description_1_metadata"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "descriptions": descriptions,
        "count": api_data["count"],
        "description_type": api_data["description_type"],
        "metadata": {
            "version": api_data["metadata_version"],
            "timestamp": api_data["metadata_timestamp"],
            "warnings": api_data["metadata_warnings"]
        }
    }
    
    return result