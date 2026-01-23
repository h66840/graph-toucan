from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for biomart-mcp-list_datasets.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - dataset_0_name (str): Internal identifier of the first dataset
        - dataset_0_display_name (str): Human-readable label of the first dataset
        - dataset_1_name (str): Internal identifier of the second dataset
        - dataset_1_display_name (str): Human-readable label of the second dataset
    """
    return {
        "dataset_0_name": "hsapiens_gene_ensembl",
        "dataset_0_display_name": "Human genes",
        "dataset_1_name": "mmusculus_gene_ensembl",
        "dataset_1_display_name": "Mouse genes"
    }

def biomart_mcp_list_datasets(mart: str) -> List[Dict[str, str]]:
    """
    Lists all available biomart datasets for a given mart.

    Each mart contains multiple datasets. This function returns all datasets
    available in the specified mart as a list of dictionaries.

    Args:
        mart (str): The mart identifier to list datasets from.
            Valid values include: ENSEMBL_MART_ENSEMBL, ENSEMBL_MART_MOUSE,
            ENSEMBL_MART_ONTOLOGY, ENSEMBL_MART_GENOMIC, ENSEMBL_MART_SNP,
            ENSEMBL_MART_FUNCGEN

    Returns:
        List[Dict[str, str]]: List of dataset entries, each with 'name' (internal identifier)
                              and 'display_name' (human-readable label).

    Raises:
        ValueError: If mart is not one of the valid mart identifiers.
    """
    valid_marts = [
        "ENSEMBL_MART_ENSEMBL",
        "ENSEMBL_MART_MOUSE",
        "ENSEMBL_MART_ONTOLOGY",
        "ENSEMBL_MART_GENOMIC",
        "ENSEMBL_MART_SNP",
        "ENSEMBL_MART_FUNCGEN"
    ]
    
    if mart not in valid_marts:
        raise ValueError(f"Invalid mart: {mart}. Must be one of {valid_marts}")
    
    api_data = call_external_api("biomart-mcp-list_datasets")
    
    datasets = [
        {
            "name": api_data["dataset_0_name"],
            "display_name": api_data["dataset_0_display_name"]
        },
        {
            "name": api_data["dataset_1_name"],
            "display_name": api_data["dataset_1_display_name"]
        }
    ]
    
    return datasets