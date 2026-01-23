from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching drug data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - drug_0_name (str): Name of the first drug
        - drug_0_target (str): Target protein or pathway of the first drug
        - drug_0_indications (str): Medical indications for the first drug
        - drug_0_molecular_weight (float): Molecular weight of the first drug
        - drug_0_chembl_id (str): ChEMBL identifier for the first drug
        - drug_1_name (str): Name of the second drug
        - drug_1_target (str): Target protein or pathway of the second drug
        - drug_1_indications (str): Medical indications for the second drug
        - drug_1_molecular_weight (float): Molecular weight of the second drug
        - drug_1_chembl_id (str): ChEMBL identifier for the second drug
        - total_count (int): Total number of drugs returned
        - metadata_drug_type (str): The requested drug type
        - metadata_timestamp (str): ISO format timestamp of data retrieval
    """
    return {
        "drug_0_name": "Aspirin",
        "drug_0_target": "Cyclooxygenase",
        "drug_0_indications": "Pain, inflammation, fever",
        "drug_0_molecular_weight": 180.157,
        "drug_0_chembl_id": "CHEMBL25",
        "drug_1_name": "Atorvastatin",
        "drug_1_target": "HMG-CoA reductase",
        "drug_1_indications": "Hypercholesterolemia",
        "drug_1_molecular_weight": 558.634,
        "drug_1_chembl_id": "CHEMBL882",
        "total_count": 2,
        "metadata_drug_type": "small molecule",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def chembl_server_example_drug(drug_type: str) -> Dict[str, Any]:
    """
    Get drug data for the specified type.

    Args:
        drug_type (str): The type of drug to retrieve (e.g., 'small molecule', 'biologic')

    Returns:
        Dict containing:
        - drugs (List[Dict]): List of drug records with detailed information such as name, target, indications, and molecular properties
        - total_count (int): Total number of drugs returned in the response
        - metadata (Dict): Additional context about the query execution including drug type requested and timestamp of retrieval

    Raises:
        ValueError: If drug_type is empty or not a string
    """
    if not drug_type or not isinstance(drug_type, str):
        raise ValueError("drug_type must be a non-empty string")

    # Call external API to get flat data
    api_data = call_external_api("chembl-server-example_drug")

    # Construct drugs list from indexed fields
    drugs = [
        {
            "name": api_data["drug_0_name"],
            "target": api_data["drug_0_target"],
            "indications": api_data["drug_0_indications"],
            "molecular_properties": {
                "molecular_weight": api_data["drug_0_molecular_weight"],
                "chembl_id": api_data["drug_0_chembl_id"]
            }
        },
        {
            "name": api_data["drug_1_name"],
            "target": api_data["drug_1_target"],
            "indications": api_data["drug_1_indications"],
            "molecular_properties": {
                "molecular_weight": api_data["drug_1_molecular_weight"],
                "chembl_id": api_data["drug_1_chembl_id"]
            }
        }
    ]

    # Construct metadata
    metadata = {
        "drug_type": api_data["metadata_drug_type"],
        "timestamp": api_data["metadata_timestamp"]
    }

    # Return final structured response
    return {
        "drugs": drugs,
        "total_count": api_data["total_count"],
        "metadata": metadata
    }