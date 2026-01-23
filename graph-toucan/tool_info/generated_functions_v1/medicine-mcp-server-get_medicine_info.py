from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for medicine information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - medicinal_product (str): Name of the medicinal product as reported
        - indication (str): The medical condition or use for which the medicine is prescribed
        - reaction (str): Reported adverse drug reaction or side effect associated with the medicine
        - seriousness (str): Assessment of the seriousness of the reported reaction
        - report_date (str): Date of the report in YYYYMMDD format
    """
    return {
        "medicinal_product": "Aspirin",
        "indication": "Pain relief and fever reduction",
        "reaction": "Gastrointestinal bleeding",
        "seriousness": "Serious",
        "report_date": "20231015"
    }

def medicine_mcp_server_get_medicine_info(medicine_name: str) -> Dict[str, Any]:
    """
    Get information for a medicine.
    
    This function retrieves detailed information about a specified medicine,
    including its indication, any reported adverse reactions, the seriousness 
    of those reactions, and the date of the report.
    
    Args:
        medicine_name (str): The name of the medicine to retrieve information for.
        
    Returns:
        Dict[str, Any] with the following keys:
        - medicinal_product (str): Name of the medicinal product as reported
        - indication (Optional[str]): Medical condition or use for which the medicine is prescribed
        - reaction (Optional[str]): Reported adverse drug reaction or side effect
        - seriousness (Optional[str]): Assessment of the seriousness of the reaction
        - report_date (str): Date of the report in YYYYMMDD format
        
    Raises:
        ValueError: If medicine_name is empty or not a string
    """
    if not medicine_name or not isinstance(medicine_name, str):
        raise ValueError("medicine_name must be a non-empty string")
    
    # Call external API to get medicine information
    api_data = call_external_api("medicine-mcp-server-get_medicine_info")
    
    # Construct result dictionary matching output schema
    result = {
        "medicinal_product": api_data["medicinal_product"],
        "indication": api_data.get("indication"),
        "reaction": api_data.get("reaction"),
        "seriousness": api_data.get("seriousness"),
        "report_date": api_data["report_date"]
    }
    
    return result