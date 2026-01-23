from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for paper matching.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if any occurred during processing
        - details_type (str): Type of error encountered
        - details_unrecognized_fields (str): Comma-separated list of unrecognized fields if applicable
    """
    return {
        "error": "",
        "details_type": "none",
        "details_unrecognized_fields": ""
    }

def ai_research_assistant_semantic_scholar_papers_match(
    title: str, 
    minCitations: Optional[int] = None, 
    openAccessOnly: Optional[bool] = None, 
    yearStart: Optional[int] = None, 
    yearEnd: Optional[int] = None
) -> Dict[str, Any]:
    """
    Find a paper by closest title match using Semantic Scholar.
    
    Args:
        title (str): Paper title to match (required)
        minCitations (int, optional): Minimum number of citations
        openAccessOnly (bool, optional): Only include open access papers
        yearStart (int, optional): Starting year for filtering (inclusive)
        yearEnd (int, optional): Ending year for filtering (inclusive)
    
    Returns:
        Dict containing:
        - error (str): error message describing the failure in processing the paper match request
        - details (Dict): contains additional error-related information such as 'type' of error or 'unrecognized_fields' if provided
    
    Raises:
        ValueError: If required title is not provided or empty
    """
    # Input validation
    if not title or not title.strip():
        return {
            "error": "Paper title is required",
            "details": {
                "type": "validation_error",
                "unrecognized_fields": ""
            }
        }
    
    # Validate year range if both are provided
    if yearStart is not None and yearEnd is not None and yearStart > yearEnd:
        return {
            "error": "Starting year cannot be greater than ending year",
            "details": {
                "type": "validation_error",
                "unrecognized_fields": ""
            }
        }
    
    # Call external API simulation
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-match")
    
    # Construct output structure from flat API response
    error = api_data["error"] if api_data["error"] else ""
    
    details = {
        "type": api_data["details_type"] if api_data["details_type"] != "none" else "",
        "unrecognized_fields": api_data["details_unrecognized_fields"]
    }
    
    return {
        "error": error,
        "details": details
    }