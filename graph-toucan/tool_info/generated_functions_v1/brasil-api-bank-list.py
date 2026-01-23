from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian bank list.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - bank_0_code (int): First bank's code
        - bank_0_name (str): First bank's name
        - bank_0_ispb (str): First bank's ISPB identifier
        - bank_1_code (int): Second bank's code
        - bank_1_name (str): Second bank's name
        - bank_1_ispb (str): Second bank's ISPB identifier
        - count (int): Total number of banks returned
        - last_updated (str): ISO 8601 timestamp of last update
        - metadata_source_api (str): Source API of the data
        - metadata_data_freshness (str): Freshness status of the data
        - metadata_query_status (str): Status of the query
    """
    return {
        "bank_0_code": 1,
        "bank_0_name": "Banco do Brasil S.A.",
        "bank_0_ispb": "00000000",
        "bank_1_code": 237,
        "bank_1_name": "Banco Bradesco S.A.",
        "bank_1_ispb": "60746948",
        "count": 2,
        "last_updated": "2023-10-15T08:30:00Z",
        "metadata_source_api": "brasilapi",
        "metadata_data_freshness": "up-to-date",
        "metadata_query_status": "success"
    }

def brasil_api_bank_list() -> Dict[str, Any]:
    """
    Retrieve a list of all Brazilian banks with their codes, names, and ISPB identifiers.
    
    This function simulates querying an external API to get up-to-date information
    about Brazilian financial institutions. It returns structured data including
    metadata about the response.
    
    Returns:
        Dict containing:
        - banks (List[Dict]): List of bank objects with code, name, and ISPB
        - count (int): Number of banks in the list
        - last_updated (str): ISO 8601 timestamp of last update
        - metadata (Dict): Additional info including source, freshness, and status
    """
    try:
        api_data = call_external_api("brasil-api-bank-list")
        
        # Construct banks list from flattened API response
        banks = [
            {
                "code": api_data["bank_0_code"],
                "name": api_data["bank_0_name"],
                "ispb": api_data["bank_0_ispb"]
            },
            {
                "code": api_data["bank_1_code"],
                "name": api_data["bank_1_name"],
                "ispb": api_data["bank_1_ispb"]
            }
        ]
        
        # Construct metadata dictionary
        metadata = {
            "source_api": api_data["metadata_source_api"],
            "data_freshness": api_data["metadata_data_freshness"],
            "query_status": api_data["metadata_query_status"]
        }
        
        # Build final result structure
        result = {
            "banks": banks,
            "count": api_data["count"],
            "last_updated": api_data["last_updated"],
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve bank list: {str(e)}")