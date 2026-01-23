from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BioMart attribute listing.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - attribute_0_name (str): Internal name of the first attribute
        - attribute_0_display_name (str): Display name of the first attribute
        - attribute_0_description (str): Description of the first attribute
        - attribute_1_name (str): Internal name of the second attribute
        - attribute_1_display_name (str): Display name of the second attribute
        - attribute_1_description (str): Description of the second attribute
    """
    return {
        "attribute_0_name": "ensembl_gene_id",
        "attribute_0_display_name": "Ensembl Gene ID",
        "attribute_0_description": "Stable Ensembl Gene Identifier",
        "attribute_1_name": "external_gene_name",
        "attribute_1_display_name": "Gene Name",
        "attribute_1_description": "Gene symbol approved by HGNC"
    }

def biomart_mcp_list_all_attributes(mart: str, dataset: str) -> List[Dict[str, str]]:
    """
    Lists all available attributes for a given dataset with some filtering.
    
    This function returns a filtered list of all attributes available for the specified
    dataset. Some less commonly used attributes (homologs, microarray probes) are
    filtered out to reduce the response size.
    
    CAUTION: This function can return a large number of attributes and may be unstable
    for certain datasets. Consider using list_common_attributes first.
    
    Args:
        mart (str): The mart identifier (e.g., "ENSEMBL_MART_ENSEMBL")
        dataset (str): The dataset identifier (e.g., "hsapiens_gene_ensembl")
    
    Returns:
        List[Dict]: List of attribute objects, each with 'name', 'display_name', and 'description' fields.
    
    Example:
        biomart_mcp_list_all_attributes("ENSEMBL_MART_ENSEMBL", "hsapiens_gene_ensembl")
    """
    # Input validation
    if not mart or not isinstance(mart, str):
        raise ValueError("Parameter 'mart' must be a non-empty string.")
    if not dataset or not isinstance(dataset, str):
        raise ValueError("Parameter 'dataset' must be a non-empty string.")
    
    # Call external API to get flat data
    api_data = call_external_api("biomart-mcp-list_all_attributes")
    
    # Construct the result list from flattened API response
    attributes = [
        {
            "name": api_data["attribute_0_name"],
            "display_name": api_data["attribute_0_display_name"],
            "description": api_data["attribute_0_description"]
        },
        {
            "name": api_data["attribute_1_name"],
            "display_name": api_data["attribute_1_display_name"],
            "description": api_data["attribute_1_description"]
        }
    ]
    
    return attributes