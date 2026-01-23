from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bitrefill product search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_count (int): Number of results returned
        - item_0_name (str): Name of the first product
        - item_0_type (str): Type of the first product
        - item_0_url (str): URL of the first product
        - item_0_baseName (str): Base name of the first product
        - item_0_categories_0 (str): First category of the first product
        - item_0_categories_1 (str): Second category of the first product
        - item_0_countries_0 (str): First supported country of the first product
        - item_0_countries_1 (str): Second supported country of the first product
        - item_0_currency (str): Currency code for the first product
        - item_0_priceRange_min (float): Minimum price of the first product
        - item_0_priceRange_max (float): Maximum price of the first product
        - item_0_ratingValue (float): Rating value of the first product
        - item_0_reviewCount (int): Number of reviews for the first product
        - item_0_cashbackPercentage (float): Cashback percentage for the first product
        - item_0_redemptionMethods_0 (str): First redemption method of the first product
        - item_0_redemptionMethods_1 (str): Second redemption method of the first product
        - item_0_usageMethods_0 (str): First usage method of the first product
        - item_0_usageMethods_1 (str): Second usage method of the first product
        - item_0_usps_0 (str): First unique selling point of the first product
        - item_0_usps_1 (str): Second unique selling point of the first product
        - item_1_name (str): Name of the second product
        - item_1_type (str): Type of the second product
        - item_1_url (str): URL of the second product
        - item_1_baseName (str): Base name of the second product
        - item_1_categories_0 (str): First category of the second product
        - item_1_categories_1 (str): Second category of the second product
        - item_1_countries_0 (str): First supported country of the second product
        - item_1_countries_1 (str): Second supported country of the second product
        - item_1_currency (str): Currency code for the second product
        - item_1_priceRange_min (float): Minimum price of the second product
        - item_1_priceRange_max (float): Maximum price of the second product
        - item_1_ratingValue (float): Rating value of the second product
        - item_1_reviewCount (int): Number of reviews for the second product
        - item_1_cashbackPercentage (float): Cashback percentage for the second product
        - item_1_redemptionMethods_0 (str): First redemption method of the second product
        - item_1_redemptionMethods_1 (str): Second redemption method of the second product
        - item_1_usageMethods_0 (str): First usage method of the second product
        - item_1_usageMethods_1 (str): Second usage method of the second product
        - item_1_usps_0 (str): First unique selling point of the second product
        - item_1_usps_1 (str): Second unique selling point of the second product
    """
    return {
        "result_count": 2,
        "item_0_name": "Amazon Gift Card",
        "item_0_type": "gift_card",
        "item_0_url": "https://bitrefill.com/products/amazon",
        "item_0_baseName": "Amazon",
        "item_0_categories_0": "gaming",
        "item_0_categories_1": "entertainment",
        "item_0_countries_0": "US",
        "item_0_countries_1": "GB",
        "item_0_currency": "USD",
        "item_0_priceRange_min": 10.0,
        "item_0_priceRange_max": 500.0,
        "item_0_ratingValue": 4.8,
        "item_0_reviewCount": 1250,
        "item_0_cashbackPercentage": 2.5,
        "item_0_redemptionMethods_0": "email_delivery",
        "item_0_redemptionMethods_1": "instant_code",
        "item_0_usageMethods_0": "online_purchase",
        "item_0_usageMethods_1": "digital_wallet",
        "item_0_usps_0": "Instant delivery",
        "item_0_usps_1": "No fees",
        "item_1_name": "Netflix Gift Card",
        "item_1_type": "gift_card",
        "item_1_url": "https://bitrefill.com/products/netflix",
        "item_1_baseName": "Netflix",
        "item_1_categories_0": "entertainment",
        "item_1_categories_1": "streaming",
        "item_1_countries_0": "US",
        "item_1_countries_1": "CA",
        "item_1_currency": "USD",
        "item_1_priceRange_min": 15.0,
        "item_1_priceRange_max": 100.0,
        "item_1_ratingValue": 4.7,
        "item_1_reviewCount": 890,
        "item_1_cashbackPercentage": 1.8,
        "item_1_redemptionMethods_0": "email_delivery",
        "item_1_redemptionMethods_1": "qr_code",
        "item_1_usageMethods_0": "subscription_payment",
        "item_1_usageMethods_1": "account_topup",
        "item_1_usps_0": "Global usage",
        "item_1_usps_1": "No expiration",
    }


def bitrefill_mcp_server_search(
    query: str,
    beta_flags: Optional[str] = None,
    cart: Optional[str] = None,
    category: Optional[str] = None,
    col: Optional[int] = None,
    country: Optional[str] = None,
    do_recommend: Optional[int] = None,
    language: Optional[str] = None,
    limit: Optional[int] = None,
    prefcc: Optional[int] = None,
    rec: Optional[int] = None,
    sec: Optional[int] = None,
    skip: Optional[int] = None,
    src: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Search for gift cards, esims, mobile topups and more on Bitrefill.

    This function simulates searching the Bitrefill platform for digital products
    based on a query and optional filters. It returns a list of matching products
    with detailed metadata.

    Args:
        query (str): Search query (e.g., 'Amazon', 'Netflix', 'AT&T' or '*' for all products)
        beta_flags (str, optional): Beta feature flags
        cart (str, optional): Cart identifier
        category (str, optional): Filter by category (e.g., 'gaming', 'entertainment')
        col (int, optional): Column layout parameter
        country (str, optional): Country code (e.g., 'US', 'IT', 'GB')
        do_recommend (int, optional): Enable recommendations
        language (str, optional): Language code for results (e.g., 'en')
        limit (int, optional): Maximum number of results to return
        prefcc (int, optional): Preferred country code parameter
        rec (int, optional): Recommendation parameter
        sec (int, optional): Security parameter
        skip (int, optional): Number of results to skip (for pagination)
        src (str, optional): Source of the request

    Returns:
        Dict containing:
        - results (List[Dict]): List of product results with fields:
            - name (str): Product name
            - type (str): Product type
            - url (str): Product URL
            - baseName (str): Base name of the product
            - categories (List[str]): List of categories
            - countries (List[str]): List of supported countries
            - currency (str): Currency code
            - priceRange (Dict): Min and max price
            - ratingValue (float): Average rating
            - reviewCount (int): Number of reviews
            - cashbackPercentage (float): Cashback percentage
            - redemptionMethods (List[str]): How to redeem the product
            - usageMethods (List[str]): How to use the product
            - usps (List[str]): Unique selling points

    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    # Call external API to get flattened data
    api_data = call_external_api("bitrefill-mcp_server_search")

    # Construct results list from flattened API data
    results = []

    # Process first item
    item_0 = {
        "name": api_data["item_0_name"],
        "type": api_data["item_0_type"],
        "url": api_data["item_0_url"],
        "baseName": api_data["item_0_baseName"],
        "categories": [
            api_data["item_0_categories_0"],
            api_data["item_0_categories_1"]
        ],
        "countries": [
            api_data["item_0_countries_0"],
            api_data["item_0_countries_1"]
        ],
        "currency": api_data["item_0_currency"],
        "priceRange": {
            "min": api_data["item_0_priceRange_min"],
            "max": api_data["item_0_priceRange_max"]
        },
        "ratingValue": api_data["item_0_ratingValue"],
        "reviewCount": api_data["item_0_reviewCount"],
        "cashbackPercentage": api_data["item_0_cashbackPercentage"],
        "redemptionMethods": [
            api_data["item_0_redemptionMethods_0"],
            api_data["item_0_redemptionMethods_1"]
        ],
        "usageMethods": [
            api_data["item_0_usageMethods_0"],
            api_data["item_0_usageMethods_1"]
        ],
        "usps": [
            api_data["item_0_usps_0"],
            api_data["item_0_usps_1"]
        ]
    }
    results.append(item_0)

    # Process second item
    item_1 = {
        "name": api_data["item_1_name"],
        "type": api_data["item_1_type"],
        "url": api_data["item_1_url"],
        "baseName": api_data["item_1_baseName"],
        "categories": [
            api_data["item_1_categories_0"],
            api_data["item_1_categories_1"]
        ],
        "countries": [
            api_data["item_1_countries_0"],
            api_data["item_1_countries_1"]
        ],
        "currency": api_data["item_1_currency"],
        "priceRange": {
            "min": api_data["item_1_priceRange_min"],
            "max": api_data["item_1_priceRange_max"]
        },
        "ratingValue": api_data["item_1_ratingValue"],
        "reviewCount": api_data["item_1_reviewCount"],
        "cashbackPercentage": api_data["item_1_cashbackPercentage"],
        "redemptionMethods": [
            api_data["item_1_redemptionMethods_0"],
            api_data["item_1_redemptionMethods_1"]
        ],
        "usageMethods": [
            api_data["item_1_usageMethods_0"],
            api_data["item_1_usageMethods_1"]
        ],
        "usps": [
            api_data["item_1_usps_0"],
            api_data["item_1_usps_1"]
        ]
    }
    results.append(item_1)

    return {
        "results": results
    }