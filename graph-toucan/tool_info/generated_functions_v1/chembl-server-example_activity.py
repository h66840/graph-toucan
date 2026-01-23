from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL activity data.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - activity_0_activity_id (int): Unique identifier for the activity
        - activity_0_assay_chembl_id (str): ChEMBL ID of the assay
        - activity_0_assay_description (str): Description of the assay
        - activity_0_assay_type (str): Type of the assay
        - activity_0_target_chembl_id (str): ChEMBL ID of the target
        - activity_0_target_organism (str): Organism of the target
        - activity_0_target_pref_name (str): Preferred name of the target
        - activity_0_molecule_chembl_id (str): ChEMBL ID of the molecule
        - activity_0_molecule_pref_name (str): Preferred name of the molecule
        - activity_0_canonical_smiles (str): Canonical SMILES representation
        - activity_0_standard_type (str): Standard type of measurement
        - activity_0_standard_value (float): Standardized activity value
        - activity_0_standard_units (str): Units of the standard value
        - activity_0_standard_relation (str): Relation operator for the value
        - activity_0_pchembl_value (float): pChEMBL value (negative log of activity)
        - activity_0_data_validity_comment (str): Comment on data validity
        - activity_0_data_validity_description (str): Description of data validity
        - activity_0_document_chembl_id (str): ChEMBL ID of the source document
        - activity_0_document_year (int): Year of publication
        - activity_0_document_journal (str): Journal name
        - activity_0_ligand_efficiency_le (float): Ligand efficiency (LE)
        - activity_0_ligand_efficiency_lei (float): Ligand efficiency index (LEI)
        - activity_0_ligand_efficiency_lle (float): Lipophilic ligand efficiency (LLE)
        - activity_0_ligand_efficiency_bei (float): Binding efficiency index (BEI)
        - activity_0_potential_duplicate (bool): Whether the activity is a potential duplicate
        - activity_0_relation (str): Relation operator
        - activity_0_value (float): Numerical value of the activity
        - activity_0_units (str): Units of the activity value
        - activity_0_type (str): Type of activity
        - activity_0_bao_endpoint (str): BioAssay Ontology endpoint ID
        - activity_0_bao_format (str): BioAssay Ontology format ID
        - activity_0_bao_label (str): BioAssay Ontology label
        - activity_0_qudt_units (str): QUDT units URI
        - activity_0_uo_units (str): UO units URI
        - activity_0_record_id (int): Record identifier
        - activity_0_src_id (int): Source identifier
        - activity_0_action_type (str): Type of action
        - activity_0_activity_comment (str): Comment on the activity
        - activity_0_standard_text_value (str): Textual representation of standard value
        - activity_0_standard_upper_value (float): Upper bound of standard value
        - activity_0_text_value (str): Textual value
        - activity_0_toid (int): TOID (target-organism identifier)
        - activity_0_upper_value (float): Upper bound of the value
        - activity_0_activity_properties_0_property (str): Name of the first activity property
        - activity_0_activity_properties_0_value (str): Value of the first activity property
        - activity_0_activity_properties_0_description (str): Description of the first activity property
        - activity_0_assay_variant_accession (str): Assay variant accession number
        - activity_0_assay_variant_mutation (str): Mutation in the assay variant
        - activity_0_parent_molecule_chembl_id (str): ChEMBL ID of the parent molecule
    """
    return {
        "activity_0_activity_id": 123456,
        "activity_0_assay_chembl_id": "CHEMBL1234",
        "activity_0_assay_description": "In vitro assay measuring inhibition of kinase activity",
        "activity_0_assay_type": "B",
        "activity_0_target_chembl_id": "CHEMBL5678",
        "activity_0_target_organism": "Homo sapiens",
        "activity_0_target_pref_name": "Mitogen-activated protein kinase 1",
        "activity_0_molecule_chembl_id": "CHEMBL9876",
        "activity_0_molecule_pref_name": "Example Molecule A",
        "activity_0_canonical_smiles": "CCOc1ccc(cc1)S(=O)(=O)Nc2ccc(cc2)C(=O)O",
        "activity_0_standard_type": "IC50",
        "activity_0_standard_value": 85.2,
        "activity_0_standard_units": "nM",
        "activity_0_standard_relation": "<",
        "activity_0_pchembl_value": 7.8,
        "activity_0_data_validity_comment": "Manually validated",
        "activity_0_data_validity_description": "Data is consistent with experimental conditions",
        "activity_0_document_chembl_id": "CHEMBLDOC98765",
        "activity_0_document_year": 2020,
        "activity_0_document_journal": "Journal of Medicinal Chemistry",
        "activity_0_ligand_efficiency_le": 0.32,
        "activity_0_ligand_efficiency_lei": 10.5,
        "activity_0_ligand_efficiency_lle": 5.4,
        "activity_0_ligand_efficiency_bei": 12.1,
        "activity_0_potential_duplicate": False,
        "activity_0_relation": "=",
        "activity_0_value": 85.2,
        "activity_0_units": "nM",
        "activity_0_type": "IC50",
        "activity_0_bao_endpoint": "BAO_0000184",
        "activity_0_bao_format": "BAO_0000015",
        "activity_0_bao_label": "in vitro",
        "activity_0_qudt_units": "http://qudt.org/vocab/unit#NanoM",
        "activity_0_uo_units": "http://purl.obolibrary.org/obo/UO_0000062",
        "activity_0_record_id": 987654,
        "activity_0_src_id": 1,
        "activity_0_action_type": "INHIBITOR",
        "activity_0_activity_comment": "High potency observed",
        "activity_0_standard_text_value": None,
        "activity_0_standard_upper_value": None,
        "activity_0_text_value": None,
        "activity_0_toid": 45678,
        "activity_0_upper_value": None,
        "activity_0_activity_properties_0_property": "Solubility",
        "activity_0_activity_properties_0_value": "-4.5",
        "activity_0_activity_properties_0_description": "Log solubility in mol/L",
        "activity_0_assay_variant_accession": "VAR_001234",
        "activity_0_assay_variant_mutation": "L858R",
        "activity_0_parent_molecule_chembl_id": "CHEMBL9876"
    }

def chembl_server_example_activity(assay_chembl_id: str) -> List[Dict[str, Any]]:
    """
    Get activity data for the specified assay_chembl_id.
    
    This function retrieves activity data associated with a given ChEMBL assay ID.
    It simulates querying an external ChEMBL server and returns structured activity records.
    
    Args:
        assay_chembl_id (str): ChEMBL assay ID (required)
        
    Returns:
        List[Dict]: List of activity data records. Each record contains fields such as:
            - activity_id (int)
            - assay_chembl_id (str)
            - assay_description (str)
            - assay_type (str)
            - target_chembl_id (str)
            - target_organism (str)
            - target_pref_name (str)
            - molecule_chembl_id (str)
            - molecule_pref_name (str)
            - canonical_smiles (str)
            - standard_type (str)
            - standard_value (float)
            - standard_units (str)
            - standard_relation (str)
            - pchembl_value (float)
            - data_validity_comment (str)
            - data_validity_description (str)
            - document_chembl_id (str)
            - document_year (int)
            - document_journal (str)
            - ligand_efficiency (dict with keys: le, lei, lle, bei)
            - potential_duplicate (bool)
            - relation (str)
            - value (float)
            - units (str)
            - type (str)
            - bao_endpoint (str)
            - bao_format (str)
            - bao_label (str)
            - qudt_units (str)
            - uo_units (str)
            - record_id (int)
            - src_id (int)
            - action_type (str)
            - activity_comment (str)
            - activity_properties (List[Dict])
            - assay_variant_accession (str)
            - assay_variant_mutation (str)
            - parent_molecule_chembl_id (str)
            - standard_text_value (Optional[str])
            - standard_upper_value (Optional[float])
            - text_value (Optional[str])
            - toid (int)
            - upper_value (Optional[float])
            
    Raises:
        ValueError: If assay_chembl_id is empty or not a string
    """
    # Input validation
    if not assay_chembl_id:
        raise ValueError("assay_chembl_id is required")
    if not isinstance(assay_chembl_id, str):
        raise ValueError("assay_chembl_id must be a string")
    
    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_activity")
    
    # Construct activity properties list
    activity_properties = [
        {
            "property": api_data["activity_0_activity_properties_0_property"],
            "value": api_data["activity_0_activity_properties_0_value"],
            "description": api_data["activity_0_activity_properties_0_description"]
        }
    ]
    
    # Construct ligand efficiency dict
    ligand_efficiency = {
        "le": api_data["activity_0_ligand_efficiency_le"],
        "lei": api_data["activity_0_ligand_efficiency_lei"],
        "lle": api_data["activity_0_ligand_efficiency_lle"],
        "bei": api_data["activity_0_ligand_efficiency_bei"]
    }
    
    # Construct the full activity record
    activity_record = {
        "activity_id": api_data["activity_0_activity_id"],
        "assay_chembl_id": api_data["activity_0_assay_chembl_id"],
        "assay_description": api_data["activity_0_assay_description"],
        "assay_type": api_data["activity_0_assay_type"],
        "target_chembl_id": api_data["activity_0_target_chembl_id"],
        "target_organism": api_data["activity_0_target_organism"],
        "target_pref_name": api_data["activity_0_target_pref_name"],
        "molecule_chembl_id": api_data["activity_0_molecule_chembl_id"],
        "molecule_pref_name": api_data["activity_0_molecule_pref_name"],
        "canonical_smiles": api_data["activity_0_canonical_smiles"],
        "standard_type": api_data["activity_0_standard_type"],
        "standard_value": api_data["activity_0_standard_value"],
        "standard_units": api_data["activity_0_standard_units"],
        "standard_relation": api_data["activity_0_standard_relation"],
        "pchembl_value": api_data["activity_0_pchembl_value"],
        "data_validity_comment": api_data["activity_0_data_validity_comment"],
        "data_validity_description": api_data["activity_0_data_validity_description"],
        "document_chembl_id": api_data["activity_0_document_chembl_id"],
        "document_year": api_data["activity_0_document_year"],
        "document_journal": api_data["activity_0_document_journal"],
        "ligand_efficiency": ligand_efficiency,
        "potential_duplicate": api_data["activity_0_potential_duplicate"],
        "relation": api_data["activity_0_relation"],
        "value": api_data["activity_0_value"],
        "units": api_data["activity_0_units"],
        "type": api_data["activity_0_type"],
        "bao_endpoint": api_data["activity_0_bao_endpoint"],
        "bao_format": api_data["activity_0_bao_format"],
        "bao_label": api_data["activity_0_bao_label"],
        "qudt_units": api_data["activity_0_qudt_units"],
        "uo_units": api_data["activity_0_uo_units"],
        "record_id": api_data["activity_0_record_id"],
        "src_id": api_data["activity_0_src_id"],
        "action_type": api_data["activity_0_action_type"],
        "activity_comment": api_data["activity_0_activity_comment"],
        "activity_properties": activity_properties,
        "assay_variant_accession": api_data["activity_0_assay_variant_accession"],
        "assay_variant_mutation": api_data["activity_0_assay_variant_mutation"],
        "parent_molecule_chembl_id": api_data["activity_0_parent_molecule_chembl_id"],
        "standard_text_value": api_data["activity_0_standard_text_value"],
        "standard_upper_value": api_data["activity_0_standard_upper_value"],
        "text_value": api_data["activity_0_text_value"],
        "toid": api_data["activity_0_toid"],
        "upper_value": api_data["activity_0_upper_value"]
    }
    
    # Return list of activities (simulated single result)
    return [activity_record]