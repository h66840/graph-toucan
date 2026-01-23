from typing import Dict, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Sci-Hub DOI lookup.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_title (str): Title of the paper
        - result_authors (str): Comma-separated list of authors
        - result_journal (str): Name of the journal
        - result_year (int): Publication year
        - result_url (str): URL to the paper on Sci-Hub
        - result_pdf_link (str): Direct link to the PDF
        - success (bool): Whether the lookup was successful
        - error_message (str): Error description if any
        - cached (bool): Whether the result was served from cache
        - timestamp (str): ISO 8601 timestamp of response generation
    """
    return {
        "result_title": "A Comprehensive Study on Climate Change Impacts",
        "result_authors": "John Doe, Jane Smith, Robert Johnson",
        "result_journal": "Journal of Environmental Science",
        "result_year": 2023,
        "result_url": "https://sci-hub.se/10.1000/climate2023",
        "result_pdf_link": "https://sci-hub.se/pdf/10.1000/climate2023.pdf",
        "success": True,
        "error_message": "",
        "cached": False,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def sci_hub_mcp_server_search_scihub_by_doi(doi: str) -> Dict[str, Any]:
    """
    Searches Sci-Hub for a paper using its DOI and returns metadata and access details.

    Args:
        doi (str): The Digital Object Identifier (DOI) of the paper to search.

    Returns:
        Dict containing:
        - result (Dict): Paper metadata including title, authors, journal, year, url, and pdf_link
        - success (bool): Whether the lookup was successful
        - error_message (str): Description of any error encountered
        - cached (bool): Whether the result was retrieved from cache
        - timestamp (str): ISO 8601 timestamp when the response was generated

    Raises:
        ValueError: If DOI is empty or invalid
    """
    if not doi or not doi.strip():
        return {
            "result": {},
            "success": False,
            "error_message": "DOI is required",
            "cached": False,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    # Call external API simulation
    api_data = call_external_api("sci-hub-mcp-server-search_scihub_by_doi")

    # Construct result dictionary from flattened API response
    result_dict = {
        "title": api_data["result_title"],
        "authors": api_data["result_authors"],
        "journal": api_data["result_journal"],
        "year": api_data["result_year"],
        "url": api_data["result_url"],
        "pdf_link": api_data["result_pdf_link"]
    }

    # Final response structure
    response = {
        "result": result_dict,
        "success": api_data["success"],
        "error_message": api_data["error_message"] if api_data["error_message"] else "",
        "cached": api_data["cached"],
        "timestamp": api_data["timestamp"]
    }

    return response