from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Scholar author information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - author_id (str): Unique identifier for the author in Google Scholar
        - name (str): Full name of the academic author
        - affiliation (str): Primary institutional affiliation or university
        - homepage_url (str): URL to the author's personal or professional homepage
        - email_domain (str): Email domain associated with the author (e.g., '@stanford.edu')
        - cited_by_count (int): Total number of citations across all publications
        - h_index (int): Hirsch index (h-index) representing productivity and citation impact
        - i10_index (int): Number of publications with at least 10 citations
        - publication_count (int): Total number of indexed publications
        - publication_0_title (str): Title of the first publication
        - publication_0_year (int): Year of the first publication
        - publication_0_cited_by (int): Citation count for the first publication
        - publication_0_journal (str): Journal name for the first publication
        - publication_0_author_0 (str): First author of the first publication
        - publication_0_author_1 (str): Second author of the first publication
        - publication_1_title (str): Title of the second publication
        - publication_1_year (int): Year of the second publication
        - publication_1_cited_by (int): Citation count for the second publication
        - publication_1_journal (str): Journal name for the second publication
        - publication_1_author_0 (str): First author of the second publication
        - publication_1_author_1 (str): Second author of the second publication
        - coauthor_0_name (str): Name of the first coauthor
        - coauthor_0_affiliation (str): Affiliation of the first coauthor
        - coauthor_0_author_id (str): Author ID of the first coauthor
        - coauthor_1_name (str): Name of the second coauthor
        - coauthor_1_affiliation (str): Affiliation of the second coauthor
        - coauthor_1_author_id (str): Author ID of the second coauthor
        - filled_fields (str): Comma-separated list of field names that were successfully retrieved
        - retrieval_status (str): Status of the request ('success', 'not_found', etc.)
        - retrieval_timestamp (str): ISO 8601 timestamp when the data was fetched
    """
    return {
        "author_id": "scholar123",
        "name": "Dr. Jane Smith",
        "affiliation": "Stanford University",
        "homepage_url": "https://janesmith.stanford.edu",
        "email_domain": "@stanford.edu",
        "cited_by_count": 4500,
        "h_index": 45,
        "i10_index": 98,
        "publication_count": 150,
        "publication_0_title": "Advancements in Machine Learning",
        "publication_0_year": 2020,
        "publication_0_cited_by": 150,
        "publication_0_journal": "Journal of AI Research",
        "publication_0_author_0": "Jane Smith",
        "publication_0_author_1": "John Doe",
        "publication_1_title": "Neural Networks in Practice",
        "publication_1_year": 2018,
        "publication_1_cited_by": 210,
        "publication_1_journal": "IEEE Transactions on Neural Networks",
        "publication_1_author_0": "Jane Smith",
        "publication_1_author_1": "Alice Johnson",
        "coauthor_0_name": "John Doe",
        "coauthor_0_affiliation": "MIT",
        "coauthor_0_author_id": "jdoe_mit",
        "coauthor_1_name": "Alice Johnson",
        "coauthor_1_affiliation": "UC Berkeley",
        "coauthor_1_author_id": "ajohnson_berkeley",
        "filled_fields": "author_id,name,affiliation,homepage_url,email_domain,cited_by_count,h_index,i10_index,publication_count,publications,coauthors",
        "retrieval_status": "success",
        "retrieval_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def google_scholar_search_server_get_author_info(author_name: str) -> Dict[str, Any]:
    """
    Retrieves detailed academic profile information for an author from Google Scholar.

    Args:
        author_name (str): The full name of the academic author to search for.

    Returns:
        Dict containing the following keys:
        - author_id (str): Unique identifier for the author in Google Scholar
        - name (str): Full name of the academic author
        - affiliation (str): Primary institutional affiliation or university
        - homepage_url (str): URL to the author's personal or professional homepage
        - email_domain (str): Email domain associated with the author
        - cited_by_count (int): Total number of citations across all publications
        - h_index (int): Hirsch index (h-index)
        - i10_index (int): Number of publications with at least 10 citations
        - publication_count (int): Total number of indexed publications
        - publications (List[Dict]): List of publication entries with keys:
            - title (str)
            - year (int)
            - cited_by (int)
            - journal (str)
            - authors (List[str])
        - coauthors (List[Dict]): List of coauthors with keys:
            - name (str)
            - affiliation (str)
            - author_id (str)
        - filled_fields (List[str]): List of field names that were successfully retrieved
        - retrieval_status (str): Status of the request ('success', 'not_found', etc.)
        - retrieval_timestamp (str): ISO 8601 timestamp when the data was fetched

    Raises:
        ValueError: If author_name is empty or not a string
    """
    if not author_name or not isinstance(author_name, str):
        raise ValueError("author_name must be a non-empty string")

    # Fetch data from simulated external API
    api_data = call_external_api("google-scholar-search-server-get_author_info")

    # Construct publications list
    publications = [
        {
            "title": api_data["publication_0_title"],
            "year": api_data["publication_0_year"],
            "cited_by": api_data["publication_0_cited_by"],
            "journal": api_data["publication_0_journal"],
            "authors": [
                api_data["publication_0_author_0"],
                api_data["publication_0_author_1"]
            ]
        },
        {
            "title": api_data["publication_1_title"],
            "year": api_data["publication_1_year"],
            "cited_by": api_data["publication_1_cited_by"],
            "journal": api_data["publication_1_journal"],
            "authors": [
                api_data["publication_1_author_0"],
                api_data["publication_1_author_1"]
            ]
        }
    ]

    # Construct coauthors list
    coauthors = [
        {
            "name": api_data["coauthor_0_name"],
            "affiliation": api_data["coauthor_0_affiliation"],
            "author_id": api_data["coauthor_0_author_id"]
        },
        {
            "name": api_data["coauthor_1_name"],
            "affiliation": api_data["coauthor_1_affiliation"],
            "author_id": api_data["coauthor_1_author_id"]
        }
    ]

    # Parse filled_fields from comma-separated string to list
    filled_fields = api_data["filled_fields"].split(",") if api_data["filled_fields"] else []

    # Construct final result matching output schema
    result = {
        "author_id": api_data["author_id"],
        "name": api_data["name"],
        "affiliation": api_data["affiliation"],
        "homepage_url": api_data["homepage_url"],
        "email_domain": api_data["email_domain"],
        "cited_by_count": api_data["cited_by_count"],
        "h_index": api_data["h_index"],
        "i10_index": api_data["i10_index"],
        "publication_count": api_data["publication_count"],
        "publications": publications,
        "coauthors": coauthors,
        "filled_fields": filled_fields,
        "retrieval_status": api_data["retrieval_status"],
        "retrieval_timestamp": api_data["retrieval_timestamp"]
    }

    return result