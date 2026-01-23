from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for skincare selfie analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - analysis_result (str): Result of the skin condition analysis, e.g., "피부좋음", "건조함", "트러블 있음"
    """
    return {
        "analysis_result": "피부좋음"
    }

def skincare_get_selfie_analysis(imageUrl: str) -> Dict[str, Any]:
    """
    Analyzes a selfie image from the given URL and returns the skin condition analysis result.
    
    This function simulates calling an external skincare analysis service.
    It takes an image URL, validates it, and returns a simulated analysis result.
    
    Args:
        imageUrl (str): The URL of the image to analyze. Required.
    
    Returns:
        Dict[str, Any]: A dictionary containing the analysis result with the following structure:
            - analysis_result (str): Description of the skin condition (e.g., "피부좋음", "건조함", "트러블 있음")
    
    Raises:
        ValueError: If imageUrl is empty or not a string
    """
    # Input validation
    if not isinstance(imageUrl, str):
        raise ValueError("imageUrl must be a string")
    if not imageUrl.strip():
        raise ValueError("imageUrl is required and cannot be empty")
    
    # Call external API simulation
    api_data = call_external_api("skincare-get-selfie-analysis")
    
    # Construct result matching output schema
    result = {
        "analysis_result": api_data["analysis_result"]
    }
    
    return result