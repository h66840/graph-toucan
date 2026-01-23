from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching drug warning data from an external API (e.g., ChEMBL server).
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - warning_0_drug_name (str): Name of the first drug associated with the MedDRA term
        - warning_0_adverse_event (str): Description of the first adverse event
        - warning_0_regulatory_source (str): Regulatory source for the first warning (e.g., EMA, FDA)
        - warning_0_meddra_pt (str): MedDRA Preferred Term for the first record
        - warning_0_meddra_soc (str): MedDRA System Organ Class for the first record
        - warning_1_drug_name (str): Name of the second drug associated with the MedDRA term
        - warning_1_adverse_event (str): Description of the second adverse event
        - warning_1_regulatory_source (str): Regulatory source for the second warning (e.g., EMA, FDA)
        - warning_1_meddra_pt (str): MedDRA Preferred Term for the second record
        - warning_1_meddra_soc (str): MedDRA System Organ Class for the second record
        - total_count (int): Total number of warnings retrieved
        - meddra_term_fetched (str): The MedDRA term that was queried
        - metadata_timestamp (str): ISO format timestamp of when the query was executed
        - metadata_data_source (str): Name of the data source (e.g., ChEMBL)
        - metadata_version (str): Version of the data source
    """
    return {
        "warning_0_drug_name": "Atorvastatin",
        "warning_0_adverse_event": "Hepatotoxicity observed in clinical trials",
        "warning_0_regulatory_source": "FDA",
        "warning_0_meddra_pt": "Hepatic enzyme increased",
        "warning_0_meddra_soc": "Hepatobiliary disorders",
        "warning_1_drug_name": "Simvastatin",
        "warning_1_adverse_event": "Risk of rhabdomyolysis with concomitant use of strong CYP3A4 inhibitors",
        "warning_1_regulatory_source": "EMA",
        "warning_1_meddra_pt": "Rhabdomyolysis",
        "warning_1_meddra_soc": "Musculoskeletal and connective tissue disorders",
        "total_count": 2,
        "meddra_term_fetched": "Hepatotoxicity",
        "metadata_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_data_source": "ChEMBL",
        "metadata_version": "32.0"
    }

def chembl_server_example_drug_warning(meddra_term: str) -> Dict[str, Any]:
    """
    Get drug warning data for the specified MedDRA term.
    
    This function retrieves drug safety warnings associated with a given MedDRA (Medical Dictionary for 
    Regulatory Activities) term. It returns detailed information about drugs, adverse events, regulatory 
    sources, and MedDRA classifications.
    
    Args:
        meddra_term (str): The MedDRA term to query for drug warnings (e.g., 'Hepatotoxicity')
        
    Returns:
        Dict containing:
        - warnings (List[Dict]): List of drug warning records with drug name, adverse event, 
          regulatory source, and MedDRA classification
        - total_count (int): Total number of warnings returned
        - meddra_term_fetched (str): The MedDRA term for which warnings were retrieved
        - metadata (Dict): Additional context including timestamp, data source, and version
        
    Raises:
        ValueError: If meddra_term is empty or not a string
    """
    if not meddra_term or not isinstance(meddra_term, str):
        raise ValueError("meddra_term must be a non-empty string")
    
    # Call simulated external API
    api_data = call_external_api("chembl-server-example_drug_warning")
    
    # Construct warnings list from indexed flat fields
    warnings = [
        {
            "drug_name": api_data["warning_0_drug_name"],
            "adverse_event": api_data["warning_0_adverse_event"],
            "regulatory_source": api_data["warning_0_regulatory_source"],
            "meddra_pt": api_data["warning_0_meddra_pt"],
            "meddra_soc": api_data["warning_0_meddra_soc"]
        },
        {
            "drug_name": api_data["warning_1_drug_name"],
            "adverse_event": api_data["warning_1_adverse_event"],
            "regulatory_source": api_data["warning_1_regulatory_source"],
            "meddra_pt": api_data["warning_1_meddra_pt"],
            "meddra_soc": api_data["warning_1_meddra_soc"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "data_source": api_data["metadata_data_source"],
        "version": api_data["metadata_version"]
    }
    
    # Build final result matching output schema
    result = {
        "warnings": warnings,
        "total_count": api_data["total_count"],
        "meddra_term_fetched": api_data["meddra_term_fetched"],
        "metadata": metadata
    }
    
    return result