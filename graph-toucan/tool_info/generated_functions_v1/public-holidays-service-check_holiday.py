from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching holiday data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the holiday if the date is a public holiday
        - type (str): Type of holiday (e.g., National, Regional, Local)
        - location (str): Country or region where the holiday is observed
        - date (str): Date of the holiday in DD/MM/YYYY format
        - message (str): Informational message when no holiday is present
        - error (str): Error message if the API failed to retrieve data
    """
    # Simulate realistic responses based on inputs (not actually used in this mock)
    return {
        "name": "Independence Day",
        "type": "National",
        "location": "United States",
        "date": "04/07/2023",
        "message": "No holiday on this date.",
        "error": ""
    }

def public_holidays_service_check_holiday(country: str, day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Get holiday information for a given country and date.
    
    Args:
        country (str): The country to check for holidays
        day (int): Day of the month (1-31)
        month (int): Month of the year (1-12)
        year (int): Year in four-digit format (e.g., 2023)
    
    Returns:
        Dict containing holiday information with keys:
        - name (str): name of the holiday if the date is a public holiday
        - type (str): type of holiday (e.g., National, Regional, Local)
        - location (str): country or region where the holiday is observed
        - date (str): date of the holiday in DD/MM/YYYY format
        - message (str): informational message when no holiday is present
        - error (str): error message if the API failed to retrieve data
    
    Raises:
        ValueError: If day, month, or year are out of valid ranges
    """
    # Input validation
    if not (1 <= day <= 31):
        return {"error": "Invalid day: must be between 1 and 31", "message": ""}
    if not (1 <= month <= 12):
        return {"error": "Invalid month: must be between 1 and 12", "message": ""}
    if not (1000 <= year <= 9999):
        return {"error": "Invalid year: must be a four-digit number", "message": ""}
    
    # Call external API (mocked)
    api_data = call_external_api("public-holidays-service-check_holiday")
    
    # Construct result dictionary matching output schema
    result = {
        "name": api_data.get("name", ""),
        "type": api_data.get("type", ""),
        "location": api_data.get("location", ""),
        "date": api_data.get("date", f"{day:02d}/{month:02d}/{year}"),
        "message": api_data.get("message", ""),
        "error": api_data.get("error", "")
    }
    
    # Simulate some logic based on inputs (for realism)
    if country.lower() == "united states" and month == 7 and day == 4:
        result["name"] = "Independence Day"
        result["type"] = "National"
        result["location"] = "United States"
        result["date"] = f"{day:02d}/{month:02d}/{year}"
        result["message"] = ""
    elif country.lower() == "france" and month == 7 and day == 14:
        result["name"] = "Bastille Day"
        result["type"] = "National"
        result["location"] = "France"
        result["date"] = f"{day:02d}/{month:02d}/{year}"
        result["message"] = ""
    elif country.lower() == "japan" and month == 1 and day == 1:
        result["name"] = "New Year's Day"
        result["type"] = "National"
        result["location"] = "Japan"
        result["date"] = f"{day:02d}/{month:02d}/{year}"
        result["message"] = ""
    else:
        result["name"] = ""
        result["type"] = ""
        result["location"] = country
        result["date"] = f"{day:02d}/{month:02d}/{year}"
        result["message"] = "No holiday on this date."
        result["error"] = ""
    
    return result