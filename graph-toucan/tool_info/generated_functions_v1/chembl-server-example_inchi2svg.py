from typing import Dict, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for InChI to SVG conversion.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - svg_image (str): SVG image string representing molecular structure
        - success (bool): Whether conversion was successful
        - error_message (str): Error message if conversion failed
        - metadata_inchi_version (str): Version of the InChI used
        - metadata_backend_tool (str): Name of the backend tool used for conversion
        - metadata_timestamp (str): ISO format timestamp of generation
    """
    return {
        "svg_image": (
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">'
            '<circle cx="100" cy="100" r="80" fill="none" stroke="black" stroke-width="2"/>'
            '<text x="100" y="100" font-size="16" text-anchor="middle" alignment-baseline="middle">C6H6</text>'
            '</svg>'
        ),
        "success": True,
        "error_message": "",
        "metadata_inchi_version": "1.06",
        "metadata_backend_tool": "Indigo",
        "metadata_timestamp": datetime.now().isoformat()
    }


def chembl_server_example_inchi2svg(inchi: str) -> Dict[str, Any]:
    """
    Convert InChI to SVG image string representing the molecular structure.

    Args:
        inchi (str): InChI string representing a chemical compound

    Returns:
        Dict with the following keys:
        - svg_image (str): SVG image string representing the molecular structure derived from the InChI input
        - success (bool): Indicates whether the conversion from InChI to SVG was successful
        - error_message (str): Descriptive error message if the conversion failed (e.g., invalid InChI format)
        - metadata (Dict): Additional information about the conversion process, such as InChI version,
          backend tool used, and timestamp of generation
    """
    # Input validation
    if not isinstance(inchi, str):
        return {
            "svg_image": "",
            "success": False,
            "error_message": "Input 'inchi' must be a string",
            "metadata": {
                "inchi_version": "",
                "backend_tool": "Indigo",
                "timestamp": datetime.now().isoformat()
            }
        }

    if not inchi.startswith("InChI="):
        return {
            "svg_image": "",
            "success": False,
            "error_message": "Invalid InChI format: must start with 'InChI='",
            "metadata": {
                "inchi_version": "",
                "backend_tool": "Indigo",
                "timestamp": datetime.now().isoformat()
            }
        }

    # Simulate calling external service
    api_data = call_external_api("chembl-server-example_inchi2svg")

    # Construct the result with proper nested structure
    result = {
        "svg_image": api_data["svg_image"],
        "success": api_data["success"],
        "error_message": api_data["error_message"],
        "metadata": {
            "inchi_version": api_data["metadata_inchi_version"],
            "backend_tool": api_data["metadata_backend_tool"],
            "timestamp": api_data["metadata_timestamp"]
        }
    }

    return result