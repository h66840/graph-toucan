from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for molecule form information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - molecule_form_0_structure (str): Chemical structure of the first molecule form (e.g., SMILES)
        - molecule_form_0_molecular_weight (float): Molecular weight of the first molecule form
        - molecule_form_0_physical_state (str): Physical state of the first molecule form (e.g., solid, liquid)
        - molecule_form_0_metadata_source (str): Source database of the first molecule form
        - molecule_form_0_metadata_version (str): Database version for the first molecule form
        - molecule_form_1_structure (str): Chemical structure of the second molecule form
        - molecule_form_1_molecular_weight (float): Molecular weight of the second molecule form
        - molecule_form_1_physical_state (str): Physical state of the second molecule form
        - molecule_form_1_metadata_source (str): Source database of the second molecule form
        - molecule_form_1_metadata_version (str): Database version for the second molecule form
        - total_count (int): Total number of molecule forms found
        - form_type (str): General classification of the form (e.g., solid, liquid)
        - has_results (bool): Whether any results were found
        - metadata_query_timestamp (str): Timestamp of the query execution
        - metadata_processing_status (str): Status of the processing (e.g., success)
        - metadata_database_version (str): Version of the source database
    """
    return {
        "molecule_form_0_structure": "CCO",
        "molecule_form_0_molecular_weight": 46.07,
        "molecule_form_0_physical_state": "liquid",
        "molecule_form_0_metadata_source": "ChEMBL",
        "molecule_form_0_metadata_version": "32",
        "molecule_form_1_structure": "CC(=O)O",
        "molecule_form_1_molecular_weight": 60.05,
        "molecule_form_1_physical_state": "solid",
        "molecule_form_1_metadata_source": "ChEMBL",
        "molecule_form_1_metadata_version": "32",
        "total_count": 2,
        "form_type": "solid",
        "has_results": True,
        "metadata_query_timestamp": "2023-10-05T12:34:56Z",
        "metadata_processing_status": "success",
        "metadata_database_version": "32"
    }

def chembl_server_example_molecule_form(form_description: str) -> Dict[str, Any]:
    """
    Get molecule form data for the specified description.
    
    Args:
        form_description (str): Form description (e.g., 'crystalline solid', 'aqueous solution')
        
    Returns:
        Dict containing:
        - molecule_forms (List[Dict]): List of dictionaries with detailed information about each molecule form
        - total_count (int): Total number of molecule forms returned
        - form_type (str): General classification or category of the form
        - has_results (bool): Indicates whether any molecule forms were found
        - metadata (Dict): Additional contextual information about the query execution
    
    Raises:
        ValueError: If form_description is empty or not a string
    """
    if not form_description:
        raise ValueError("form_description is required")
    if not isinstance(form_description, str):
        raise ValueError("form_description must be a string")

    # Call external API to get flat data
    api_data = call_external_api("chembl-server-example_molecule_form")

    # Construct molecule forms list from indexed fields
    molecule_forms = [
        {
            "structure": api_data["molecule_form_0_structure"],
            "molecular_weight": api_data["molecule_form_0_molecular_weight"],
            "physical_state": api_data["molecule_form_0_physical_state"],
            "metadata": {
                "source": api_data["molecule_form_0_metadata_source"],
                "version": api_data["molecule_form_0_metadata_version"]
            }
        },
        {
            "structure": api_data["molecule_form_1_structure"],
            "molecular_weight": api_data["molecule_form_1_molecular_weight"],
            "physical_state": api_data["molecule_form_1_physical_state"],
            "metadata": {
                "source": api_data["molecule_form_1_metadata_source"],
                "version": api_data["molecule_form_1_metadata_version"]
            }
        }
    ]

    # Construct final result with proper nested structure
    result = {
        "molecule_forms": molecule_forms,
        "total_count": api_data["total_count"],
        "form_type": api_data["form_type"],
        "has_results": api_data["has_results"],
        "metadata": {
            "query_timestamp": api_data["metadata_query_timestamp"],
            "processing_status": api_data["metadata_processing_status"],
            "database_version": api_data["metadata_database_version"]
        }
    }

    return result