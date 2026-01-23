from typing import Dict, Any
import re
from datetime import datetime

def chembl_server_example_removeHs(smiles: str) -> Dict[str, Any]:
    """
    Remove hydrogen atoms from SMILES string.
    
    Args:
        smiles (str): Input SMILES string
        
    Returns:
        Dict with the following keys:
        - processed_smiles (str): SMILES string with hydrogen atoms removed
        - success (bool): Indicates whether the hydrogen removal was successful
        - original_smiles (str): The original SMILES string provided as input
        - metadata (Dict): Additional information about the processing, such as number of hydrogens removed, timestamp, or software version used
    """
    try:
        if not isinstance(smiles, str) or not smiles.strip():
            return {
                "processed_smiles": "",
                "success": False,
                "original_smiles": smiles or "",
                "metadata": {
                    "hydrogens_removed": 0,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "version": "1.0.0"
                }
            }
        
        # Count hydrogens (explicit H atoms in SMILES)
        # This regex matches H not followed by lowercase (to avoid matching CH, NH, etc.)
        # and standalone [H] (explicit hydrogen)
        hydrogen_pattern = r'H(?![a-z])|\[H\]'
        hydrogens = re.findall(hydrogen_pattern, smiles)
        num_hydrogens = len(hydrogens)
        
        # Remove hydrogens
        processed = re.sub(hydrogen_pattern, '', smiles)
        
        # Clean up any resulting invalid syntax (e.g., empty parentheses)
        # Remove empty brackets or parentheses
        processed = re.sub(r'\(\)', '', processed)
        processed = re.sub(r'\[\]', '', processed)
        
        # Ensure we don't return empty string if only hydrogens were present
        if not processed:
            processed = ""
            success = False
        else:
            success = True
        
        return {
            "processed_smiles": processed,
            "success": success,
            "original_smiles": smiles,
            "metadata": {
                "hydrogens_removed": num_hydrogens,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": "1.0.0"
            }
        }
        
    except Exception as e:
        return {
            "processed_smiles": "",
            "success": False,
            "original_smiles": smiles or "",
            "metadata": {
                "hydrogens_removed": 0,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": "1.0.0",
                "error": str(e)
            }
        }