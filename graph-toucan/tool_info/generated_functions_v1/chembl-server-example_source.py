from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL source information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - source_0_source_id (str): Unique identifier for the first source
        - source_0_source_description (str): Description of the first source
        - source_0_url (str): URL of the first source
        - source_0_reference (str): Reference (e.g., DOI or PubMed ID) for the first source
        - source_0_last_accessed_date (str): Last accessed date of the first source in ISO format
        - source_1_source_id (str): Unique identifier for the second source
        - source_1_source_description (str): Description of the second source
        - source_1_url (str): URL of the second source
        - source_1_reference (str): Reference (e.g., DOI or PubMed ID) for the second source
        - source_1_last_accessed_date (str): Last accessed date of the second source in ISO format
        - count (int): Total number of sources returned
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, otherwise empty string
    """
    return {
        "source_0_source_id": "SRC001",
        "source_0_source_description": "ChEMBL database release notes",
        "source_0_url": "https://www.ebi.ac.uk/chembl/release_notes",
        "source_0_reference": "doi:10.1093/nar/gkx1010",
        "source_0_last_accessed_date": "2023-10-05T14:30:00Z",
        "source_1_source_id": "SRC002",
        "source_1_source_description": "ChEMBL documentation portal",
        "source_1_url": "https://docs.chembl.org",
        "source_1_reference": "pmid:31691827",
        "source_1_last_accessed_date": "2023-09-28T09:15:00Z",
        "count": 2,
        "success": True,
        "error_message": "",
    }


def chembl_server_example_source(source_description: str) -> Dict[str, Any]:
    """
    Get source information for the specified description.

    Args:
        source_description (str): Source description to query.

    Returns:
        Dict containing:
        - sources (List[Dict]): List of source information objects with keys:
            - source_id (str)
            - source_description (str)
            - url (str)
            - reference (str)
            - last_accessed_date (str)
        - count (int): Total number of sources returned
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, otherwise empty string
    """
    # Input validation
    if not source_description or not isinstance(source_description, str):
        return {
            "sources": [],
            "count": 0,
            "success": False,
            "error_message": "Invalid input: source_description must be a non-empty string."
        }

    try:
        # Call external API (simulated)
        api_data = call_external_api("chembl-server-example_source")

        # Construct sources list from flattened API response
        sources = [
            {
                "source_id": api_data["source_0_source_id"],
                "source_description": api_data["source_0_source_description"],
                "url": api_data["source_0_url"],
                "reference": api_data["source_0_reference"],
                "last_accessed_date": api_data["source_0_last_accessed_date"]
            },
            {
                "source_id": api_data["source_1_source_id"],
                "source_description": api_data["source_1_source_description"],
                "url": api_data["source_1_url"],
                "reference": api_data["source_1_reference"],
                "last_accessed_date": api_data["source_1_last_accessed_date"]
            }
        ]

        # Return structured response
        return {
            "sources": sources,
            "count": api_data["count"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }

    except Exception as e:
        return {
            "sources": [],
            "count": 0,
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}"
        }