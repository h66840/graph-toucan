from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching organism data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - organism_0_scientific_name (str): Scientific name of the first organism
        - organism_0_common_name (str): Common name of the first organism
        - organism_0_tax_id (int): Taxonomy ID of the first organism
        - organism_0_rank (str): Taxonomic rank of the first organism
        - organism_0_lineage (str): Lineage path of the first organism
        - organism_1_scientific_name (str): Scientific name of the second organism
        - organism_1_common_name (str): Common name of the second organism
        - organism_1_tax_id (int): Taxonomy ID of the second organism
        - organism_1_rank (str): Taxonomic rank of the second organism
        - organism_1_lineage (str): Lineage path of the second organism
        - count (int): Total number of organisms returned
        - success (bool): Whether the request was successful
        - error_message (str): Error message if any, otherwise null
    """
    return {
        "organism_0_scientific_name": "Homo sapiens",
        "organism_0_common_name": "human",
        "organism_0_tax_id": 9606,
        "organism_0_rank": "species",
        "organism_0_lineage": "Eukaryota; Metazoa; Chordata; Mammalia; Primates; Hominidae; Homo",
        "organism_1_scientific_name": "Mus musculus",
        "organism_1_common_name": "house mouse",
        "organism_1_tax_id": 10090,
        "organism_1_rank": "species",
        "organism_1_lineage": "Eukaryota; Metazoa; Chordata; Mammalia; Rodentia; Muridae; Mus",
        "count": 2,
        "success": True,
        "error_message": None
    }

def chembl_server_example_organism(tax_id: int) -> Dict[str, Any]:
    """
    Get organism data for the specified taxonomy ID.
    
    Args:
        tax_id (int): Taxonomy ID to query organism data for
        
    Returns:
        Dict containing:
        - organisms (List[Dict]): List of organism records with detailed taxonomic data
        - count (int): Total number of organisms returned
        - success (bool): Whether the request was processed successfully
        - error_message (Optional[str]): Error message if request failed, otherwise None
        
    Example:
        {
            "organisms": [
                {
                    "scientific_name": "Homo sapiens",
                    "common_name": "human",
                    "tax_id": 9606,
                    "rank": "species",
                    "lineage": "Eukaryota; Metazoa; Chordata; Mammalia; Primates; Hominidae; Homo"
                },
                {
                    "scientific_name": "Mus musculus",
                    "common_name": "house mouse",
                    "tax_id": 10090,
                    "rank": "species",
                    "lineage": "Eukaryota; Metazoa; Chordata; Mammalia; Rodentia; Muridae; Mus"
                }
            ],
            "count": 2,
            "success": True,
            "error_message": None
        }
    """
    # Input validation
    if not isinstance(tax_id, int) or tax_id <= 0:
        return {
            "organisms": [],
            "count": 0,
            "success": False,
            "error_message": "Invalid tax_id: must be a positive integer"
        }
    
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("chembl-server-example_organism")
        
        # Construct organisms list from flattened API response
        organisms = [
            {
                "scientific_name": api_data["organism_0_scientific_name"],
                "common_name": api_data["organism_0_common_name"],
                "tax_id": api_data["organism_0_tax_id"],
                "rank": api_data["organism_0_rank"],
                "lineage": api_data["organism_0_lineage"]
            },
            {
                "scientific_name": api_data["organism_1_scientific_name"],
                "common_name": api_data["organism_1_common_name"],
                "tax_id": api_data["organism_1_tax_id"],
                "rank": api_data["organism_1_rank"],
                "lineage": api_data["organism_1_lineage"]
            }
        ]
        
        # Return structured response matching output schema
        return {
            "organisms": organisms,
            "count": api_data["count"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
    except Exception as e:
        return {
            "organisms": [],
            "count": 0,
            "success": False,
            "error_message": f"Failed to retrieve organism data: {str(e)}"
        }