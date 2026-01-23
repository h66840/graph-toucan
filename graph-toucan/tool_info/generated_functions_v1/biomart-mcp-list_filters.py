from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching filter data from external Biomart API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - filter_0_name (str): Name of the first available filter
        - filter_0_type (str): Type of the first filter
        - filter_0_description (str): Description of the first filter
        - filter_1_name (str): Name of the second available filter
        - filter_1_type (str): Type of the second filter
        - filter_1_description (str): Description of the second filter
    """
    return {
        "filter_0_name": "chromosome_name",
        "filter_0_type": "string",
        "filter_0_description": "Chromosome/scaffold name",
        "filter_1_name": "start",
        "filter_1_type": "int",
        "filter_1_description": "Gene start (bp)"
    }

def biomart_mcp_list_filters(mart: str, dataset: str) -> List[Dict[str, str]]:
    """
    Lists all available filters for a given dataset in a Biomart mart.
    
    Filters are used to narrow down the results of a Biomart query.
    This function returns all filters that can be applied to the specified dataset.
    
    Args:
        mart (str): The mart identifier (e.g., "ENSEMBL_MART_ENSEMBL")
        dataset (str): The dataset identifier (e.g., "hsapiens_gene_ensembl")
    
    Returns:
        List[Dict[str, str]]: List of filter objects, each with 'name', 'type', and 'description' fields.
    
    Example:
        biomart_mcp_list_filters("ENSEMBL_MART_ENSEMBL", "hsapiens_gene_ensembl")
        >>> [
            {"name": "chromosome_name", "type": "string", "description": "Chromosome/scaffold name"},
            {"name": "start", "type": "int", "description": "Gene start (bp)"}
        ]
    """
    # Input validation
    if not mart or not isinstance(mart, str):
        raise ValueError("Parameter 'mart' must be a non-empty string.")
    if not dataset or not isinstance(dataset, str):
        raise ValueError("Parameter 'dataset' must be a non-empty string.")
    
    # Fetch data from simulated external API
    api_data = call_external_api("biomart-mcp-list_filters")
    
    # Construct the result list from flattened API response
    filters = [
        {
            "name": api_data["filter_0_name"],
            "type": api_data["filter_0_type"],
            "description": api_data["filter_0_description"]
        },
        {
            "name": api_data["filter_1_name"],
            "type": api_data["filter_1_type"],
            "description": api_data["filter_1_description"]
        }
    ]
    
    return filters