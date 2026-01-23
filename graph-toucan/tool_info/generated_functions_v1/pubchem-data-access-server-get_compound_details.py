from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound data from PubChem Data Access Server.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - CID (int): PubChem Compound ID
        - properties_MolecularFormula (str): Molecular formula of the compound
        - properties_MolecularWeight (float): Molecular weight in g/mol
        - properties_ConnectivitySMILES (str): Canonical SMILES string
        - properties_IUPACName (str): Preferred IUPAC name
        - properties_XLogP (float): Calculated octanol-water partition coefficient
        - properties_ExactMass (float): Exact mass of the most abundant isotope
        - properties_MonoisotopicMass (float): Monoisotopic mass
        - properties_TPSA (float): Topological polar surface area in Å²
        - properties_HBondDonorCount (int): Number of hydrogen bond donors
        - properties_HBondAcceptorCount (int): Number of hydrogen bond acceptors
        - properties_RotatableBondCount (int): Number of rotatable bonds
        - synonyms_0 (str): First synonym or alternative name
        - synonyms_1 (str): Second synonym or alternative name
        - record_atom_count (int): Total number of atoms
        - record_bond_count (int): Total number of bonds
        - record_heavy_atom_count (int): Number of non-hydrogen atoms
        - record_chiral_center_count (int): Number of chiral centers
        - record_charge (int): Total molecular charge
    """
    return {
        "CID": 2244,
        "properties_MolecularFormula": "C9H8O4",
        "properties_MolecularWeight": 180.157,
        "properties_ConnectivitySMILES": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "properties_IUPACName": "acetylsalicylic acid",
        "properties_XLogP": 1.2,
        "properties_ExactMass": 180.037,
        "properties_MonoisotopicMass": 180.037,
        "properties_TPSA": 63.6,
        "properties_HBondDonorCount": 1,
        "properties_HBondAcceptorCount": 4,
        "properties_RotatableBondCount": 4,
        "synonyms_0": "Aspirin",
        "synonyms_1": "2-acetyloxybenzoic acid",
        "record_atom_count": 21,
        "record_bond_count": 24,
        "record_heavy_atom_count": 17,
        "record_chiral_center_count": 0,
        "record_charge": 0
    }

def pubchem_data_access_server_get_compound_details(cid: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific compound by its PubChem CID.
    
    Args:
        cid (int): PubChem Compound ID (CID)
        
    Returns:
        Dictionary with compound details including:
        - CID (int): PubChem Compound ID
        - properties (Dict): Key chemical properties including MolecularFormula, MolecularWeight,
          ConnectivitySMILES, IUPACName, XLogP, ExactMass, MonoisotopicMass, TPSA,
          HBondDonorCount, HBondAcceptorCount, and RotatableBondCount
        - synonyms (List[str]): List of alternative names and identifiers for the compound
        - record (Dict): Detailed structural record containing atom, bond, charge,
          and count information including heavy atom count and chiral features
          
    Raises:
        ValueError: If CID is not a positive integer
    """
    if not isinstance(cid, int) or cid <= 0:
        raise ValueError("CID must be a positive integer")
    
    # Call external API to get flattened data
    api_data = call_external_api("pubchem-data-access-server-get_compound_details")
    
    # Construct nested structure matching output schema
    result = {
        "CID": cid,
        "properties": {
            "MolecularFormula": api_data["properties_MolecularFormula"],
            "MolecularWeight": api_data["properties_MolecularWeight"],
            "ConnectivitySMILES": api_data["properties_ConnectivitySMILES"],
            "IUPACName": api_data["properties_IUPACName"],
            "XLogP": api_data["properties_XLogP"],
            "ExactMass": api_data["properties_ExactMass"],
            "MonoisotopicMass": api_data["properties_MonoisotopicMass"],
            "TPSA": api_data["properties_TPSA"],
            "HBondDonorCount": api_data["properties_HBondDonorCount"],
            "HBondAcceptorCount": api_data["properties_HBondAcceptorCount"],
            "RotatableBondCount": api_data["properties_RotatableBondCount"]
        },
        "synonyms": [
            api_data["synonyms_0"],
            api_data["synonyms_1"]
        ],
        "record": {
            "atom": {"count": api_data["record_atom_count"]},
            "bond": {"count": api_data["record_bond_count"]},
            "charge": api_data["record_charge"],
            "props": {},
            "count": {
                "heavy_atom": api_data["record_heavy_atom_count"],
                "chiral_center": api_data["record_chiral_center_count"]
            }
        }
    }
    
    return result