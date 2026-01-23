from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching binding site data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - binding_sites_0_site_id (str): Unique identifier for the first binding site
        - binding_sites_0_site_name (str): Name of the first binding site
        - binding_sites_0_target_id (str): Target ID for the first binding site
        - binding_sites_0_target_name (str): Target name for the first binding site
        - binding_sites_0_organism (str): Organism for the first binding site
        - binding_sites_0_value (float): Binding affinity value for the first site
        - binding_sites_0_unit (str): Unit of binding affinity for the first site
        - binding_sites_0_type (str): Type of measurement for the first site
        - binding_sites_0_residues_0 (str): First residue of the first binding site
        - binding_sites_0_residues_1 (str): Second residue of the first binding site
        - binding_sites_0_description (str): Description of the first binding site
        - binding_sites_0_metadata_source (str): Data source for the first site
        - binding_sites_0_metadata_chembl_id (str): ChEMBL ID for the first site
        - binding_sites_0_metadata_updated (str): Update timestamp for the first site
        - binding_sites_1_site_id (str): Unique identifier for the second binding site
        - binding_sites_1_site_name (str): Name of the second binding site
        - binding_sites_1_target_id (str): Target ID for the second binding site
        - binding_sites_1_target_name (str): Target name for the second binding site
        - binding_sites_1_organism (str): Organism for the second binding site
        - binding_sites_1_value (float): Binding affinity value for the second site
        - binding_sites_1_unit (str): Unit of binding affinity for the second site
        - binding_sites_1_type (str): Type of measurement for the second site
        - binding_sites_1_residues_0 (str): First residue of the second binding site
        - binding_sites_1_residues_1 (str): Second residue of the second binding site
        - binding_sites_1_description (str): Description of the second binding site
        - binding_sites_1_metadata_source (str): Data source for the second site
        - binding_sites_1_metadata_chembl_id (str): ChEMBL ID for the second site
        - binding_sites_1_metadata_updated (str): Update timestamp for the second site
        - total_count (int): Total number of binding sites returned
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed (empty if success)
    """
    return {
        "binding_sites_0_site_id": "BS001",
        "binding_sites_0_site_name": "Catalytic Site",
        "binding_sites_0_target_id": "CHEMBL1234",
        "binding_sites_0_target_name": "Serine Protease",
        "binding_sites_0_organism": "Homo sapiens",
        "binding_sites_0_value": 12.5,
        "binding_sites_0_unit": "nM",
        "binding_sites_0_type": "Ki",
        "binding_sites_0_residues_0": "HIS57",
        "binding_sites_0_residues_1": "ASP102",
        "binding_sites_0_description": "Catalytic triad involved in peptide bond hydrolysis",
        "binding_sites_0_metadata_source": "ChEMBL",
        "binding_sites_0_metadata_chembl_id": "CHEMBLBS1001",
        "binding_sites_0_metadata_updated": "2023-10-01",
        
        "binding_sites_1_site_id": "BS002",
        "binding_sites_1_site_name": "Allosteric Site",
        "binding_sites_1_target_id": "CHEMBL5678",
        "binding_sites_1_target_name": "Kinase Inhibitor Target",
        "binding_sites_1_organism": "Mus musculus",
        "binding_sites_1_value": 850.0,
        "binding_sites_1_unit": "nM",
        "binding_sites_1_type": "IC50",
        "binding_sites_1_residues_0": "GLU98",
        "binding_sites_1_residues_1": "LYS105",
        "binding_sites_1_description": "Allosteric regulatory site modulating kinase activity",
        "binding_sites_1_metadata_source": "ChEMBL",
        "binding_sites_1_metadata_chembl_id": "CHEMBLBS1002",
        "binding_sites_1_metadata_updated": "2023-09-15",
        
        "total_count": 2,
        "success": True,
        "error_message": ""
    }

def chembl_server_example_binding_site(site_name: str) -> Dict[str, Any]:
    """
    Get binding site data for the specified name.
    
    Args:
        site_name (str): Binding site name to query
        
    Returns:
        Dict containing:
        - binding_sites (List[Dict]): List of binding site entries with detailed information
        - total_count (int): Total number of binding sites returned
        - success (bool): Whether the request was processed successfully
        - error_message (str): Optional error description if request failed
        
        Each binding site dict contains:
        - site_id (str): Unique identifier for the binding site
        - site_name (str): Name of the binding site
        - target_id (str): Identifier of the biological target
        - target_name (str): Name of the biological target
        - organism (str): Organism from which the target is derived
        - binding_affinity (Dict): Binding affinity data with value, unit, and type
        - residues (List[str]): List of amino acid residues involved
        - description (str): Textual description of the binding site
        - metadata (Dict): Additional structured information including source, ChEMBL ID, and update timestamp
    """
    # Input validation
    if not site_name or not isinstance(site_name, str):
        return {
            "binding_sites": [],
            "total_count": 0,
            "success": False,
            "error_message": "Invalid site_name: must be a non-empty string"
        }
    
    try:
        # Call external API to get flattened data
        api_data = call_external_api("chembl-server-example_binding_site")
        
        # Construct binding affinity data for first site
        binding_affinity_0 = {
            "value": api_data["binding_sites_0_value"],
            "unit": api_data["binding_sites_0_unit"],
            "type": api_data["binding_sites_0_type"]
        }
        
        # Construct residues list for first site
        residues_0 = [
            api_data["binding_sites_0_residues_0"],
            api_data["binding_sites_0_residues_1"]
        ]
        
        # Construct metadata for first site
        metadata_0 = {
            "source": api_data["binding_sites_0_metadata_source"],
            "chembl_id": api_data["binding_sites_0_metadata_chembl_id"],
            "updated": api_data["binding_sites_0_metadata_updated"]
        }
        
        # Construct first binding site
        site_0 = {
            "site_id": api_data["binding_sites_0_site_id"],
            "site_name": api_data["binding_sites_0_site_name"],
            "target_id": api_data["binding_sites_0_target_id"],
            "target_name": api_data["binding_sites_0_target_name"],
            "organism": api_data["binding_sites_0_organism"],
            "binding_affinity": binding_affinity_0,
            "residues": residues_0,
            "description": api_data["binding_sites_0_description"],
            "metadata": metadata_0
        }
        
        # Construct binding affinity data for second site
        binding_affinity_1 = {
            "value": api_data["binding_sites_1_value"],
            "unit": api_data["binding_sites_1_unit"],
            "type": api_data["binding_sites_1_type"]
        }
        
        # Construct residues list for second site
        residues_1 = [
            api_data["binding_sites_1_residues_0"],
            api_data["binding_sites_1_residues_1"]
        ]
        
        # Construct metadata for second site
        metadata_1 = {
            "source": api_data["binding_sites_1_metadata_source"],
            "chembl_id": api_data["binding_sites_1_metadata_chembl_id"],
            "updated": api_data["binding_sites_1_metadata_updated"]
        }
        
        # Construct second binding site
        site_1 = {
            "site_id": api_data["binding_sites_1_site_id"],
            "site_name": api_data["binding_sites_1_site_name"],
            "target_id": api_data["binding_sites_1_target_id"],
            "target_name": api_data["binding_sites_1_target_name"],
            "organism": api_data["binding_sites_1_organism"],
            "binding_affinity": binding_affinity_1,
            "residues": residues_1,
            "description": api_data["binding_sites_1_description"],
            "metadata": metadata_1
        }
        
        # Return structured response
        return {
            "binding_sites": [site_0, site_1],
            "total_count": api_data["total_count"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
    except Exception as e:
        return {
            "binding_sites": [],
            "total_count": 0,
            "success": False,
            "error_message": f"Failed to process binding site data: {str(e)}"
        }