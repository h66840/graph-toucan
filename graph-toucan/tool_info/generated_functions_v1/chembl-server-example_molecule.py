from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching molecule data from external ChEMBL server API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - molecule_0_molecular_formula (str): Molecular formula of first molecule
        - molecule_0_molecular_weight (float): Molecular weight of first molecule
        - molecule_0_chembl_id (str): ChEMBL ID of first molecule
        - molecule_0_iupac_name (str): IUPAC name of first molecule
        - molecule_0_smiles (str): SMILES representation of first molecule
        - molecule_0_inchi (str): InChI representation of first molecule
        - molecule_0_target (str): Biological target of first molecule
        - molecule_0_bioactivity_value (float): Bioactivity value (e.g., IC50) of first molecule
        - molecule_1_molecular_formula (str): Molecular formula of second molecule
        - molecule_1_molecular_weight (float): Molecular weight of second molecule
        - molecule_1_chembl_id (str): ChEMBL ID of second molecule
        - molecule_1_iupac_name (str): IUPAC name of second molecule
        - molecule_1_smiles (str): SMILES representation of second molecule
        - molecule_1_inchi (str): InChI representation of second molecule
        - molecule_1_target (str): Biological target of second molecule
        - molecule_1_bioactivity_value (float): Bioactivity value (e.g., IC50) of second molecule
        - count (int): Total number of molecules returned
        - molecule_type (str): The type of molecule queried
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, otherwise null
    """
    return {
        "molecule_0_molecular_formula": "C27H36N2O10",
        "molecule_0_molecular_weight": 548.58,
        "molecule_0_chembl_id": "CHEMBL12345",
        "molecule_0_iupac_name": "(2S)-2-[(1R)-1-hydroxyethyl]-4,6-dimethyl-7-oxo-8-[(2S,3R,4R,5R,6S)-3,4,5-trihydroxy-6-(hydroxymethyl)oxan-2-yl]oxy-1,5-diazabicyclo[3.3.0]octane-3-carboxamide",
        "molecule_0_smiles": "CC[C@H](C)[C@H]1C(=O)N[C@H](C)[C@@H](C)C(=O)N1CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1O",
        "molecule_0_inchi": "InChI=1S/C27H36N2O10/c1-5-14(2)22-25(33)28-13(3)19(7-4)24(32)29-22(6-8-26(34)30-20-17(31)15(29)16(30)10-35-20)21(31)23(32)18(27(36)37)11-9-12(28)27/h12-22,31-32H,5-11H2,1-4H3,(H,28,34)(H,29,33)(H,30,36,37)/t12-,13+,14+,15+,16+,17+,18+,19+,20+,21+,22+/m0/s1",
        "molecule_0_target": "Beta-lactamase",
        "molecule_0_bioactivity_value": 0.045,
        "molecule_1_molecular_formula": "C16H19N3O2S",
        "molecule_1_molecular_weight": 333.40,
        "molecule_1_chembl_id": "CHEMBL67890",
        "molecule_1_iupac_name": "N-(4-methoxybenzyl)-1-methyl-2-oxo-1,2-dihydro-4-pyridinecarboxamide",
        "molecule_1_smiles": "COc1ccc(CCN(C)c2ccc(C(N)=O)cc2)cc1",
        "molecule_1_inchi": "InChI=1S/C16H19N3O2S/c1-12-10-18(2)16(20)11-8-14-6-4-13(5-7-14)17-9-15(19)21-3/h4-8,10,12,17H,9,11H2,1-3H3,(H,18,20)",
        "molecule_1_target": "Carbonic anhydrase II",
        "molecule_1_bioactivity_value": 0.012,
        "count": 2,
        "molecule_type": "small molecule",
        "success": True,
        "error_message": None
    }

def chembl_server_example_molecule(molecule_type: str) -> Dict[str, Any]:
    """
    Get molecule data for the specified type.
    
    Args:
        molecule_type (str): The type of molecule to query (e.g., 'small molecule', 'antibody', 'peptide')
        
    Returns:
        Dict containing:
        - molecules (List[Dict]): List of molecule records with chemical and biological properties
        - count (int): Total number of molecules returned
        - molecule_type (str): The queried molecule type
        - success (bool): Whether the request was processed successfully
        - error_message (Optional[str]): Error description if failed, otherwise None
    """
    # Input validation
    if not molecule_type or not isinstance(molecule_type, str):
        return {
            "molecules": [],
            "count": 0,
            "molecule_type": "",
            "success": False,
            "error_message": "Invalid molecule_type: must be a non-empty string"
        }
    
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("chembl-server-example_molecule")
        
        # Construct molecules list from indexed fields
        molecules = [
            {
                "molecular_formula": api_data["molecule_0_molecular_formula"],
                "molecular_weight": api_data["molecule_0_molecular_weight"],
                "chembl_id": api_data["molecule_0_chembl_id"],
                "iupac_name": api_data["molecule_0_iupac_name"],
                "smiles": api_data["molecule_0_smiles"],
                "inchi": api_data["molecule_0_inchi"],
                "target": api_data["molecule_0_target"],
                "bioactivity_value": api_data["molecule_0_bioactivity_value"]
            },
            {
                "molecular_formula": api_data["molecule_1_molecular_formula"],
                "molecular_weight": api_data["molecule_1_molecular_weight"],
                "chembl_id": api_data["molecule_1_chembl_id"],
                "iupac_name": api_data["molecule_1_iupac_name"],
                "smiles": api_data["molecule_1_smiles"],
                "inchi": api_data["molecule_1_inchi"],
                "target": api_data["molecule_1_target"],
                "bioactivity_value": api_data["molecule_1_bioactivity_value"]
            }
        ]
        
        # Construct final result matching output schema
        result = {
            "molecules": molecules,
            "count": api_data["count"],
            "molecule_type": api_data["molecule_type"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except Exception as e:
        return {
            "molecules": [],
            "count": 0,
            "molecule_type": molecule_type,
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}"
        }