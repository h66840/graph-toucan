from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for product details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - product_id (str): Unique identifier of the product
        - name (str): Name of the product
        - description (str): Detailed description of the product
        - category (str): Category or type of the product
        - brand (str): Brand or provider associated with the product
        - denomination_0_value (int): Value of the first denomination
        - denomination_0_currency (str): Currency of the first denomination
        - denomination_0_price (float): Price of the first denomination
        - denomination_0_display_value (str): Display value of the first denomination
        - denomination_1_value (int): Value of the second denomination
        - denomination_1_currency (str): Currency of the second denomination
        - denomination_1_price (float): Price of the second denomination
        - denomination_1_display_value (str): Display value of the second denomination
        - available_country_0 (str): First country code where product is available
        - available_country_1 (str): Second country code where product is available
        - supported_currency_0 (str): First supported currency for purchase
        - supported_currency_1 (str): Second supported currency for purchase
        - is_active (bool): Whether the product is currently available for purchase
        - validity_period_days (int): Number of days the product is valid after purchase
        - redemption_instructions (str): Instructions for redeeming the product
        - image_url (str): URL to the product's image or logo
        - metadata_key1 (str): First metadata key-value pair (example key)
        - metadata_key2 (str): Second metadata key-value pair (example key)
    """
    return {
        "product_id": "prod_12345",
        "name": "Amazon US Gift Card",
        "description": "Redeemable on Amazon.com for millions of items.",
        "category": "gift card",
        "brand": "Amazon",
        "denomination_0_value": 10,
        "denomination_0_currency": "USD",
        "denomination_0_price": 10.5,
        "denomination_0_display_value": "$10",
        "denomination_1_value": 25,
        "denomination_1_currency": "USD",
        "denomination_1_price": 26.0,
        "denomination_1_display_value": "$25",
        "available_country_0": "US",
        "available_country_1": "CA",
        "supported_currency_0": "BTC",
        "supported_currency_1": "ETH",
        "is_active": True,
        "validity_period_days": 365,
        "redemption_instructions": "Visit amazon.com/gc and enter the code.",
        "image_url": "https://example.com/images/amazon-gc.png",
        "metadata_key1": "digital_delivery",
        "metadata_key2": "no_refunds"
    }

def bitrefill_mcp_server_detail(id: str) -> Dict[str, Any]:
    """
    Get detailed information about a product by its unique identifier.
    
    Args:
        id (str): Unique identifier of the product
        
    Returns:
        Dict containing detailed product information with the following structure:
        - product_id (str): Unique identifier of the product
        - name (str): Name of the product
        - description (str): Detailed description of the product
        - category (str): Category or type of the product
        - brand (str): Brand or provider associated with the product
        - denominations (List[Dict]): List of available denominations with value, currency, price, and display_value
        - available_countries (List[str]): List of country codes where the product is available
        - supported_currencies (List[str]): List of cryptocurrencies or fiat currencies accepted
        - is_active (bool): Whether the product is currently available for purchase
        - validity_period_days (int): Number of days the product is valid after purchase
        - redemption_instructions (str): Instructions for how to redeem the product
        - image_url (str): URL to the product's image or logo
        - metadata (Dict): Additional key-value pairs with extended attributes
    """
    if not id:
        raise ValueError("Product ID is required")
        
    api_data = call_external_api("bitrefill-mcp-server-detail")
    
    # Construct denominations list from indexed fields
    denominations = [
        {
            "value": api_data["denomination_0_value"],
            "currency": api_data["denomination_0_currency"],
            "price": api_data["denomination_0_price"],
            "display_value": api_data["denomination_0_display_value"]
        },
        {
            "value": api_data["denomination_1_value"],
            "currency": api_data["denomination_1_currency"],
            "price": api_data["denomination_1_price"],
            "display_value": api_data["denomination_1_display_value"]
        }
    ]
    
    # Construct available countries list
    available_countries = [
        api_data["available_country_0"],
        api_data["available_country_1"]
    ]
    
    # Construct supported currencies list
    supported_currencies = [
        api_data["supported_currency_0"],
        api_data["supported_currency_1"]
    ]
    
    # Construct metadata dictionary
    metadata = {
        "key1": api_data["metadata_key1"],
        "key2": api_data["metadata_key2"]
    }
    
    # Build final result matching output schema
    result = {
        "product_id": api_data["product_id"],
        "name": api_data["name"],
        "description": api_data["description"],
        "category": api_data["category"],
        "brand": api_data["brand"],
        "denominations": denominations,
        "available_countries": available_countries,
        "supported_currencies": supported_currencies,
        "is_active": api_data["is_active"],
        "validity_period_days": api_data["validity_period_days"],
        "redemption_instructions": api_data["redemption_instructions"],
        "image_url": api_data["image_url"],
        "metadata": metadata
    }
    
    return result