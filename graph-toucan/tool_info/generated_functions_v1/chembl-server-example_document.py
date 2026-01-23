from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching document data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - document_0_title (str): Title of the first document
        - document_0_authors (str): Authors of the first document (comma-separated)
        - document_0_publication_date (str): Publication date of the first document (YYYY-MM-DD)
        - document_0_abstract (str): Abstract of the first document
        - document_0_doi (str): DOI of the first document
        - document_0_journal (str): Journal name for the first document
        - document_0_year (int): Publication year of the first document
        - document_1_title (str): Title of the second document
        - document_1_authors (str): Authors of the second document (comma-separated)
        - document_1_publication_date (str): Publication date of the second document (YYYY-MM-DD)
        - document_1_abstract (str): Abstract of the second document
        - document_1_doi (str): DOI of the second document
        - document_1_journal (str): Journal name for the second document
        - document_1_year (int): Publication year of the second document
        - total_count (int): Total number of documents returned
        - metadata_query_timestamp (str): ISO format timestamp when query was made
        - metadata_api_version (str): Version of the API used
        - metadata_source_database (str): Name and version of the source database
        - journal_name (str): The name of the journal queried
    """
    return {
        "document_0_title": "Discovery of Novel Anticancer Agents Targeting EGFR",
        "document_0_authors": "Smith J, Johnson A, Lee M",
        "document_0_publication_date": "2023-05-15",
        "document_0_abstract": "This study reports the identification and characterization of new small molecule inhibitors targeting the epidermal growth factor receptor (EGFR) with potent anticancer activity in vitro and in vivo.",
        "document_0_doi": "10.1021/jm400123x",
        "document_0_journal": "Journal of Medicinal Chemistry",
        "document_0_year": 2023,
        "document_1_title": "Structure-Based Drug Design of Dual BRAF/MEK Inhibitors",
        "document_1_authors": "Brown K, Davis R, Wilson T",
        "document_1_publication_date": "2023-04-22",
        "document_1_abstract": "We describe the rational design of dual inhibitors targeting BRAF and MEK kinases in the MAPK signaling pathway, showing enhanced efficacy in melanoma models.",
        "document_1_doi": "10.1021/acs.jmedchem.3c00456",
        "document_1_journal": "Journal of Medicinal Chemistry",
        "document_1_year": 2023,
        "total_count": 2,
        "metadata_query_timestamp": datetime.now().isoformat(),
        "metadata_api_version": "1.0",
        "metadata_source_database": "ChEMBL-32",
        "journal_name": "Journal of Medicinal Chemistry"
    }


def chembl_server_example_document(journal: str) -> Dict[str, Any]:
    """
    Get document data for the specified journal.

    Args:
        journal (str): Journal name

    Returns:
        Dict containing:
        - documents (List[Dict]): List of document entries with metadata such as title, authors,
          publication date, abstract, DOI, and other relevant scientific paper details.
        - journal_name (str): The name of the journal for which documents were retrieved.
        - total_count (int): Total number of documents returned.
        - metadata (Dict): Additional information about the retrieval process including
          query timestamp, API version, and source database identifier.
    """
    if not journal or not isinstance(journal, str):
        raise ValueError("Journal name must be a non-empty string.")

    api_data = call_external_api("chembl-server-example_document")

    # Construct documents list from indexed fields
    documents = [
        {
            "title": api_data["document_0_title"],
            "authors": api_data["document_0_authors"],
            "publication_date": api_data["document_0_publication_date"],
            "abstract": api_data["document_0_abstract"],
            "doi": api_data["document_0_doi"],
            "journal": api_data["document_0_journal"],
            "year": api_data["document_0_year"]
        },
        {
            "title": api_data["document_1_title"],
            "authors": api_data["document_1_authors"],
            "publication_date": api_data["document_1_publication_date"],
            "abstract": api_data["document_1_abstract"],
            "doi": api_data["document_1_doi"],
            "journal": api_data["document_1_journal"],
            "year": api_data["document_1_year"]
        }
    ]

    # Construct final result matching output schema
    result = {
        "documents": documents,
        "journal_name": api_data["journal_name"],
        "total_count": api_data["total_count"],
        "metadata": {
            "query_timestamp": api_data["metadata_query_timestamp"],
            "api_version": api_data["metadata_api_version"],
            "source_database": api_data["metadata_source_database"]
        }
    }

    return result