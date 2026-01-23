from typing import Dict, Any
import re
import hashlib

def chembl_server_example_inchi2inchiKey(inchi: str) -> Dict[str, Any]:
    """
    Convert InChI to InChI Key.
    
    This function takes an InChI string as input and generates the corresponding InChI Key.
    The conversion is based on a simplified simulation of the standard InChI to InChIKey algorithm,
    using SHA-256 hashing of the InChI string and formatting the result according to InChIKey conventions.
    
    Args:
        inchi (str): The input InChI string (e.g., "InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H")
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - inchi_key (str): The generated InChI Key corresponding to the input InChI string
            - success (bool): Indicates whether the conversion from InChI to InChI Key was successful
            - error_message (str): Descriptive error message if the conversion failed (e.g., invalid InChI format)
            - metadata (Dict): Additional information about the conversion process, such as version of the cheminformatics backend or timestamp of operation
    """
    # Input validation
    if not isinstance(inchi, str):
        return {
            "inchi_key": "",
            "success": False,
            "error_message": "Input must be a string",
            "metadata": {
                "backend_version": "1.0.0",
                "conversion_method": "simulated_sha256"
            }
        }
    
    if not inchi:
        return {
            "inchi_key": "",
            "success": False,
            "error_message": "Input InChI string cannot be empty",
            "metadata": {
                "backend_version": "1.0.0",
                "conversion_method": "simulated_sha256"
            }
        }
    
    # Basic InChI format validation
    inchi_pattern = r'^InChI=1S?\/[A-Za-z0-9\.]+.*$'
    if not re.match(inchi_pattern, inchi):
        return {
            "inchi_key": "",
            "success": False,
            "error_message": "Invalid InChI format. Must start with 'InChI=1S/'",
            "metadata": {
                "backend_version": "1.0.0",
                "conversion_method": "simulated_sha256"
            }
        }
    
    try:
        # Simulate InChIKey generation using SHA-256 hash of the InChI string
        # In a real implementation, this would use the IUPAC InChI software library
        hash_object = hashlib.sha256(inchi.encode())
        hex_dig = hash_object.hexdigest()
        
        # Format as InChIKey: 14 characters + 8 characters + 1 character
        # Example: XLYOFNOQVPJJNP-UHFFFAOYSA-N
        part1 = hex_dig[:14].upper()
        part2 = hex_dig[14:22].upper()
        # Simple checksum character (simulated)
        checksum = 'S'  # Simulated checksum character
        
        inchi_key = f"{part1}-{part2}-{checksum}"
        
        return {
            "inchi_key": inchi_key,
            "success": True,
            "error_message": "",
            "metadata": {
                "backend_version": "1.0.0",
                "conversion_method": "simulated_sha256"
            }
        }
        
    except Exception as e:
        return {
            "inchi_key": "",
            "success": False,
            "error_message": f"Unexpected error during conversion: {str(e)}",
            "metadata": {
                "backend_version": "1.0.0",
                "conversion_method": "simulated_sha256"
            }
        }