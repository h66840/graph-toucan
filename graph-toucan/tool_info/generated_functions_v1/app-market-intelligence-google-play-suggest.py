from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play search suggestions.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - suggestion_0 (str): First suggested search term
        - suggestion_1 (str): Second suggested search term
        - suggestion_2 (str): Third suggested search term
        - suggestion_3 (str): Fourth suggested search term
        - suggestion_4 (str): Fifth suggested search term
        - metadata_country (str): Country code used for fetching suggestions
        - metadata_lang (str): Language code used for fetching suggestions
    """
    return {
        "suggestion_0": "panda pop",
        "suggestion_1": "panda",
        "suggestion_2": "panda games",
        "suggestion_3": "panda run",
        "suggestion_4": "panda pop for free",
        "metadata_country": "us",
        "metadata_lang": "en"
    }

def app_market_intelligence_google_play_suggest(
    term: str,
    country: Optional[str] = "us",
    lang: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get search suggestions from Google Play based on a given search term.
    
    Args:
        term (str): Search term to get suggestions for (e.g., 'panda'). Required.
        country (Optional[str]): Country code to get suggestions from (default: 'us').
        lang (Optional[str]): Language code for suggestions (default: 'en').
    
    Returns:
        Dict containing:
        - suggestions (List[str]): List of suggested search terms from Google Play based on the input term, typically up to 5 results.
        - metadata (Dict): Additional context about the response, such as country and language used for fetching suggestions.
    
    Raises:
        ValueError: If the required 'term' parameter is empty or None.
    """
    if not term:
        raise ValueError("The 'term' parameter is required and cannot be empty.")
    
    # Call the external API simulation
    api_data = call_external_api("app-market-intelligence-google-play-suggest")
    
    # Construct the suggestions list from indexed fields
    suggestions: List[str] = []
    for i in range(5):
        suggestion_key = f"suggestion_{i}"
        if suggestion_key in api_data and isinstance(api_data[suggestion_key], str):
            suggestions.append(api_data[suggestion_key])
    
    # Construct metadata
    metadata = {
        "country": api_data.get("metadata_country", country),
        "lang": api_data.get("metadata_lang", lang)
    }
    
    return {
        "suggestions": suggestions,
        "metadata": metadata
    }