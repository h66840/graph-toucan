from typing import Dict, Any
import re
import hashlib
from itertools import groupby

def chembl_server_example_smiles2inchiKey(smiles: str) -> Dict[str, Any]:
    """
    Convert SMILES string to InChI Key.
    
    This function simulates the conversion of a SMILES (Simplified Molecular Input Line Entry System)
    string into an InChI Key (International Chemical Identifier Key) using a deterministic hashing
    approach that mimics realistic behavior without requiring external cheminformatics libraries.
    
    Args:
        smiles (str): A SMILES string representing a chemical structure
        
    Returns:
        Dict[str, str]: A dictionary containing the generated InChI Key
        
    Raises:
        ValueError: If the SMILES string is empty or contains invalid characters
    """
    # Input validation
    if not smiles:
        raise ValueError("SMILES string cannot be empty")
    
    if not isinstance(smiles, str):
        raise ValueError("SMILES must be a string")
    
    # Basic SMILES character validation
    # Allow alphanumeric, parentheses, brackets, +, -, =, #, ., /, \, @, :, space
    if not re.match(r'^[A-Za-z0-9\(\)\[\]\+\-\=\#\.\\/\\\@\:\s]+$', smiles):
        raise ValueError("SMILES contains invalid characters")
    
    # Generate InChI Key using a deterministic algorithm
    # InChI Key format: XXXXXXXX-XXXXXX-X (14-10-1 characters)
    # We'll simulate this using SHA-256 hash of the SMILES string
    
    # Normalize the SMILES string (remove spaces, standardize)
    normalized_smiles = re.sub(r'\s+', '', smiles.strip())
    
    # Create hash from SMILES
    hash_input = f"SMILES:{normalized_smiles}".encode('utf-8')
    sha256_hash = hashlib.sha256(hash_input).hexdigest().upper()
    
    # Format as InChI Key: 14-10-1 characters
    part1 = sha256_hash[:14]
    part2 = sha256_hash[14:24]
    # Third part is single character, often derived from protonation state
    # We'll use a checksum of the string
    checksum = sum(ord(c) for c in normalized_smiles) % 26
    part3 = chr(65 + checksum)  # A-Z
    
    inchi_key = f"{part1}-{part2}-{part3}"
    
    return {"inchi_key": inchi_key}