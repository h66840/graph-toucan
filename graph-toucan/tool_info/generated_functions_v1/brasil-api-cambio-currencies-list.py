from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for currency information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - currency_0_code (str): First currency code (e.g., 'USD')
        - currency_0_name (str): First currency name (e.g., 'US Dollar')
        - currency_0_type (str): First currency type (e.g., 'Fiat')
        - currency_1_code (str): Second currency code (e.g., 'EUR')
        - currency_1_name (str): Second currency name (e.g., 'Euro')
        - currency_1_type (str): Second currency type (e.g., 'Fiat')
    """
    return {
        "currency_0_code": "USD",
        "currency_0_name": "US Dollar",
        "currency_0_type": "Fiat",
        "currency_1_code": "EUR",
        "currency_1_name": "Euro",
        "currency_1_type": "Fiat"
    }

def brasil_api_cambio_currencies_list() -> Dict[str, Any]:
    """
    Fetches and returns a list of all available currencies for exchange rates.
    
    This function simulates retrieving currency data from an external API by using
    a helper function that returns flat scalar values, then constructs the proper
    nested structure as defined in the output schema.
    
    Returns:
        Dict containing:
            - currencies (List[Dict]): List of currency objects with 'code', 'name', and 'type' fields
              Example:
              [
                {"code": "USD", "name": "US Dollar", "type": "Fiat"},
                {"code": "EUR", "name": "Euro", "type": "Fiat"}
              ]
    """
    try:
        # Fetch simulated API data with only flat fields
        api_data = call_external_api("brasil-api-cambio-currencies-list")
        
        # Construct the list of currency objects from flattened API response
        currencies = [
            {
                "code": api_data["currency_0_code"],
                "name": api_data["currency_0_name"],
                "type": api_data["currency_0_type"]
            },
            {
                "code": api_data["currency_1_code"],
                "name": api_data["currency_1_name"],
                "type": api_data["currency_1_type"]
            }
        ]
        
        return {"currencies": currencies}
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"An error occurred while processing currency data: {str(e)}") from e