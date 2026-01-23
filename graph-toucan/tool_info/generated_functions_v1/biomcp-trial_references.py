from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for clinical trial references.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - reference_0_citation (str): Citation for the first reference
        - reference_0_pmid (str): PubMed ID for the first reference
        - reference_0_type (str): Type of the first reference (e.g., primary_result)
        - reference_0_doi (str): DOI for the first reference (optional)
        - reference_1_citation (str): Citation for the second reference
        - reference_1_pmid (str): PubMed ID for the second reference
        - reference_1_type (str): Type of the second reference
        - reference_1_doi (str): DOI for the second reference (optional)
        - nct_id (str): The NCT ID for which references were retrieved
        - has_results (bool): Whether any references were found
        - error (str): Error message if retrieval failed; empty if successful
        - source (str): Source of the data
        - fetched_at (str): ISO 8601 timestamp when data was retrieved
    """
    return {
        "reference_0_citation": "Smith J et al. Efficacy of Drug X in Treating Y. N Engl J Med. 2023;388(5):456-467.",
        "reference_0_pmid": "12345678",
        "reference_0_type": "primary_result",
        "reference_0_doi": "10.1056/nejmoa1234567",
        "reference_1_citation": "Johnson A et al. Long-term Outcomes of Trial Z. Lancet. 2024;400(10350):234-245.",
        "reference_1_pmid": "12345679",
        "reference_1_type": "secondary_publication",
        "reference_1_doi": "10.1016/s0140-6736(23)00123-4",
        "nct_id": "NCT04280705",
        "has_results": True,
        "error": "",
        "source": "ClinicalTrials.gov v2 API",
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }

def biomcp_trial_references(call_benefit: str, nct_id: str) -> Dict[str, Any]:
    """
    Retrieves publications and other references associated with a single clinical trial identified by its NCT ID.
    
    This function simulates calling an external API to fetch the ReferencesModule from ClinicalTrials.gov v2 API.
    It returns a structured response containing citation details, PMIDs, reference types, DOIs, and metadata.
    
    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        nct_id (str): A single NCT ID (e.g., "NCT04280705")
    
    Returns:
        Dict with the following keys:
        - references (List[Dict]): List of reference entries with keys 'citation', 'pmid', 'type', and 'doi'
        - nct_id (str): The NCT ID for which references were retrieved
        - has_results (bool): Indicates whether any references were found
        - error (str): Error message if retrieval failed; empty if successful
        - source (str): Source of the data
        - fetched_at (str): ISO 8601 timestamp indicating when the data was retrieved
    """
    # Input validation
    if not call_benefit.strip():
        return {
            "references": [],
            "nct_id": nct_id,
            "has_results": False,
            "error": "call_benefit is required and cannot be empty",
            "source": "ClinicalTrials.gov v2 API",
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        }
    
    if not nct_id or not nct_id.startswith("NCT") or len(nct_id) < 11:
        return {
            "references": [],
            "nct_id": nct_id,
            "has_results": False,
            "error": "Invalid NCT ID format. Must start with 'NCT' and be followed by digits (e.g., NCT0123456789)",
            "source": "ClinicalTrials.gov v2 API",
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        }

    # Call simulated external API
    try:
        api_data = call_external_api("biomcp-trial_references")
        
        # Construct references list from indexed fields
        references: List[Dict[str, Optional[str]]] = []
        
        for i in range(2):  # Two references as per simulation
            citation_key = f"reference_{i}_citation"
            pmid_key = f"reference_{i}_pmid"
            type_key = f"reference_{i}_type"
            doi_key = f"reference_{i}_doi"
            
            if citation_key in api_data and api_data[citation_key]:
                references.append({
                    "citation": api_data[citation_key],
                    "pmid": api_data.get(pmid_key, ""),
                    "type": api_data.get(type_key, ""),
                    "doi": api_data.get(doi_key, "")
                })
        
        # Build final result structure
        result = {
            "references": references,
            "nct_id": api_data["nct_id"],
            "has_results": api_data["has_results"],
            "error": api_data["error"],
            "source": api_data["source"],
            "fetched_at": api_data["fetched_at"]
        }
        
        return result
        
    except Exception as e:
        return {
            "references": [],
            "nct_id": nct_id,
            "has_results": False,
            "error": f"Failed to retrieve references: {str(e)}",
            "source": "ClinicalTrials.gov v2 API",
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        }