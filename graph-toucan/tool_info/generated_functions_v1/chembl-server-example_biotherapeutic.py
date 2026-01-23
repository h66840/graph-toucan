from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching biotherapeutic data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - results_0_mechanism_of_action (str): Mechanism of action for first biotherapeutic
        - results_0_target (str): Target protein or pathway for first entry
        - results_0_molecular_type (str): Molecular classification of first biotherapeutic
        - results_0_indications (str): Therapeutic indications for first entry
        - results_0_pharmacological_properties (str): Key pharmacological traits
        - results_1_mechanism_of_action (str): Mechanism of action for second biotherapeutic
        - results_1_target (str): Target protein or pathway for second entry
        - results_1_molecular_type (str): Molecular classification of second biotherapeutic
        - results_1_indications (str): Therapeutic indications for second entry
        - results_1_pharmacological_properties (str): Key pharmacological traits
        - count (int): Total number of biotherapeutic entries returned
        - biotherapeutic_type_fetched (str): The type of biotherapeutic queried
        - metadata_source_database_version (str): Version of the source database (e.g., ChEMBL)
        - metadata_timestamp (str): ISO format timestamp of data retrieval
        - metadata_warnings (str): Any warnings or notes about the response
    """
    return {
        "results_0_mechanism_of_action": "Inhibition of TNF-alpha",
        "results_0_target": "Tumor necrosis factor alpha (TNF-alpha)",
        "results_0_molecular_type": "Monoclonal antibody",
        "results_0_indications": "Rheumatoid arthritis, Crohn's disease",
        "results_0_pharmacological_properties": "High specificity, long half-life, immunomodulatory effects",
        "results_1_mechanism_of_action": "EGFR signaling blockade",
        "results_1_target": "Epidermal growth factor receptor (EGFR)",
        "results_1_molecular_type": "Fusion protein",
        "results_1_indications": "Non-small cell lung cancer, colorectal cancer",
        "results_1_pharmacological_properties": "Targeted therapy, reduced off-target effects",
        "count": 2,
        "biotherapeutic_type_fetched": "antibody",
        "metadata_source_database_version": "ChEMBL 32",
        "metadata_timestamp": "2023-10-15T14:30:00Z",
        "metadata_warnings": "Limited clinical trial data for rare indications"
    }

def chembl_server_example_biotherapeutic(biotherapeutic_type: str) -> Dict[str, Any]:
    """
    Get biotherapeutic data for the specified type.
    
    Args:
        biotherapeutic_type (str): Biotherapeutic type (e.g., 'antibody', 'fusion protein', 'gene therapy')
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of biotherapeutic data entries with detailed biological and pharmacological information
        - count (int): Total number of entries returned
        - biotherapeutic_type_fetched (str): The type of biotherapeutic that was queried
        - metadata (Dict): Contextual information including database version, timestamp, and warnings
    """
    if not biotherapeutic_type or not isinstance(biotherapeutic_type, str):
        raise ValueError("biotherapeutic_type must be a non-empty string")
    
    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_biotherapeutic")
    
    # Construct results list from indexed flat fields
    results = [
        {
            "mechanism_of_action": api_data["results_0_mechanism_of_action"],
            "target": api_data["results_0_target"],
            "molecular_type": api_data["results_0_molecular_type"],
            "indications": api_data["results_0_indications"],
            "pharmacological_properties": api_data["results_0_pharmacological_properties"]
        },
        {
            "mechanism_of_action": api_data["results_1_mechanism_of_action"],
            "target": api_data["results_1_target"],
            "molecular_type": api_data["results_1_molecular_type"],
            "indications": api_data["results_1_indications"],
            "pharmacological_properties": api_data["results_1_pharmacological_properties"]
        }
    ]
    
    # Construct metadata dictionary
    metadata = {
        "source_database_version": api_data["metadata_source_database_version"],
        "timestamp": api_data["metadata_timestamp"],
        "warnings": api_data["metadata_warnings"]
    }
    
    # Return structured response matching output schema
    return {
        "results": results,
        "count": api_data["count"],
        "biotherapeutic_type_fetched": biotherapeutic_type,
        "metadata": metadata
    }