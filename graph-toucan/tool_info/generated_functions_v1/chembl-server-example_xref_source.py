from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cross-reference source data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_source_name (str): Source name of the first cross-reference entry
        - results_0_reference_id (str): Reference ID of the first entry
        - results_0_url (str): URL of the first entry
        - results_0_description (str): Description of the first entry
        - results_0_resource_type (str): Resource type of the first entry
        - results_1_source_name (str): Source name of the second cross-reference entry
        - results_1_reference_id (str): Reference ID of the second entry
        - results_1_url (str): URL of the second entry
        - results_1_description (str): Description of the second entry
        - results_1_resource_type (str): Resource type of the second entry
        - count (int): Total number of cross-reference entries returned
        - source_metadata_display_name (str): Display name of the source
        - source_metadata_primary_url (str): Primary URL of the source
        - source_metadata_availability (str): Availability status of the source
        - source_metadata_data_type (str): Type of data provided by the source
        - source_metadata_last_updated (str): Last updated timestamp of the source
    """
    return {
        "results_0_source_name": "PubChem",
        "results_0_reference_id": "123456",
        "results_0_url": "https://pubchem.ncbi.nlm.nih.gov/compound/123456",
        "results_0_description": "Public chemical database maintained by the National Institutes of Health",
        "results_0_resource_type": "compound",
        "results_1_source_name": "ChEBI",
        "results_1_reference_id": "CHEBI:50000",
        "results_1_url": "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:50000",
        "results_1_description": "Chemical Entities of Biological Interest database",
        "results_1_resource_type": "molecule",
        "count": 2,
        "source_metadata_display_name": "External Chemical Databases",
        "source_metadata_primary_url": "https://www.ebi.ac.uk/chembl",
        "source_metadata_availability": "public",
        "source_metadata_data_type": "chemical_reference",
        "source_metadata_last_updated": "2023-10-01"
    }

def chembl_server_example_xref_source(xref_name: str) -> Dict[str, Any]:
    """
    Get cross-reference source data for the specified name.
    
    Args:
        xref_name (str): Cross-reference source name (e.g., 'PubChem', 'ChEBI')
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with cross-reference source data entries
        - count (int): Total number of cross-reference entries returned
        - source_metadata (Dict): Metadata about the cross-reference source
        
    Each result dictionary includes:
        - source_name (str): Name of the source database
        - reference_id (str): Identifier within the source database
        - url (str): Direct URL to the resource
        - description (str): Brief description of the source
        - resource_type (str): Type of resource (e.g., compound, molecule)
        
    Source metadata includes:
        - display_name (str): Human-readable name of the source
        - primary_url (str): Main URL of the source
        - availability (str): Access level (e.g., public, restricted)
        - data_type (str): Category of data provided
        - last_updated (str): Date when the source was last updated
    """
    if not xref_name or not isinstance(xref_name, str):
        raise ValueError("xref_name must be a non-empty string")
        
    api_data = call_external_api("chembl-server-example_xref_source")
    
    results = [
        {
            "source_name": api_data["results_0_source_name"],
            "reference_id": api_data["results_0_reference_id"],
            "url": api_data["results_0_url"],
            "description": api_data["results_0_description"],
            "resource_type": api_data["results_0_resource_type"]
        },
        {
            "source_name": api_data["results_1_source_name"],
            "reference_id": api_data["results_1_reference_id"],
            "url": api_data["results_1_url"],
            "description": api_data["results_1_description"],
            "resource_type": api_data["results_1_resource_type"]
        }
    ]
    
    source_metadata = {
        "display_name": api_data["source_metadata_display_name"],
        "primary_url": api_data["source_metadata_primary_url"],
        "availability": api_data["source_metadata_availability"],
        "data_type": api_data["source_metadata_data_type"],
        "last_updated": api_data["source_metadata_last_updated"]
    }
    
    return {
        "results": results,
        "count": api_data["count"],
        "source_metadata": source_metadata
    }