from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external PubChem API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - results_0_cid (int): CID of the first compound
        - results_0_formula (str): Molecular formula of the first compound
        - results_0_name (str): Name of the first compound
        - results_0_smiles (str): SMILES string of the first compound
        - results_0_molecular_weight (float): Molecular weight of the first compound
        - results_1_cid (int): CID of the second compound
        - results_1_formula (str): Molecular formula of the second compound
        - results_1_name (str): Name of the second compound
        - results_1_smiles (str): SMILES string of the second compound
        - results_1_molecular_weight (float): Molecular weight of the second compound
        - total_count (int): Total number of matching compounds
        - query_time_ms (int): Time in milliseconds for query processing
        - page (int): Current page of results
        - has_more (bool): Whether more results are available
        - search_metadata_formula (str): Formula used in search
        - search_metadata_name (str): Name used in search
        - search_metadata_smiles (str): SMILES used in search
        - search_metadata_database_version (str): Version of PubChem database
        - search_metadata_timestamp (str): Timestamp of the query
    """
    return {
        "results_0_cid": 2244,
        "results_0_formula": "C9H8O4",
        "results_0_name": "Aspirin",
        "results_0_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "results_0_molecular_weight": 180.157,
        "results_1_cid": 1983,
        "results_1_formula": "C8H9NO2",
        "results_1_name": "Acetaminophen",
        "results_1_smiles": "CC(=O)NC1=CC=C(O)C=C1",
        "results_1_molecular_weight": 151.163,
        "total_count": 2,
        "query_time_ms": 45,
        "page": 1,
        "has_more": False,
        "search_metadata_formula": "C9H8O4",
        "search_metadata_name": "Aspirin",
        "search_metadata_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "search_metadata_database_version": "2023.10",
        "search_metadata_timestamp": "2023-11-15T10:30:00Z"
    }

def pubchem_mcp_server_search_pubchem_advanced(
    cid: Optional[str] = None,
    formula: Optional[str] = None,
    max_results: Optional[int] = None,
    name: Optional[str] = None,
    smiles: Optional[str] = None
) -> Dict[str, Any]:
    """
    Searches PubChem database using advanced criteria such as CID, molecular formula, compound name, or SMILES.
    
    Args:
        cid (Optional[str]): Compound Identifier (CID) to search for.
        formula (Optional[str]): Molecular formula to match (e.g., "C9H8O4").
        max_results (Optional[int]): Maximum number of results to return. Defaults to all available.
        name (Optional[str]): Compound name or partial name to search.
        smiles (Optional[str]): SMILES string representing the molecular structure.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of compound records with identifiers, formula, name, SMILES, and properties.
        - total_count (int): Total number of compounds matching the query.
        - query_time_ms (int): Time in milliseconds that PubChem took to process the query.
        - page (int): Current page of results (default is 1).
        - has_more (bool): Indicates if more results exist beyond current set.
        - search_metadata (Dict): Additional metadata about the search (filters used, DB version, timestamp).
    
    Example:
        >>> pubchem_mcp_server_search_pubchem_advanced(name="Aspirin", formula="C9H8O4")
        {
            "results": [
                {
                    "cid": 2244,
                    "formula": "C9H8O4",
                    "name": "Aspirin",
                    "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
                    "molecular_weight": 180.157
                },
                ...
            ],
            "total_count": 2,
            ...
        }
    """
    # Validate inputs
    if max_results is not None and max_results < 1:
        raise ValueError("max_results must be a positive integer")

    # Call simulated external API
    api_data = call_external_api("pubchem-mcp-server-search_pubchem_advanced")

    # Construct results list from flattened API response
    results = [
        {
            "cid": api_data["results_0_cid"],
            "formula": api_data["results_0_formula"],
            "name": api_data["results_0_name"],
            "smiles": api_data["results_0_smiles"],
            "molecular_weight": api_data["results_0_molecular_weight"]
        },
        {
            "cid": api_data["results_1_cid"],
            "formula": api_data["results_1_formula"],
            "name": api_data["results_1_name"],
            "smiles": api_data["results_1_smiles"],
            "molecular_weight": api_data["results_1_molecular_weight"]
        }
    ]

    # Apply max_results limit if specified
    if max_results is not None:
        results = results[:max_results]

    # Build final output structure
    output = {
        "results": results,
        "total_count": api_data["total_count"],
        "query_time_ms": api_data["query_time_ms"],
        "page": api_data["page"],
        "has_more": api_data["has_more"],
        "search_metadata": {
            "formula": api_data["search_metadata_formula"],
            "name": api_data["search_metadata_name"],
            "smiles": api_data["search_metadata_smiles"],
            "database_version": api_data["search_metadata_database_version"],
            "timestamp": api_data["search_metadata_timestamp"]
        }
    }

    return output