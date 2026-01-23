from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BioMart common attributes.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - attribute_0_name (str): Internal name of the first common attribute
        - attribute_0_display_name (str): Display name of the first common attribute
        - attribute_0_description (str): Description of the first common attribute
        - attribute_1_name (str): Internal name of the second common attribute
        - attribute_1_display_name (str): Display name of the second common attribute
        - attribute_1_description (str): Description of the second common attribute
    """
    return {
        "attribute_0_name": "ensembl_gene_id",
        "attribute_0_display_name": "Gene stable ID",
        "attribute_0_description": "Ensembl stable ID for the gene",
        "attribute_1_name": "external_gene_name",
        "attribute_1_display_name": "Gene name",
        "attribute_1_description": "The gene name"
    }

def biomart_mcp_list_common_attributes(mart: str, dataset: str) -> List[Dict[str, str]]:
    """
    Lists commonly used attributes available for a given dataset.

    This function returns only the most frequently used attributes (defined in COMMON_ATTRIBUTES)
    to avoid overwhelming the model with too many options. For a complete list,
    use list_all_attributes.

    Args:
        mart (str): The mart identifier (e.g., "ENSEMBL_MART_ENSEMBL")
        dataset (str): The dataset identifier (e.g., "hsapiens_gene_ensembl")

    Returns:
        List[Dict[str, str]]: List of attribute objects, each with 'name', 'display_name', and 'description' fields.

    Example:
        biomart_mcp_list_common_attributes("ENSEMBL_MART_ENSEMBL", "hsapiens_gene_ensembl")
        >>> [
            {
                "name": "ensembl_gene_id",
                "display_name": "Gene stable ID",
                "description": "Ensembl stable ID for the gene"
            },
            {
                "name": "external_gene_name",
                "display_name": "Gene name",
                "description": "The gene name"
            }
        ]
    """
    if not mart or not isinstance(mart, str):
        raise ValueError("Parameter 'mart' must be a non-empty string.")
    if not dataset or not isinstance(dataset, str):
        raise ValueError("Parameter 'dataset' must be a non-empty string.")

    api_data = call_external_api("biomart-mcp-list_common_attributes")

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