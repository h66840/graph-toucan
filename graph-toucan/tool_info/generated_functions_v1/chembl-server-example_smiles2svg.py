from typing import Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

def chembl_server_example_smiles2svg(smiles: str) -> Dict[str, Any]:
    """
    Convert SMILES string to SVG image representation.
    
    This function takes a SMILES (Simplified Molecular Input Line Entry System) string
    and generates a simple SVG visualization of the molecular structure. The rendering
    is schematic and does not represent exact molecular geometry but provides a basic
    structural depiction.
    
    Args:
        smiles (str): A SMILES string representing a chemical compound
        
    Returns:
        Dict[str, Any]: A dictionary containing the SVG content as a string
            - svg_content (str): The full SVG XML string representing the molecular structure
    """
    if not smiles or not isinstance(smiles, str):
        raise ValueError("SMILES string must be a non-empty string")
    
    # Basic validation of SMILES characters (simplified)
    valid_chars = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz()=+#-./\\[]')
    if not all(c in valid_chars for c in smiles):
        raise ValueError("Invalid characters in SMILES string")
    
    # Generate a simple SVG representation
    svg_content = generate_svg_from_smiles(smiles)
    
    return {"svg_content": svg_content}

def generate_svg_from_smiles(smiles: str) -> str:
    """
    Generate SVG XML string from SMILES string with basic layout.
    
    Args:
        smiles (str): The SMILES string to visualize
        
    Returns:
        str: SVG XML string representing the molecule
    """
    # Calculate approximate width based on SMILES length
    width = max(200, len(smiles) * 20)
    height = 100
    
    # Create SVG root element
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width': str(width),
        'height': str(height),
        'version': '1.1'
    })
    
    # Add white background
    ET.SubElement(svg, 'rect', {
        'width': '100%',
        'height': '100%',
        'fill': 'white'
    })
    
    # Add molecule label
    text = ET.SubElement(svg, 'text', {
        'x': '50%',
        'y': '50%',
        'font-family': 'Arial, sans-serif',
        'font-size': '16',
        'text-anchor': 'middle',
        'fill': 'black'
    })
    text.text = smiles
    
    # Convert to string and pretty print
    rough_string = ET.tostring(svg, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")