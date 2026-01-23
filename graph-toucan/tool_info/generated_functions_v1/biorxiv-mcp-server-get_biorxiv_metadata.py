from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for bioRxiv metadata.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): The title of the preprint article from bioRxiv
        - author_0_name (str): Name of the first author
        - author_0_affiliation (str): Affiliation of the first author
        - author_0_orcid (str): ORCID of the first author if available
        - author_1_name (str): Name of the second author
        - author_1_affiliation (str): Affiliation of the second author
        - author_1_orcid (str): ORCID of the second author if available
        - doi (str): Digital Object Identifier for the preprint
        - published_date (str): Publication date of the preprint in ISO format (YYYY-MM-DD)
        - abstract (str): Abstract or summary of the preprint content
        - version (str): Version identifier of the preprint (e.g., '1', '2')
        - license (str): License under which the preprint is shared
        - pdf_url (str): Direct URL to the PDF version of the preprint
        - html_url (str): URL to the HTML version of the preprint on bioRxiv
        - keyword_0 (str): First keyword associated with the preprint
        - keyword_1 (str): Second keyword associated with the preprint
        - journal (str): Target journal or current publication status (e.g., 'Posted' or 'Under review')
        - category (str): Primary research category or subject area
        - status (str): Current status of the preprint (e.g., 'posted', 'revised', 'withdrawn')
        - related_doi_0 (str): First related DOI (e.g., previous version)
        - related_doi_1 (str): Second related DOI (e.g., later publication)
        - date_submitted (str): Date when the preprint was submitted (ISO format)
        - date_updated (str): Date when the preprint was last updated (ISO format)
        - citation_count (int): Number of citations for the preprint
        - source_identifier (str): Source-specific identifier for the preprint
    """
    return {
        "title": "A Novel Approach to Neural Circuit Mapping Using Optogenetics",
        "author_0_name": "Jane Smith",
        "author_0_affiliation": "Department of Neuroscience, Stanford University",
        "author_0_orcid": "0000-0002-1825-0097",
        "author_1_name": "John Doe",
        "author_1_affiliation": "School of Biology, Massachusetts Institute of Technology",
        "author_1_orcid": "0000-0003-1234-5678",
        "doi": "10.1101/2023.01.01.498271",
        "published_date": "2023-01-01",
        "abstract": "This study presents a new method for mapping neural circuits using optogenetic stimulation combined with high-resolution imaging. We demonstrate its application in the mouse visual cortex.",
        "version": "1",
        "license": "CC-BY-4.0",
        "pdf_url": "https://www.biorxiv.org/content/10.1101/2023.01.01.498271v1.full.pdf",
        "html_url": "https://www.biorxiv.org/content/10.1101/2023.01.01.498271v1",
        "keyword_0": "neuroscience",
        "keyword_1": "optogenetics",
        "journal": "Posted",
        "category": "neuroscience",
        "status": "posted",
        "related_doi_0": "10.1101/2022.12.01.497654",
        "related_doi_1": "10.1038/s41586-023-06000-w",
        "date_submitted": "2022-12-15",
        "date_updated": "2023-01-01",
        "citation_count": 42,
        "source_identifier": "biorxiv-2023-01-01-498271"
    }

def biorxiv_mcp_server_get_biorxiv_metadata(doi: str) -> Dict[str, Any]:
    """
    Fetch metadata for a preprint article from bioRxiv using its DOI.

    Args:
        doi (str): Digital Object Identifier for the preprint (required).

    Returns:
        Dict containing the following keys:
        - title (str): The title of the preprint article from bioRxiv
        - authors (List[Dict]): List of author dictionaries, each containing 'name', 'affiliation', and 'orcid' if available
        - doi (str): Digital Object Identifier for the preprint
        - published_date (str): Publication date of the preprint in ISO format (YYYY-MM-DD)
        - abstract (str): Abstract or summary of the preprint content
        - version (str): Version identifier of the preprint (e.g., '1', '2')
        - license (str): License under which the preprint is shared
        - pdf_url (str): Direct URL to the PDF version of the preprint
        - html_url (str): URL to the HTML version of the preprint on bioRxiv
        - keywords (List[str]): Keywords or tags associated with the preprint
        - journal (str): Target journal or current publication status (e.g., 'Posted' or 'Under review')
        - category (str): Primary research category or subject area (e.g., 'bioinformatics', 'neuroscience')
        - status (str): Current status of the preprint (e.g., 'posted', 'revised', 'withdrawn')
        - related_dois (List[str]): List of related DOIs, such as previous versions or later publications
        - metadata (Dict): Additional metadata including fields like 'date_submitted', 'date_updated', 'citation_count', and source-specific identifiers

    Raises:
        ValueError: If the DOI is empty or invalid.
    """
    if not doi or not isinstance(doi, str) or not doi.strip():
        raise ValueError("DOI must be a non-empty string.")

    # Call external API to get flattened data
    api_data = call_external_api("biorxiv-mcp-server-get_biorxiv_metadata")

    # Construct authors list
    authors = [
        {
            "name": api_data["author_0_name"],
            "affiliation": api_data["author_0_affiliation"],
            "orcid": api_data["author_0_orcid"]
        },
        {
            "name": api_data["author_1_name"],
            "affiliation": api_data["author_1_affiliation"],
            "orcid": api_data["author_1_orcid"]
        }
    ]

    # Construct keywords list
    keywords = [api_data["keyword_0"], api_data["keyword_1"]]

    # Construct related DOIs list
    related_dois = [api_data["related_doi_0"], api_data["related_doi_1"]]

    # Construct metadata dictionary
    metadata = {
        "date_submitted": api_data["date_submitted"],
        "date_updated": api_data["date_updated"],
        "citation_count": api_data["citation_count"],
        "source_identifier": api_data["source_identifier"]
    }

    # Build final result matching output schema
    result = {
        "title": api_data["title"],
        "authors": authors,
        "doi": api_data["doi"],
        "published_date": api_data["published_date"],
        "abstract": api_data["abstract"],
        "version": api_data["version"],
        "license": api_data["license"],
        "pdf_url": api_data["pdf_url"],
        "html_url": api_data["html_url"],
        "keywords": keywords,
        "journal": api_data["journal"],
        "category": api_data["category"],
        "status": api_data["status"],
        "related_dois": related_dois,
        "metadata": metadata
    }

    return result