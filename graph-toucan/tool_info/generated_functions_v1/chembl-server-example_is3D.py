from typing import Dict, Any

def chembl_server_example_is3D(smiles: str) -> Dict[str, Any]:
    """
    Check if SMILES string represents a 3D structure.
    
    Args:
        smiles (str): SMILES string representing a molecular structure
        
    Returns:
        Dict with keys:
        - is_3d (bool): Indicates whether the provided SMILES string represents a 3D molecular structure
        - details (Dict): Additional information about the 3D detection, including stereochemistry and chiral centers
    """
    if not isinstance(smiles, str):
        raise TypeError("smiles must be a string")
    
    if not smiles.strip():
        raise ValueError("smiles string cannot be empty or whitespace")
    
    # Check for stereochemistry indicators in SMILES
    has_stereochemistry = any(char in smiles for char in ['@', '@@', '/', '\\'])
    
    # Count chiral centers (indicated by '@' symbols)
    chiral_centers_count = smiles.count('@')
    
    # Presence of 3D coordinates cannot be determined from SMILES alone
    has_3d_coordinates = False
    
    # A SMILES is considered 3D if it contains stereochemical information
    is_3d = has_stereochemistry
    
    details = {
        'has_stereochemistry': has_stereochemistry,
        'has_3d_coordinates': has_3d_coordinates,
        'chiral_centers_count': chiral_centers_count
    }
    
    return {
        'is_3d': is_3d,
        'details': details
    }