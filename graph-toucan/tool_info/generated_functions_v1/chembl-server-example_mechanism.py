from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL mechanism of action.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_target_organism (str): Organism of the target for the first result
        - result_0_target_type (str): Type of target for the first result
        - result_0_target_name (str): Name of the target for the first result
        - result_0_molecule_chembl_id (str): ChEMBL ID of the molecule for the first result
        - result_0_molecule_name (str): Name of the molecule for the first result
        - result_0_action_type (str): Pharmacological action type for the first result
        - result_0_mechanism_of_action (str): Detailed mechanism of action for the first result
        - result_1_target_organism (str): Organism of the target for the second result
        - result_1_target_type (str): Type of target for the second result
        - result_1_target_name (str): Name of the target for the second result
        - result_1_molecule_chembl_id (str): ChEMBL ID of the molecule for the second result
        - result_1_molecule_name (str): Name of the molecule for the second result
        - result_1_action_type (str): Pharmacological action type for the second result
        - result_1_mechanism_of_action (str): Detailed mechanism of action for the second result
        - count (int): Total number of mechanism entries returned
        - page (int): Current page number
        - has_more (bool): Indicates if more results are available
        - metadata_response_time (float): Time taken to process the query in seconds
        - metadata_database_version (str): Version of the ChEMBL database used
        - metadata_warnings (str): Any warnings related to the query (empty if none)
    """
    return {
        "result_0_target_organism": "Homo sapiens",
        "result_0_target_type": "PROTEIN",
        "result_0_target_name": "Dopamine receptor D2",
        "result_0_molecule_chembl_id": "CHEMBL12345",
        "result_0_molecule_name": "Risperidone",
        "result_0_action_type": "Antagonist",
        "result_0_mechanism_of_action": "Competitive antagonist of dopamine D2 receptors",
        "result_1_target_organism": "Homo sapiens",
        "result_1_target_type": "SEROTONIN RECEPTOR",
        "result_1_target_name": "5-HT2A receptor",
        "result_1_molecule_chembl_id": "CHEMBL67890",
        "result_1_molecule_name": "Olanzapine",
        "result_1_action_type": "Inverse agonist",
        "result_1_mechanism_of_action": "Inverse agonist at serotonin 5-HT2A receptors",
        "count": 2,
        "page": 1,
        "has_more": False,
        "metadata_response_time": 0.15,
        "metadata_database_version": "32",
        "metadata_warnings": ""
    }

def chembl_server_example_mechanism(mechanism_of_action: str) -> Dict[str, Any]:
    """
    Get data for the specified mechanism of action from ChEMBL database.

    Args:
        mechanism_of_action (str): The mechanism of action to query (e.g., 'antagonist', 'inhibitor')

    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with detailed mechanism data
        - count (int): Total number of mechanism entries returned
        - page (int): Current page number
        - has_more (bool): Indicates if more results are available
        - metadata (Dict): Additional information about the query execution

    Raises:
        ValueError: If mechanism_of_action is empty or not a string
    """
    if not mechanism_of_action or not isinstance(mechanism_of_action, str):
        raise ValueError("mechanism_of_action must be a non-empty string")

    # Call external API to get flattened data
    api_data = call_external_api("chembl-server-example_mechanism")

    # Construct results list from indexed fields
    results = [
        {
            "target": {
                "organism": api_data["result_0_target_organism"],
                "type": api_data["result_0_target_type"],
                "name": api_data["result_0_target_name"]
            },
            "molecule": {
                "chembl_id": api_data["result_0_molecule_chembl_id"],
                "name": api_data["result_0_molecule_name"]
            },
            "pharmacology": {
                "action_type": api_data["result_0_action_type"],
                "mechanism_of_action": api_data["result_0_mechanism_of_action"]
            }
        },
        {
            "target": {
                "organism": api_data["result_1_target_organism"],
                "type": api_data["result_1_target_type"],
                "name": api_data["result_1_target_name"]
            },
            "molecule": {
                "chembl_id": api_data["result_1_molecule_chembl_id"],
                "name": api_data["result_1_molecule_name"]
            },
            "pharmacology": {
                "action_type": api_data["result_1_action_type"],
                "mechanism_of_action": api_data["result_1_mechanism_of_action"]
            }
        }
    ]

    # Construct metadata
    metadata = {
        "response_time": api_data["metadata_response_time"],
        "database_version": api_data["metadata_database_version"]
    }

    # Add warnings to metadata if present
    if api_data["metadata_warnings"]:
        metadata["warnings"] = api_data["metadata_warnings"]

    # Build final response
    response = {
        "results": results,
        "count": api_data["count"],
        "page": api_data["page"],
        "has_more": api_data["has_more"],
        "metadata": metadata
    }

    return response