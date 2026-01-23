from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external PubChem API by tool name.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - cid (int): PubChem compound identifier
        - iupac_name (str): IUPAC systematic name; None if unavailable
        - molecular_formula (str): molecular formula; None if unavailable
        - molecular_weight (float): average molecular weight in g/mol; None if unavailable
        - canonical_smiles (str): canonical SMILES string; None if unavailable
        - isomeric_smiles (str): isomeric SMILES with stereochemistry; None if unavailable
        - inchi (str): InChI string; None if unavailable
        - inchikey (str): hashed InChI; None if unavailable
        - xlogp (float): computed octanol/water partition coefficient; None if unavailable
        - exact_mass (float): exact mass of most abundant isotopic composition; None if unavailable
        - monoisotopic_mass (float): mass using most abundant isotope; None if unavailable
        - tpsa (float): topological polar surface area in Å²; None if unavailable
        - complexity (float): complexity score based on molecular features; None if unavailable
        - charge (int): net charge of the molecule
        - h_bond_donor_count (int): number of hydrogen bond donors; None if unavailable
        - h_bond_acceptor_count (int): number of hydrogen bond acceptors; None if unavailable
        - rotatable_bond_count (int): number of rotatable bonds; None if unavailable
        - heavy_atom_count (int): number of non-hydrogen atoms
        - atom_stereo_count (int): total number of stereocenters at atoms
        - defined_atom_stereo_count (int): number of defined stereocenters at atoms
        - undefined_atom_stereo_count (int): number of undefined stereocenters at atoms
        - bond_stereo_count (int): total number of stereocenters at bonds
        - defined_bond_stereo_count (int): number of defined stereocenters at bonds
        - undefined_bond_stereo_count (int): number of undefined stereocenters at bonds
        - covalent_unit_count (int): number of covalent units
        - synonyms_0 (str): first synonym
        - synonyms_1 (str): second synonym
    """
    return {
        "cid": 2244,
        "iupac_name": "Aspirin",
        "molecular_formula": "C9H8O4",
        "molecular_weight": 180.157,
        "canonical_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "isomeric_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
        "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "xlogp": 1.2,
        "exact_mass": 180.042,
        "monoisotopic_mass": 180.042,
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
        "synonyms_0": "Acetylsalicylic acid",
        "synonyms_1": "ASA"
    }

def pubchem_mcp_server_search_pubchem_by_name(name: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Searches PubChem database by compound name and returns detailed chemical information.
    
    Args:
        name (str): Required compound name to search in PubChem
        max_results (Optional[int]): Maximum number of results to return (not used in simulation)
    
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing detailed chemical information
        Each dictionary contains:
            - cid (int): PubChem compound identifier
            - iupac_name (Optional[str]): IUPAC systematic name
            - molecular_formula (Optional[str]): molecular formula
            - molecular_weight (Optional[float]): average molecular weight in g/mol
            - canonical_smiles (Optional[str]): canonical SMILES string
            - isomeric_smiles (Optional[str]): isomeric SMILES with stereochemistry
            - inchi (Optional[str]): InChI string
            - inchikey (Optional[str]): hashed InChI
            - xlogp (Optional[float]): computed octanol/water partition coefficient
            - exact_mass (Optional[float]): exact mass of most abundant isotopic composition
            - monoisotopic_mass (Optional[float]): mass using most abundant isotope
            - tpsa (Optional[float]): topological polar surface area in Å²
            - complexity (Optional[float]): complexity score
            - charge (int): net charge
            - h_bond_donor_count (Optional[int]): number of hydrogen bond donors
            - h_bond_acceptor_count (Optional[int]): number of hydrogen bond acceptors
            - rotatable_bond_count (Optional[int]): number of rotatable bonds
            - heavy_atom_count (int): number of non-hydrogen atoms
            - atom_stereo_count (int): total number of stereocenters at atoms
            - defined_atom_stereo_count (int): number of defined stereocenters at atoms
            - undefined_atom_stereo_count (int): number of undefined stereocenters at atoms
            - bond_stereo_count (int): total number of stereocenters at bonds
            - defined_bond_stereo_count (int): number of defined stereocenters at bonds
            - undefined_bond_stereo_count (int): number of undefined stereocenters at bonds
            - covalent_unit_count (int): number of covalent units
            - synonyms (List[str]): list of alternative names and identifiers
    """
    if not name or not name.strip():
        raise ValueError("Parameter 'name' is required and cannot be empty")
    
    if max_results is not None and max_results <= 0:
        raise ValueError("Parameter 'max_results' must be positive if provided")
    
    # Call simulated external API
    api_data = call_external_api("pubchem_mcp_server_search_pubchem_by_name")
    
    # Construct the synonyms list from indexed fields
    synonyms = []
    for i in range(2):  # We have 2 synonyms in the simulation
        synonym_key = f"synonyms_{i}"
        if synonym_key in api_data and api_data[synonym_key] is not None:
            synonyms.append(api_data[synonym_key])
    
    # Construct the result dictionary matching the output schema
    result = {
        "cid": api_data["cid"],
        "iupac_name": api_data["iupac_name"] if api_data["iupac_name"] is not None else None,
        "molecular_formula": api_data["molecular_formula"] if api_data["molecular_formula"] is not None else None,
        "molecular_weight": api_data["molecular_weight"] if api_data["molecular_weight"] is not None else None,
        "canonical_smiles": api_data["canonical_smiles"] if api_data["canonical_smiles"] is not None else None,
        "isomeric_smiles": api_data["isomeric_smiles"] if api_data["isomeric_smiles"] is not None else None,
        "inchi": api_data["inchi"] if api_data["inchi"] is not None else None,
        "inchikey": api_data["inchikey"] if api_data["inchikey"] is not None else None,
        "xlogp": api_data["xlogp"] if api_data["xlogp"] is not None else None,
        "exact_mass": api_data["exact_mass"] if api_data["exact_mass"] is not None else None,
        "monoisotopic_mass": api_data["monoisotopic_mass"] if api_data["monoisotopic_mass"] is not None else None,
        "tpsa": api_data["tpsa"] if api_data["tpsa"] is not None else None,
        "complexity": api_data["complexity"] if api_data["complexity"] is not None else None,
        "charge": api_data["charge"],
        "h_bond_donor_count": api_data["h_bond_donor_count"] if api_data["h_bond_donor_count"] is not None else None,
        "h_bond_acceptor_count": api_data["h_bond_acceptor_count"] if api_data["h_bond_acceptor_count"] is not None else None,
        "rotatable_bond_count": api_data["rotatable_bond_count"] if api_data["rotatable_bond_count"] is not None else None,
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
    
    return [result]