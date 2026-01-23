from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - currency_0_code (str): First supported currency code (three-letter)
        - currency_0_name (str): Full name of the first currency
        - currency_1_code (str): Second supported currency code (three-letter)
        - currency_1_name (str): Full name of the second currency
        - currency_2_code (str): Third supported currency code (three-letter)
        - currency_2_name (str): Full name of the third currency
        - currency_3_code (str): Fourth supported currency code (three-letter)
        - currency_3_name (str): Full name of the fourth currency
        - currency_4_code (str): Fifth supported currency code (three-letter)
        - currency_4_name (str): Full name of the fifth currency
    """
    return {
        "currency_0_code": "USD",
        "currency_0_name": "United States Dollar",
        "currency_1_code": "EUR",
        "currency_1_name": "Euro",
        "currency_2_code": "JPY",
        "currency_2_name": "Japanese Yen",
        "currency_3_code": "GBP",
        "currency_3_name": "British Pound Sterling",
        "currency_4_code": "CAD",
        "currency_4_name": "Canadian Dollar"
    }

def frankfurtermcp_get_supported_currencies() -> Dict[str, Dict[str, str]]:
    """
    Returns a dictionary mapping three-letter currency codes to their full names
    for the supported currencies.
    
    This function queries an external API (simulated) to retrieve supported currency
    information and formats it into a dictionary structure.
    
    Returns:
        Dict[str, str]: A dictionary where keys are three-letter currency codes (e.g., "USD")
                       and values are the full names of the currencies (e.g., "United States Dollar").
                       Example:
                       {
                           "USD": "United States Dollar",
                           "EUR": "Euro",
                           ...
                       }
    
    Raises:
        KeyError: If expected fields are missing from the API response
        Exception: If any unexpected error occurs during processing
    """
    try:
        api_data = call_external_api("frankfurtermcp-get_supported_currencies")
        
        currencies = {}
        
        # Extract 5 currencies from flattened API response
        for i in range(5):
            code_key = f"currency_{i}_code"
            name_key = f"currency_{i}_name"
            
            if code_key in api_data and name_key in api_data:
                currency_code = api_data[code_key]
                currency_name = api_data[name_key]
                
                if isinstance(currency_code, str) and isinstance(currency_name, str):
                    currencies[currency_code] = currency_name
        
        return {"currencies": currencies}
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise Exception(f"Failed to retrieve supported currencies: {e}")