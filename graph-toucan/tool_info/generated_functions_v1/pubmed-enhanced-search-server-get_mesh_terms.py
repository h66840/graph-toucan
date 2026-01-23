from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching MeSH terms from external PubMed API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Indicates whether the MeSH term search was successful
        - mesh_term_0 (str): First MeSH term related to the search word
        - mesh_term_1 (str): Second MeSH term related to the search word
    """
    return {
        "success": True,
        "mesh_term_0": "Diabetes Mellitus",
        "mesh_term_1": "Blood Glucose"
    }

def pubmed_enhanced_search_server_get_mesh_terms(search_word: str) -> Dict[str, Any]:
    """
    Get MeSH (Medical Subject Headings) terms related to a search word.
    
    This function queries the PubMed MeSH database to find relevant medical terminology
    that matches the provided search term. Useful for finding standardized medical terms.
    
    Parameters:
        search_word (str): The word or phrase to search for in the MeSH database.
        
    Returns:
        Dict[str, Any]: A dictionary containing success status and a list of MeSH terms.
            - success (bool): indicates whether the MeSH term search was successful
            - mesh_terms (List[str]): list of Medical Subject Headings (MeSH) terms returned by the PubMed database that are related to the input search word
    """
    # Input validation
    if not isinstance(search_word, str):
        return {
            "success": False,
            "mesh_terms": []
        }
    
    if not search_word.strip():
        return {
            "success": False,
            "mesh_terms": []
        }
    
    # Call external API to get flat response
    api_data = call_external_api("pubmed_enhanced_search_server_get_mesh_terms")
    
    # Construct the nested output structure from flat API data
    result = {
        "success": api_data["success"],
        "mesh_terms": [
            api_data["mesh_term_0"],
            api_data["mesh_term_1"]
        ]
    }
    
    return result