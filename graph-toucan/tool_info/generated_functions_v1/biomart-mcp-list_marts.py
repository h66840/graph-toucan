from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Biomart marts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - mart_0_name (str): Internal name of the first mart
        - mart_0_display_name (str): Display name of the first mart
        - mart_0_description (str): Description of the first mart
        - mart_1_name (str): Internal name of the second mart
        - mart_1_display_name (str): Display name of the second mart
        - mart_1_description (str): Description of the second mart
    """
    return {
        "mart_0_name": "ENSEMBL_MART_ENSEMBL",
        "mart_0_display_name": "Ensembl Genes",
        "mart_0_description": "Gene annotation from Ensembl",
        "mart_1_name": "ENSEMBL_MART_MOUSE",
        "mart_1_display_name": "Mouse strains",
        "mart_1_description": "Strain-specific data for mouse"
    }

def biomart_mcp_list_marts() -> str:
    """
    Lists all available Biomart marts (databases) from Ensembl.

    Biomart organizes biological data in a hierarchy: MART -> DATASET -> ATTRIBUTES/FILTERS.
    This function returns all available marts as a CSV string.

    Returns:
        str: CSV-formatted table of all marts with their display names and descriptions.
             Contains headers 'name,display_name,description' followed by data rows.

    Example:
        >>> biomart_mcp_list_marts()
        'name,display_name,description\\nENSEMBL_MART_ENSEMBL,Ensembl Genes,Gene annotation from Ensembl\\nENSEMBL_MART_MOUSE,Mouse strains,Strain-specific data for mouse'
    """
    try:
        api_data = call_external_api("biomart-mcp-list_marts")
        
        # Build CSV string
        csv_lines = ["name,display_name,description"]
        
        # Add first mart
        line_0 = f"{api_data['mart_0_name']},{api_data['mart_0_display_name']},{api_data['mart_0_description']}"
        csv_lines.append(line_0)
        
        # Add second mart
        line_1 = f"{api_data['mart_1_name']},{api_data['mart_1_display_name']},{api_data['mart_1_description']}"
        csv_lines.append(line_1)
        
        return "\n".join(csv_lines)
    except Exception as e:
        raise RuntimeError(f"Failed to list Biomart marts: {str(e)}")