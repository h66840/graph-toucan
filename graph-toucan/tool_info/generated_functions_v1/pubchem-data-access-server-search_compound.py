from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound data from PubChem API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - count (int): Total number of compounds found
        - compound_0_CID (int): CID of first compound
        - compound_0_IUPACName (str): IUPAC name of first compound
        - compound_0_MolecularFormula (str): Molecular formula of first compound
        - compound_0_MolecularWeight (float): Molecular weight of first compound
        - compound_0_CanonicalSMILES (str): Canonical SMILES of first compound
        - compound_1_CID (int): CID of second compound
        - compound_1_IUPACName (str): IUPAC name of second compound
        - compound_1_MolecularFormula (str): Molecular formula of second compound
        - compound_1_MolecularWeight (float): Molecular weight of second compound
        - compound_1_CanonicalSMILES (str): Canonical SMILES of second compound
    """
    return {
        "count": 2,
        "compound_0_CID": 2244,
        "compound_0_IUPACName": "Aspirin",
        "compound_0_MolecularFormula": "C9H8O4",
        "compound_0_MolecularWeight": 180.157,
        "compound_0_CanonicalSMILES": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "compound_1_CID": 1983,
        "compound_1_IUPACName": "Caffeine",
        "compound_1_MolecularFormula": "C8H10N4O2",
        "compound_1_MolecularWeight": 194.19,
        "compound_1_CanonicalSMILES": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    }

def pubchem_data_access_server_search_compound(query: str, max_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Search for compounds by name, CID, or other identifiers.
    
    Args:
        query (str): The search query (compound name, CID, SMILES, etc.)
        max_results (int, optional): Maximum number of results to return. Defaults to 10.
        
    Returns:
        Dict containing:
            - count (int): total number of compounds found matching the query
            - compounds (List[Dict]): list of compound records with 'CID', 'IUPACName', 
              'MolecularFormula', 'MolecularWeight', and 'CanonicalSMILES' fields
    
    Raises:
        ValueError: If query is empty or max_results is not positive
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    if max_results is not None and max_results <= 0:
        raise ValueError("max_results must be a positive integer")
    
    # Call external API to get flat data
    api_data = call_external_api("pubchem-data-access-server-search_compound")
    
    # Construct compounds list from indexed fields
    compounds = []
    
    # Add first compound if available
    if "compound_0_CID" in api_data:
        compounds.append({
            "CID": api_data["compound_0_CID"],
            "IUPACName": api_data["compound_0_IUPACName"],
            "MolecularFormula": api_data["compound_0_MolecularFormula"],
            "MolecularWeight": api_data["compound_0_MolecularWeight"],
            "CanonicalSMILES": api_data["compound_0_CanonicalSMILES"]
        })
    
    # Add second compound if available and within max_results limit
    if len(compounds) < max_results and "compound_1_CID" in api_data:
        compounds.append({
            "CID": api_data["compound_1_CID"],
            "IUPACName": api_data["compound_1_IUPACName"],
            "MolecularFormula": api_data["compound_1_MolecularFormula"],
            "MolecularWeight": api_data["compound_1_MolecularWeight"],
            "CanonicalSMILES": api_data["compound_1_CanonicalSMILES"]
        })
    
    # Apply max_results limit
    compounds = compounds[:max_results]
    
    # Construct final result
    result = {
        "count": api_data["count"],
        "compounds": compounds
    }
    
    return result