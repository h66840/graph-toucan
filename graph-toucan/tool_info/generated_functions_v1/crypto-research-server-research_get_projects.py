from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for research projects.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_project_name (str): Name of the first project
        - results_0_description (str): Description of the first project
        - results_0_research_domain (str): Research domain of the first project
        - results_0_publication_date (str): Publication date of the first project
        - results_0_associated_researchers (str): Comma-separated researchers of the first project
        - results_0_institutions (str): Comma-separated institutions of the first project
        - results_1_project_name (str): Name of the second project
        - results_1_description (str): Description of the second project
        - results_1_research_domain (str): Research domain of the second project
        - results_1_publication_date (str): Publication date of the second project
        - results_1_associated_researchers (str): Comma-separated researchers of the second project
        - results_1_institutions (str): Comma-separated institutions of the second project
        - total_count (int): Total number of matching projects
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages are available
        - metadata_timestamp (str): Timestamp of the request
        - metadata_database_version (str): Version of the source database
        - metadata_default_filter (str): Any default filter applied
        - metadata_sorting_criteria (str): Sorting criteria used
    """
    return {
        "results_0_project_name": "Quantum-Resistant Blockchain Protocols",
        "results_0_description": "Exploring post-quantum cryptographic algorithms for blockchain security.",
        "results_0_research_domain": "Cryptography",
        "results_0_publication_date": "2023-09-15",
        "results_0_associated_researchers": "Dr. Alice Chen, Prof. Bob Liu",
        "results_0_institutions": "MIT, Stanford University",
        "results_1_project_name": "Decentralized Identity Verification",
        "results_1_description": "A novel approach to self-sovereign identity using zero-knowledge proofs.",
        "results_1_research_domain": "Identity Management",
        "results_1_publication_date": "2023-08-22",
        "results_1_associated_researchers": "Dr. Carol Wang, Dr. David Kim",
        "results_1_institutions": "UC Berkeley, ETH Zurich",
        "total_count": 42,
        "page": 1,
        "page_size": 2,
        "has_more": True,
        "metadata_timestamp": "2024-01-15T10:30:00Z",
        "metadata_database_version": "v2.3.1",
        "metadata_default_filter": "published:true",
        "metadata_sorting_criteria": "relevance"
    }

def crypto_research_server_research_get_projects() -> Dict[str, Any]:
    """
    Search for projects on the Research knowledge base.

    Returns:
        Dict containing:
        - results (List[Dict]): List of project entries with details like name, description,
          research domain, publication date, researchers, and institutions.
        - total_count (int): Total number of projects found.
        - page (int): Current page number.
        - page_size (int): Number of projects per page.
        - has_more (bool): Whether additional pages exist.
        - metadata (Dict): Contextual info about the query (timestamp, DB version, filters, sorting).
    
    Raises:
        KeyError: If expected fields are missing from the API response.
        Exception: For any other processing errors.
    """
    try:
        api_data = call_external_api("crypto-research-server-research_get_projects")

        # Construct results list from indexed fields
        results = [
            {
                "project_name": api_data["results_0_project_name"],
                "description": api_data["results_0_description"],
                "research_domain": api_data["results_0_research_domain"],
                "publication_date": api_data["results_0_publication_date"],
                "associated_researchers": api_data["results_0_associated_researchers"].split(", "),
                "institutions": api_data["results_0_institutions"].split(", ")
            },
            {
                "project_name": api_data["results_1_project_name"],
                "description": api_data["results_1_description"],
                "research_domain": api_data["results_1_research_domain"],
                "publication_date": api_data["results_1_publication_date"],
                "associated_researchers": api_data["results_1_associated_researchers"].split(", "),
                "institutions": api_data["results_1_institutions"].split(", ")
            }
        ]

        # Construct metadata
        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "database_version": api_data["metadata_database_version"],
            "default_filter": api_data["metadata_default_filter"],
            "sorting_criteria": api_data["metadata_sorting_criteria"]
        }

        # Build final response
        response = {
            "results": results,
            "total_count": api_data["total_count"],
            "page": api_data["page"],
            "page_size": api_data["page_size"],
            "has_more": api_data["has_more"],
            "metadata": metadata
        }

        return response

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise Exception(f"Error processing research projects data: {e}")