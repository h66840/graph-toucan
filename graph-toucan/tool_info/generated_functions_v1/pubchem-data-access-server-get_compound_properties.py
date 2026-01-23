from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound properties data from external PubChem API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - CID (int): PubChem Compound Identifier
        - MolecularFormula (str): Molecular formula of the compound
        - MolecularWeight (float): Molecular weight in g/mol
        - SMILES (str): Simplified Molecular Input Line Entry System notation
        - IUPACName (str): IUPAC name of the compound
        - XLogP (float): Octanol-water partition coefficient
        - ExactMass (float): Exact mass of the most abundant isotope
        - MonoisotopicMass (float): Monoisotopic mass in atomic mass units
        - TPSA (float): Topological polar surface area in Å²
        - Complexity (float): Complexity score of the compound
        - Charge (int): Net charge of the molecule
        - HBondDonorCount (int): Number of hydrogen bond donors
        - HBondAcceptorCount (int): Number of hydrogen bond acceptors
        - RotatableBondCount (int): Number of rotatable bonds
        - ConnectivitySMILES (str): Canonical SMILES without chiral or isotopic information
    """
    return {
        "CID": 2244,
        "MolecularFormula": "C9H8O4",
        "MolecularWeight": 180.157,
        "SMILES": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "IUPACName": "acetylsalicylic acid",
        "XLogP": 1.2,
        "ExactMass": 180.042,
        "MonoisotopicMass": 180.042,
        "TPSA": 63.6,
        "Complexity": 276,
        "Charge": 0,
        "HBondDonorCount": 1,
        "HBondAcceptorCount": 4,
        "RotatableBondCount": 4,
        "ConnectivitySMILES": "CC(=O)OC1=CC=CC=C1C(=O)O"
    }

def pubchem_data_access_server_get_compound_properties(cid: int) -> Dict[str, Any]:
    """
    Get physical and chemical properties of a compound from PubChem by CID.
    
    Args:
        cid (int): PubChem Compound ID (CID)
        
    Returns:
        Dictionary containing compound properties with structure:
        - CID (int): PubChem Compound Identifier
        - properties (Dict): Detailed molecular and chemical properties including:
            - MolecularFormula (str)
            - MolecularWeight (float)
            - SMILES (str)
            - IUPACName (str)
            - XLogP (float)
            - ExactMass (float)
            - MonoisotopicMass (float)
            - TPSA (float)
            - Complexity (float)
            - Charge (int)
            - HBondDonorCount (int)
            - HBondAcceptorCount (int)
            - RotatableBondCount (int)
            - ConnectivitySMILES (str)
            
    Raises:
        ValueError: If cid is not a positive integer
    """
    if not isinstance(cid, int) or cid <= 0:
        raise ValueError("CID must be a positive integer")
    
    # Call external API to get flattened data
    api_data = call_external_api("pubchem-data-access-server-get_compound_properties")
    
    # Construct nested structure matching output schema
    result = {
        "CID": api_data["CID"],
        "properties": {
            "MolecularFormula": api_data["MolecularFormula"],
            "MolecularWeight": api_data["MolecularWeight"],
            "SMILES": api_data["SMILES"],
            "IUPACName": api_data["IUPACName"],
            "XLogP": api_data["XLogP"],
            "ExactMass": api_data["ExactMass"],
            "MonoisotopicMass": api_data["MonoisotopicMass"],
            "TPSA": api_data["TPSA"],
            "Complexity": api_data["Complexity"],
            "Charge": api_data["Charge"],
            "HBondDonorCount": api_data["HBondDonorCount"],
            "HBondAcceptorCount": api_data["HBondAcceptorCount"],
            "RotatableBondCount": api_data["RotatableBondCount"],
            "ConnectivitySMILES": api_data["ConnectivitySMILES"]
        }
    }
    
    return result