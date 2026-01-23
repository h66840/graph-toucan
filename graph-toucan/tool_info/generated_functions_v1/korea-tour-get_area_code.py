from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Korea tour area code information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - area_0_code (str): First area code
        - area_0_name (str): First area name
        - area_1_code (str): Second area code
        - area_1_name (str): Second area name
        - error (str): Error message if any occurred
    """
    return {
        "area_0_code": "1",
        "area_0_name": "서울",
        "area_1_code": "2",
        "area_1_name": "부산",
        "error": ""
    }

def korea_tour_get_area_code(areaCode: Optional[str] = None) -> Dict[str, Any]:
    """
    한국의 지역코드를 조회합니다. 상위 지역코드를 입력하면 하위 지역 목록을 반환하고, 
    입력하지 않으면 광역시/도 목록을 반환합니다.
    
    Args:
        areaCode (Optional[str]): 상위 지역코드 (선택)
    
    Returns:
        Dict containing list of area information with code and name, or error message.
        The structure matches the expected output schema:
        {
            "error": str,
            "areas": [
                {"code": str, "name": str},
                {"code": str, "name": str}
            ]
        }
        Note: In case of error, areas list will be empty.
    """
    try:
        # Validate input type if provided
        if areaCode is not None and not isinstance(areaCode, str):
            return {
                "error": "areaCode must be a string if provided"
            }
        
        # Call external API to get data (simulated)
        api_data = call_external_api("korea-tour-get_area_code")
        
        # Check for errors from API
        if api_data.get("error"):
            return {"error": api_data["error"]}
        
        # Construct areas list from flattened API response
        areas = []
        for i in range(2):  # We expect 2 items as per implementation instructions
            code_key = f"area_{i}_code"
            name_key = f"area_{i}_name"
            if code_key in api_data and name_key in api_data:
                areas.append({
                    "code": api_data[code_key],
                    "name": api_data[name_key]
                })
        
        return {
            "error": "",
            "areas": areas
        }
        
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }