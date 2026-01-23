from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bitrefill MCP server categories.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - giftcards_0 (str): First available gift card category slug
        - giftcards_1 (str): Second available gift card category slug
        - refills_0 (str): First available mobile refill category slug
        - refills_1 (str): Second available mobile refill category slug
        - bills_0 (str): First available bill payment category slug
        - bills_1 (str): Second available bill payment category slug
        - esims_0 (str): First available eSIM category slug
        - esims_1 (str): Second available eSIM category slug
        - crypto_utils_0 (str): First available cryptocurrency utility category slug
        - crypto_utils_1 (str): Second available cryptocurrency utility category slug
    """
    return {
        "giftcards_0": "digital-gift-cards",
        "giftcards_1": "physical-gift-cards",
        "refills_0": "mobile-top-up",
        "refills_1": "data-packages",
        "bills_0": "electricity-bills",
        "bills_1": "internet-bills",
        "esims_0": "travel-esim",
        "esims_1": "local-esim",
        "crypto_utils_0": "crypto-giftcards",
        "crypto_utils_1": "crypto-exchange",
    }

def bitrefill_mcp_server_categories() -> Dict[str, List[str]]:
    """
    Get the full product type/categories map from Bitrefill MCP server.
    
    This function retrieves the list of available categories for various product types
    including gift cards, mobile refills, bill payments, eSIMs, and cryptocurrency utilities.
    It is suggested to use this tool to get the categories and then use the `search` tool
    to search for products in a specific category.
    
    Returns:
        Dict containing lists of category slugs for each product type:
        - giftcards (List[str]): list of available gift card category slugs
        - refills (List[str]): list of available mobile refill category slugs
        - bills (List[str]): list of available bill payment category slugs
        - esims (List[str]): list of available eSIM category slugs
        - crypto-utils (List[str]): list of available cryptocurrency utility category slugs
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("bitrefill-mcp-server-categories")
        
        # Construct the result dictionary with proper nested structure
        result = {
            "giftcards": [
                api_data["giftcards_0"],
                api_data["giftcards_1"]
            ],
            "refills": [
                api_data["refills_0"],
                api_data["refills_1"]
            ],
            "bills": [
                api_data["bills_0"],
                api_data["bills_1"]
            ],
            "esims": [
                api_data["esims_0"],
                api_data["esims_1"]
            ],
            "crypto-utils": [
                api_data["crypto_utils_0"],
                api_data["crypto_utils_1"]
            ]
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve categories: {str(e)}")