from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound data from PubChem MCP server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - cid (int): PubChem Compound ID
        - iupac_name (str): IUPAC systematic name
        - molecular_formula (str): Molecular formula
        - molecular_weight (str): Average molecular weight in g/mol
        - canonical_smiles (str or None): Canonical SMILES string
        - isomeric_smiles (str or None): Isomeric SMILES string
        - inchi (str): InChI string
        - inchikey (str): InChIKey string
        - xlogp (float): Calculated XLogP value
        - exact_mass (str): Exact mass of the molecule
        - monoisotopic_mass (str): Monoisotopic mass
        - tpsa (float): Topological polar surface area
        - complexity (float): Structural complexity score
        - charge (int): Net charge
        - h_bond_donor_count (int): Number of H-bond donors
        - h_bond_acceptor_count (int): Number of H-bond acceptors
        - rotatable_bond_count (int): Number of rotatable bonds
        - heavy_atom_count (int): Number of non-hydrogen atoms
        - atom_stereo_count (int): Total atom stereocenters
        - defined_atom_stereo_count (int): Defined atom stereocenters
        - undefined_atom_stereo_count (int): Undefined atom stereocenters
        - bond_stereo_count (int): Total bond stereocenters
        - defined_bond_stereo_count (int): Defined bond stereocenters
        - undefined_bond_stereo_count (int): Undefined bond stereocenters
        - covalent_unit_count (int): Number of covalent units
        - synonyms_0 (str): First synonym
        - synonyms_1 (str): Second synonym
    """
    return {
        "cid": 2244,
        "iupac_name": "acetylsalicylic acid",
        "molecular_formula": "C9H8O4",
        "molecular_weight": "180.157",
        "canonical_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "isomeric_smiles": None,
        "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
        "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "xlogp": 1.2,
        "exact_mass": "180.042",
        "monoisotopic_mass": "180.042",
        "tpsa": 63.6,
        "complexity": 276,
        "charge": 0,
        "h_bond_donor_count": 1,
        "h_bond_acceptor_count": 4,
        "rotatable_bond_count": 4,
        "heavy_atom_count": 13,
        "atom_stereo_count": 0,
        "defined_atom_stereo_count": 0,
        "undefined_atom_stereo_count": 0,
        "bond_stereo_count": 0,
        "defined_bond_stereo_count": 0,
        "undefined_bond_stereo_count": 0,
        "covalent_unit_count": 1,
        "synonyms_0": "Aspirin",
        "synonyms_1": "2-acetyloxybenzoic acid"
    }

def pubchem_mcp_server_get_pubchem_compound_by_cid(cid: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve PubChem compound information by Compound ID (CID).
    
    Args:
        cid (int): PubChem Compound ID (CID) uniquely identifying the compound
        
    Returns:
        Dict containing compound information with the following fields:
        - cid (int): PubChem Compound ID
        - iupac_name (str): IUPAC systematic name
        - molecular_formula (str): Molecular formula
        - molecular_weight (str): Average molecular weight in g/mol
        - canonical_smiles (str or None): Canonical SMILES string
        - isomeric_smiles (str or None): Isomeric SMILES string
        - inchi (str): InChI string
        - inchikey (str): InChIKey string
        - xlogp (float): Calculated XLogP value
        - exact_mass (str): Exact mass
        - monoisotopic_mass (str): Monoisotopic mass
        - tpsa (float): Topological polar surface area
        - complexity (float): Structural complexity
        - charge (int): Net charge
        - h_bond_donor_count (int): H-bond donor count
        - h_bond_acceptor_count (int): H-bond acceptor count
        - rotatable_bond_count (int): Rotatable bond count
        - heavy_atom_count (int): Heavy atom count
        - atom_stereo_count (int): Total atom stereocenters
        - defined_atom_stereo_count (int): Defined atom stereocenters
        - undefined_atom_stereo_count (int): Undefined atom stereocenters
        - bond_stereo_count (int): Total bond stereocenters
        - defined_bond_stereo_count (int): Defined bond stereocenters
        - undefined_bond_stereo_count (int): Undefined bond stereocenters
        - covalent_unit_count (int): Covalent unit count
        - synonyms (List[str]): List of alternative names
        
    Returns None if compound not found.
    """
    if not isinstance(cid, int) or cid <= 0:
        raise ValueError("CID must be a positive integer")
        
    try:
        api_data = call_external_api("pubchem-mcp-server-get_pubchem_compound_by_cid")
        
        # Construct the synonyms list from indexed fields
        synonyms = [
            api_data["synonyms_0"],
            api_data["synonyms_1"]
        ]
        
        # Build the complete compound data structure
        compound_data = {
            "cid": api_data["cid"],
            "iupac_name": api_data["iupac_name"],
            "molecular_formula": api_data["molecular_formula"],
            "molecular_weight": api_data["molecular_weight"],
            "canonical_smiles": api_data["canonical_smiles"] if api_data["canonical_smiles"] is not None else None,
            "isomeric_smiles": api_data["isomeric_smiles"] if api_data["isomeric_smiles"] is not None else None,
            "inchi": api_data["inchi"],
            "inchikey": api_data["inchikey"],
            "xlogp": api_data["xlogp"],
            "exact_mass": api_data["exact_mass"],
            "monoisotopic_mass": api_data["monoisotopic_mass"],
            "tpsa": api_data["tpsa"],
            "complexity": api_data["complexity"],
            "charge": api_data["charge"],
            "h_bond_donor_count": api_data["h_bond_donor_count"],
            "h_bond_acceptor_count": api_data["h_bond_acceptor_count"],
            "rotatable_bond_count": api_data["rotatable_bond_count"],
            "heavy_atom_count": api_data["heavy_atom_count"],
            "atom_stereo_count": api_data["atom_stereo_count"],
            "defined_atom_stereo_count": api_data["defined_atom_stereo_count"],
            "undefined_atom_stereo_count": api_data["undefined_atom_stereo_count"],
            "bond_stereo_count": api_data["bond_stereo_count"],
            "defined_bond_stereo_count": api_data["defined_bond_stereo_count"],
            "undefined_bond_stereo_count": api_data["undefined_bond_stereo_count"],
            "covalent_unit_count": api_data["covalent_unit_count"],
            "synonyms": synonyms
        }
        
        return compound_data
        
    except Exception as e:
        # In a real implementation, this might handle API errors
        # For this simulation, we return None if something goes wrong
        return None