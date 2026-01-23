from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for academic author network co-authors.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - coauthor_0_name (str): First co-author's first name
        - coauthor_0_surname (str): First co-author's last name
        - coauthor_0_institution (str): First co-author's institution
        - coauthor_0_field (str): First co-author's research field
        - coauthor_0_joint_publications (int): Number of joint publications with first co-author
        - coauthor_0_collaboration_strength (float): Collaboration strength score for first co-author
        - coauthor_1_name (str): Second co-author's first name
        - coauthor_1_surname (str): Second co-author's last name
        - coauthor_1_institution (str): Second co-author's institution
        - coauthor_1_field (str): Second co-author's research field
        - coauthor_1_joint_publications (int): Number of joint publications with second co-author
        - coauthor_1_collaboration_strength (float): Collaboration strength score for second co-author
        - total_coauthors (int): Total number of co-authors found
        - author_info_name (str): Queried author's first name
        - author_info_surname (str): Queried author's last name
        - author_info_institution (str): Queried author's primary institution
        - author_info_field (str): Queried author's research field
        - author_info_publication_count (int): Total publication count of queried author
        - metadata_timestamp (str): ISO format timestamp of query execution
        - metadata_data_source (str): Source of the academic data
        - metadata_filter_institution_used (bool): Whether institution filter was applied
        - metadata_filter_field_used (bool): Whether research field filter was applied
    """
    return {
        "coauthor_0_name": "Jane",
        "coauthor_0_surname": "Smith",
        "coauthor_0_institution": "MIT",
        "coauthor_0_field": "Computer Science",
        "coauthor_0_joint_publications": 15,
        "coauthor_0_collaboration_strength": 0.85,
        "coauthor_1_name": "John",
        "coauthor_1_surname": "Doe",
        "coauthor_1_institution": "Stanford University",
        "coauthor_1_field": "Artificial Intelligence",
        "coauthor_1_joint_publications": 8,
        "coauthor_1_collaboration_strength": 0.62,
        "total_coauthors": 23,
        "author_info_name": "Alice",
        "author_info_surname": "Johnson",
        "author_info_institution": "Harvard University",
        "author_info_field": "Machine Learning",
        "author_info_publication_count": 47,
        "metadata_timestamp": datetime.now().isoformat(),
        "metadata_data_source": "AcademicDB v2.1",
        "metadata_filter_institution_used": True,
        "metadata_filter_field_used": False,
    }


def academic_author_network_get_coauthors(
    name: str,
    surname: str,
    institution: Optional[str] = None,
    field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all co-authors for a given author.

    Args:
        name (str): Author's first name (required)
        surname (str): Author's last name (required)
        institution (Optional[str]): Optional institution affiliation to filter results
        field (Optional[str]): Optional research field to filter results

    Returns:
        Dict containing:
        - coauthors (List[Dict]): List of co-author dictionaries with details
        - total_coauthors (int): Total number of co-authors found
        - author_info (Dict): Information about the queried author
        - metadata (Dict): Metadata about the query execution

    Raises:
        ValueError: If name or surname is empty or None
    """
    # Input validation
    if not name or not isinstance(name, str):
        raise ValueError("Author's first name is required and must be a non-empty string.")
    if not surname or not isinstance(surname, str):
        raise ValueError("Author's last name is required and must be a non-empty string.")

    # Call external API to get flattened data
    api_data = call_external_api("academic-author-network-get_coauthors")

    # Construct co-authors list from indexed fields
    coauthors = [
        {
            "name": api_data["coauthor_0_name"],
            "surname": api_data["coauthor_0_surname"],
            "institution": api_data["coauthor_0_institution"],
            "field": api_data["coauthor_0_field"],
            "joint_publications": api_data["coauthor_0_joint_publications"],
            "collaboration_strength": api_data["coauthor_0_collaboration_strength"]
        },
        {
            "name": api_data["coauthor_1_name"],
            "surname": api_data["coauthor_1_surname"],
            "institution": api_data["coauthor_1_institution"],
            "field": api_data["coauthor_1_field"],
            "joint_publications": api_data["coauthor_1_joint_publications"],
            "collaboration_strength": api_data["coauthor_1_collaboration_strength"]
        }
    ]

    # Construct author info
    author_info = {
        "name": api_data["author_info_name"],
        "surname": api_data["author_info_surname"],
        "institution": api_data["author_info_institution"],
        "field": api_data["author_info_field"],
        "publication_count": api_data["author_info_publication_count"]
    }

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "data_source": api_data["metadata_data_source"],
        "filters": {
            "institution": institution,
            "field": field
        },
        "filter_applied": {
            "institution": api_data["metadata_filter_institution_used"],
            "field": api_data["metadata_filter_field_used"]
        }
    }

    # Final result structure
    result = {
        "coauthors": coauthors,
        "total_coauthors": api_data["total_coauthors"],
        "author_info": author_info,
        "metadata": metadata
    }

    return result