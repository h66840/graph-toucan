from typing import Dict, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL ID description.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - description (str): Textual description of the ChEMBL entity
        - entity_type (str): Type of entity ('compound', 'target', 'assay')
        - chembl_id (str): The ChEMBL identifier
        - property_0_key (str): Key of first additional property
        - property_0_value (str): Value of first additional property
        - property_1_key (str): Key of second additional property
        - property_1_value (str): Value of second additional property
        - url (str): URL to the full ChEMBL page
        - last_updated (str): ISO 8601 timestamp of last update
    """
    return {
        "description": "A selective inhibitor of the BCR-ABL tyrosine kinase used in chronic myeloid leukemia treatment.",
        "entity_type": "compound",
        "chembl_id": "CHEMBL941",
        "property_0_key": "molecular_weight",
        "property_0_value": "429.89",
        "property_1_key": "mechanism_of_action",
        "property_1_value": "Tyrosine kinase inhibitor",
        "url": "https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL941/",
        "last_updated": "2023-10-15T08:23:19Z"
    }


def chembl_server_example_description_utils(chembl_id: str) -> Dict[str, Any]:
    """
    Get description information for the ChEMBL ID.

    Args:
        chembl_id (str): ChEMBL ID (e.g., 'CHEMBL941')

    Returns:
        Dict containing:
        - description (str): The textual description associated with the ChEMBL ID
        - entity_type (str): Type of entity described (e.g., 'compound', 'target', 'assay')
        - chembl_id (str): The ChEMBL identifier for which description is retrieved
        - properties (Dict): Key-value pairs of additional descriptive properties
        - url (str): A URL linking to the full ChEMBL database page for this ID
        - last_updated (str): Timestamp indicating when the description was last updated in ISO 8601 format

    Raises:
        ValueError: If chembl_id is empty or invalid
    """
    if not chembl_id or not isinstance(chembl_id, str) or not chembl_id.strip():
        raise ValueError("chembl_id must be a non-empty string")

    chembl_id = chembl_id.strip()

    # Call external API to get flat data
    api_data = call_external_api("chembl-server-example_description_utils")

    # Construct properties dictionary from flattened property fields
    properties = {}
    if api_data.get("property_0_key"):
        properties[api_data["property_0_key"]] = api_data["property_0_value"]
    if api_data.get("property_1_key"):
        properties[api_data["property_1_key"]] = api_data["property_1_value"]

    # Build result matching output schema
    result = {
        "description": api_data["description"],
        "entity_type": api_data["entity_type"],
        "chembl_id": api_data["chembl_id"],
        "properties": properties,
        "url": api_data["url"],
        "last_updated": api_data["last_updated"]
    }

    return result