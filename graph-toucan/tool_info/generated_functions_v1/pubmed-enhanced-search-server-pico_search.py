from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PICO-based PubMed search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Whether the search operation was successful
        - individual_P_query (str): Query string for Population terms
        - individual_P_count (int): Result count for Population search
        - individual_I_query (str): Query string for Intervention terms
        - individual_I_count (int): Result count for Intervention search
        - individual_C_query (str): Query string for Comparison terms
        - individual_C_count (int): Result count for Comparison search
        - individual_O_query (str): Query string for Outcome terms
        - individual_O_count (int): Result count for Outcome search
        - combination_P_AND_I_query (str): Query string for P AND I combination
        - combination_P_AND_I_count (int): Result count for P AND I combination
        - combination_P_AND_I_AND_C_query (str): Query string for P AND I AND C combination
        - combination_P_AND_I_AND_C_count (int): Result count for P AND I AND C combination
        - combination_P_AND_I_AND_O_query (str): Query string for P AND I AND O combination
        - combination_P_AND_I_AND_O_count (int): Result count for P AND I AND O combination
        - combination_P_AND_I_AND_C_AND_O_query (str): Query string for P AND I AND C AND O combination
        - combination_P_AND_I_AND_C_AND_O_count (int): Result count for P AND I AND C AND O combination
    """
    return {
        "success": True,
        "individual_P_query": "diabetes OR diabetic",
        "individual_P_count": 500000,
        "individual_I_query": "metformin OR insulin",
        "individual_I_count": 300000,
        "individual_C_query": "placebo OR control",
        "individual_C_count": 400000,
        "individual_O_query": "HbA1c reduction OR glycemic control",
        "individual_O_count": 200000,
        "combination_P_AND_I_query": "(diabetes OR diabetic) AND (metformin OR insulin)",
        "combination_P_AND_I_count": 150000,
        "combination_P_AND_I_AND_C_query": "(diabetes OR diabetic) AND (metformin OR insulin) AND (placebo OR control)",
        "combination_P_AND_I_AND_C_count": 75000,
        "combination_P_AND_I_AND_O_query": "(diabetes OR diabetic) AND (metformin OR insulin) AND (HbA1c reduction OR glycemic control)",
        "combination_P_AND_I_AND_O_count": 60000,
        "combination_P_AND_I_AND_C_AND_O_query": "(diabetes OR diabetic) AND (metformin OR insulin) AND (placebo OR control) AND (HbA1c reduction OR glycemic control)",
        "combination_P_AND_I_AND_C_AND_O_count": 30000
    }

def pubmed_enhanced_search_server_pico_search(
    p_terms: Optional[List[str]] = None,
    i_terms: Optional[List[str]] = None,
    c_terms: Optional[List[str]] = None,
    o_terms: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Perform PICO (Population, Intervention, Comparison, Outcome) based PubMed search with synonyms.
    
    This function takes lists of terms for each PICO element, combines them with OR within each element,
    and then performs various AND combinations between elements. Returns search queries and result counts.
    
    Parameters:
        p_terms (List[str], optional): Population terms/synonyms (at least 2 recommended)
        i_terms (List[str], optional): Intervention terms/synonyms (at least 2 recommended)
        c_terms (List[str], optional): Comparison terms/synonyms (optional, at least 2 recommended if provided)
        o_terms (List[str], optional): Outcome terms/synonyms (optional, at least 2 recommended if provided)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - success (bool): whether the search operation was successful
            - results (Dict): contains 'individual' and 'combinations' search results with queries and counts
                - individual (Dict): individual PICO element searches, keyed by element label ('P', 'I', 'C', 'O')
                - combinations (Dict): combined PICO searches (e.g., P_AND_I, P_AND_I_AND_C)
    """
    # Input validation
    if not p_terms or len(p_terms) < 2:
        return {"success": False, "results": {"individual": {}, "combinations": {}}}
    if not i_terms or len(i_terms) < 2:
        return {"success": False, "results": {"individual": {}, "combinations": {}}}

    # Call external API (simulated)
    api_data = call_external_api("pubmed-enhanced-search-server-pico_search")

    # Construct individual results
    individual = {}
    if p_terms:
        individual["P"] = {
            "query": api_data["individual_P_query"],
            "count": api_data["individual_P_count"]
        }
    if i_terms:
        individual["I"] = {
            "query": api_data["individual_I_query"],
            "count": api_data["individual_I_count"]
        }
    if c_terms:
        individual["C"] = {
            "query": api_data["individual_C_query"],
            "count": api_data["individual_C_count"]
        }
    if o_terms:
        individual["O"] = {
            "query": api_data["individual_O_query"],
            "count": api_data["individual_O_count"]
        }

    # Construct combination results
    combinations = {}
    combinations["P_AND_I"] = {
        "query": api_data["combination_P_AND_I_query"],
        "count": api_data["combination_P_AND_I_count"]
    }
    
    if c_terms:
        combinations["P_AND_I_AND_C"] = {
            "query": api_data["combination_P_AND_I_AND_C_query"],
            "count": api_data["combination_P_AND_I_AND_C_count"]
        }
    
    if o_terms:
        combinations["P_AND_I_AND_O"] = {
            "query": api_data["combination_P_AND_I_AND_O_query"],
            "count": api_data["combination_P_AND_I_AND_O_count"]
        }
    
    if c_terms and o_terms:
        combinations["P_AND_I_AND_C_AND_O"] = {
            "query": api_data["combination_P_AND_I_AND_C_AND_O_query"],
            "count": api_data["combination_P_AND_I_AND_C_AND_O_count"]
        }

    # Build final result
    result = {
        "success": api_data["success"],
        "results": {
            "individual": individual,
            "combinations": combinations
        }
    }

    return result