from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cell line data from external ChEMBL server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_cell_line_id (str): First cell line ID
        - result_0_name (str): First cell line name
        - result_0_species (str): First cell line species
        - result_0_tissue_origin (str): First cell line tissue origin
        - result_0_disease_association (str): First cell line disease association
        - result_0_biological_annotations (str): First cell line biological annotations
        - result_1_cell_line_id (str): Second cell line ID
        - result_1_name (str): Second cell line name
        - result_1_species (str): Second cell line species
        - result_1_tissue_origin (str): Second cell line tissue origin
        - result_1_disease_association (str): Second cell line disease association
        - result_1_biological_annotations (str): Second cell line biological annotations
        - count (int): Total number of results returned
        - page_info_page (int): Current page number
        - page_info_per_page (int): Number of results per page
        - page_info_has_next (bool): Whether next page exists
        - metadata_data_source_version (str): ChEMBL database version
        - metadata_response_timestamp (str): ISO format timestamp of response
        - metadata_warnings (str): Any warnings from the query execution
        - metadata_notes (str): Additional notes about the query
    """
    return {
        "result_0_cell_line_id": "CL000001",
        "result_0_name": "A549",
        "result_0_species": "Homo sapiens",
        "result_0_tissue_origin": "lung",
        "result_0_disease_association": "lung adenocarcinoma",
        "result_0_biological_annotations": "epithelial, carcinoma, KRAS mutation",
        "result_1_cell_line_id": "CL000002",
        "result_1_name": "MCF7",
        "result_1_species": "Homo sapiens",
        "result_1_tissue_origin": "breast",
        "result_1_disease_association": "breast adenocarcinoma",
        "result_1_biological_annotations": "epithelial, hormone-sensitive, ER+",
        "count": 2,
        "page_info_page": 1,
        "page_info_per_page": 20,
        "page_info_has_next": False,
        "metadata_data_source_version": "ChEMBL 32",
        "metadata_response_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_warnings": "",
        "metadata_notes": "Results filtered by cell line name match"
    }

def chembl_server_example_cell_line(cell_line_name: str) -> Dict[str, Any]:
    """
    Get cell line data for the specified name.
    
    Args:
        cell_line_name (str): The name of the cell line to search for (e.g., 'A549', 'MCF7')
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with detailed cell line information
        - count (int): Total number of cell lines returned
        - page_info (Dict): Pagination metadata including page, per_page, and has_next
        - metadata (Dict): Additional contextual information about the query execution
        
    Raises:
        ValueError: If cell_line_name is empty or not a string
    """
    if not cell_line_name:
        raise ValueError("cell_line_name is required")
    if not isinstance(cell_line_name, str):
        raise ValueError("cell_line_name must be a string")
    
    # Call external API to get flattened data
    api_data = call_external_api("chembl-server-example_cell_line")
    
    # Construct results list from indexed fields
    results = [
        {
            "cell_line_id": api_data["result_0_cell_line_id"],
            "name": api_data["result_0_name"],
            "species": api_data["result_0_species"],
            "tissue_origin": api_data["result_0_tissue_origin"],
            "disease_association": api_data["result_0_disease_association"],
            "biological_annotations": api_data["result_0_biological_annotations"]
        },
        {
            "cell_line_id": api_data["result_1_cell_line_id"],
            "name": api_data["result_1_name"],
            "species": api_data["result_1_species"],
            "tissue_origin": api_data["result_1_tissue_origin"],
            "disease_association": api_data["result_1_disease_association"],
            "biological_annotations": api_data["result_1_biological_annotations"]
        }
    ]
    
    # Construct page_info dictionary
    page_info = {
        "page": api_data["page_info_page"],
        "per_page": api_data["page_info_per_page"],
        "has_next": api_data["page_info_has_next"]
    }
    
    # Construct metadata dictionary
    metadata = {
        "data_source_version": api_data["metadata_data_source_version"],
        "response_timestamp": api_data["metadata_response_timestamp"],
        "warnings": api_data["metadata_warnings"] if api_data["metadata_warnings"] else None,
        "notes": api_data["metadata_notes"]
    }
    
    # Return final structured response
    return {
        "results": results,
        "count": api_data["count"],
        "page_info": page_info,
        "metadata": metadata
    }