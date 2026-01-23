from typing import Dict, Any

def chembl_server_example_highlightSmilesFragmentSvg(smiles: str, fragment: str) -> Dict[str, Any]:
    """
    Generate SVG image with highlighted fragment for SMILES string.
    
    Args:
        smiles (str): The SMILES string representing the molecular structure
        fragment (str): The substructure fragment to highlight in the molecule
        
    Returns:
        Dict containing:
        - svg_content (str): The full SVG image string representing the SMILES structure with the specified fragment highlighted
        - highlighted_fragment (str): The fragment that was highlighted in the SMILES structure
        - smiles_string (str): The original SMILES string that was provided for rendering
        - success (bool): Indicates whether the SVG generation and highlighting were successful
        - error_message (str): Error details if the operation failed, otherwise empty string
    """
    try:
        # Input validation
        if not isinstance(smiles, str) or not smiles.strip():
            return {
                "svg_content": "",
                "highlighted_fragment": fragment,
                "smiles_string": smiles,
                "success": False,
                "error_message": "SMILES string is required and must be a non-empty string"
            }
        
        if not isinstance(fragment, str) or not fragment.strip():
            return {
                "svg_content": "",
                "highlighted_fragment": fragment,
                "smiles_string": smiles,
                "success": False,
                "error_message": "Fragment is required and must be a non-empty string"
            }
        
        # Simplified simulation of SVG generation
        # In a real implementation, this would involve cheminformatics libraries like RDKit
        smiles = smiles.strip()
        fragment = fragment.strip()
        
        # Basic check if fragment is contained in smiles (simplified)
        fragment_found = fragment in smiles
        
        if not fragment_found:
            return {
                "svg_content": "",
                "highlighted_fragment": fragment,
                "smiles_string": smiles,
                "success": False,
                "error_message": f"Fragment '{fragment}' not found in SMILES string '{smiles}'"
            }
        
        # Generate a simple SVG representation (simulated)
        # This is a simplified representation for demonstration purposes
        # Fixed the incorrect string replacement that was creating extra spaces
        safe_smiles = smiles
        safe_fragment = fragment
        base_part = safe_smiles.replace(safe_fragment, "")
        fragment_index = safe_smiles.find(safe_fragment)
        
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <rect width="100%" height="100%" fill="white"/>
  <text x="20" y="40" font-family="Arial" font-size="14" fill="black">SMILES: {safe_smiles}</text>
  <text x="20" y="70" font-family="Arial" font-size="14" fill="black">Highlighting fragment: {safe_fragment}</text>
  <rect x="20" y="90" width="360" height="80" fill="none" stroke="lightgray" stroke-width="1"/>
  <!-- Simulated molecular structure with highlighted fragment -->
  <text x="40" y="130" font-family="Arial" font-size="16" fill="black">
    <tspan fill="black">{base_part[:fragment_index]}</tspan>
    <tspan fill="red" font-weight="bold">{safe_fragment}</tspan>
    <tspan fill="black">{base_part[fragment_index:]}</tspan>
  </text>
  <text x="20" y="180" font-family="Arial" font-size="12" fill="gray">Generated SVG representation</text>
</svg>"""
        
        return {
            "svg_content": svg_content,
            "highlighted_fragment": fragment,
            "smiles_string": smiles,
            "success": True,
            "error_message": ""
        }
        
    except Exception as e:
        return {
            "svg_content": "",
            "highlighted_fragment": fragment,
            "smiles_string": smiles,
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}"
        }