from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound record data from external ChEMBL server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - compound_key_0 (str): Compound key for first record
        - compound_name_0 (str): Compound name for first record
        - document_chembl_id_0 (str): Document ChEMBL ID for first record
        - molecule_chembl_id_0 (str): Molecule ChEMBL ID for first record
        - record_id_0 (int): Record ID for first record
        - src_id_0 (int): Source ID for first record
        - compound_key_1 (str): Compound key for second record
        - compound_name_1 (str): Compound name for second record
        - document_chembl_id_1 (str): Document ChEMBL ID for second record
        - molecule_chembl_id_1 (str): Molecule ChEMBL ID for second record
        - record_id_1 (int): Record ID for second record
        - src_id_1 (int): Source ID for second record
    """
    return {
        "compound_key_0": "CHEMBL1234567",
        "compound_name_0": "ASPIRIN",
        "document_chembl_id_0": "CHEMBL1000",
        "molecule_chembl_id_0": "CHEMBL25",
        "record_id_0": 100001,
        "src_id_0": 1,
        "compound_key_1": "CHEMBL7654321",
        "compound_name_1": "ASPIRIN",
        "document_chembl_id_1": "CHEMBL2000",
        "molecule_chembl_id_1": "CHEMBL25",
        "record_id_1": 100002,
        "src_id_1": 2
    }

def chembl_server_example_compound_record(compound_name: str) -> List[Dict[str, Any]]:
    """
    Get compound records for the specified name.
    
    This function simulates querying a ChEMBL server for compound records
    by the given compound name and returns a list of matching records.
    
    Args:
        compound_name (str): The name of the compound to search for (e.g., 'ASPIRIN')
        
    Returns:
        List[Dict]: A list of compound records, each containing:
            - compound_key (str): Unique compound key
            - compound_name (str): Name of the compound
            - document_chembl_id (str): Document identifier in ChEMBL
            - molecule_chembl_id (str): Molecule identifier in ChEMBL
            - record_id (int): Unique record identifier
            - src_id (int): Source identifier
            
    Raises:
        ValueError: If compound_name is empty or not a string
    """
    if not compound_name or not isinstance(compound_name, str):
        raise ValueError("compound_name must be a non-empty string")
    
    # Fetch simulated external API data
    api_data = call_external_api("chembl-server-example_compound_record")
    
    # Construct the results list by mapping flat API fields to nested structure
    results = [
        {
            "compound_key": api_data["compound_key_0"],
            "compound_name": api_data["compound_name_0"],
            "document_chembl_id": api_data["document_chembl_id_0"],
            "molecule_chembl_id": api_data["molecule_chembl_id_0"],
            "record_id": api_data["record_id_0"],
            "src_id": api_data["src_id_0"]
        },
        {
            "compound_key": api_data["compound_key_1"],
            "compound_name": api_data["compound_name_1"],
            "document_chembl_id": api_data["document_chembl_id_1"],
            "molecule_chembl_id": api_data["molecule_chembl_id_1"],
            "record_id": api_data["record_id_1"],
            "src_id": api_data["src_id_1"]
        }
    ]
    
    # Filter results by compound name (case-insensitive)
    filtered_results = [
        record for record in results 
        if record["compound_name"].upper() == compound_name.upper()
    ]
    
    return filtered_results