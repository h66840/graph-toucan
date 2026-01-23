from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for board game prices.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - currency (str): Currency code used for prices (e.g., USD, EUR)
        - sitename (str): Name of the price comparison website
        - url (str): Base URL of the price comparison service
        - logo (str): URL to the site's logo image
        - item_0_name (str): Name of the first board game edition
        - item_0_id (int): BGG ID of the first board game edition
        - item_0_external_id (str): External identifier for the first edition
        - item_0_image (str): Image URL for the first edition
        - item_0_thumbnail (str): Thumbnail URL for the first edition
        - item_0_url (str): Product page URL for the first edition
        - item_0_price_0_country (str): Country of the first retailer offer
        - item_0_price_0_price (float): Price of the first offer
        - item_0_price_0_product (str): Product name from the first retailer
        - item_0_price_0_shipping (float): Shipping cost for the first offer
        - item_0_price_0_stock (bool): Stock availability for the first offer
        - item_0_price_0_link (str): Purchase link for the first offer
        - item_0_price_0_fee (float): Additional fee for the first offer
        - item_0_price_0_discount (bool): Whether discount applies to first offer
        - item_0_price_0_shipping_known (bool): Whether shipping cost is known
        - item_0_version_lang_0 (str): First language of the first edition
        - item_0_version_lang_1 (str): Second language of the first edition
        - item_1_name (str): Name of the second board game edition
        - item_1_id (int): BGG ID of the second board game edition
        - item_1_external_id (str): External identifier for the second edition
        - item_1_image (str): Image URL for the second edition
        - item_1_thumbnail (str): Thumbnail URL for the second edition
        - item_1_url (str): Product page URL for the second edition
        - item_1_price_0_country (str): Country of the first retailer offer for second item
        - item_1_price_0_price (float): Price of the first offer for second item
        - item_1_price_0_product (str): Product name from the first retailer for second item
        - item_1_price_0_shipping (float): Shipping cost for the first offer for second item
        - item_1_price_0_stock (bool): Stock availability for the first offer for second item
        - item_1_price_0_link (str): Purchase link for the first offer for second item
        - item_1_price_0_fee (float): Additional fee for the first offer for second item
        - item_1_price_0_discount (bool): Whether discount applies to first offer for second item
        - item_1_price_0_shipping_known (bool): Whether shipping cost is known for second item
        - item_1_version_lang_0 (str): First language of the second edition
        - item_1_version_lang_1 (str): Second language of the second edition
    """
    return {
        "currency": "USD",
        "sitename": "BoardGamePrices.com",
        "url": "https://www.boardgameprices.com",
        "logo": "https://www.boardgameprices.com/logo.png",
        "item_0_name": "Catan",
        "item_0_id": 13,
        "item_0_external_id": "bgg-13",
        "item_0_image": "https://example.com/catan.jpg",
        "item_0_thumbnail": "https://example.com/catan_thumb.jpg",
        "item_0_url": "https://www.boardgameprices.com/game/catan",
        "item_0_price_0_country": "US",
        "item_0_price_0_price": 49.99,
        "item_0_price_0_product": "Catan Base Game",
        "item_0_price_0_shipping": 5.99,
        "item_0_price_0_stock": True,
        "item_0_price_0_link": "https://retailer.com/catan",
        "item_0_price_0_fee": 2.50,
        "item_0_price_0_discount": False,
        "item_0_price_0_shipping_known": True,
        "item_0_version_lang_0": "en",
        "item_0_version_lang_1": "es",
        "item_1_name": "Ticket to Ride",
        "item_1_id": 30549,
        "item_1_external_id": "bgg-30549",
        "item_1_image": "https://example.com/ticket_to_ride.jpg",
        "item_1_thumbnail": "https://example.com/ticket_to_ride_thumb.jpg",
        "item_1_url": "https://www.boardgameprices.com/game/ticket-to-ride",
        "item_1_price_0_country": "US",
        "item_1_price_0_price": 59.99,
        "item_1_price_0_product": "Ticket to Ride: Europe",
        "item_1_price_0_shipping": 6.99,
        "item_1_price_0_stock": True,
        "item_1_price_0_link": "https://retailer.com/ticket-to-ride",
        "item_1_price_0_fee": 3.00,
        "item_1_price_0_discount": True,
        "item_1_price_0_shipping_known": True,
        "item_1_version_lang_0": "en",
        "item_1_version_lang_1": "fr"
    }

def boardgamegeek_api_server_bgg_price(
    ids: str,
    currency: Optional[str] = "USD",
    destination: Optional[str] = "US"
) -> Dict[str, Any]:
    """
    Get current prices for board games from multiple retailers using BGG IDs.
    
    Args:
        ids (str): Comma-separated BGG IDs (e.g., '12,844,2096,13857')
        currency (Optional[str]): Currency code: DKK, GBP, SEK, EUR, or USD (default: USD)
        destination (Optional[str]): Destination country: DK, SE, GB, DE, or US (default: US)
        
    Returns:
        Dict containing:
        - currency (str): the currency code used for prices
        - items (List[Dict]): list of game versions/editions with details including name, image, thumbnail, URL, prices, and version metadata
        - logo (str): URL to the site's logo image
        - sitename (str): name of the price comparison website
        - url (str): base URL of the price comparison service
        Each item in 'items' contains:
        - name (str): game name
        - id (int): BGG ID
        - external_id (str): external identifier
        - image (str): image URL
        - thumbnail (str): thumbnail URL
        - url (str): product page URL
        - prices (List[Dict]): list of retailer offers with country, price, product, shipping, stock, link, fee, discount, shipping_known
        - versions (Dict): language or regional version info with 'lang' as List[str]
        
    Raises:
        ValueError: If ids parameter is empty or not provided
    """
    if not ids or not ids.strip():
        raise ValueError("Parameter 'ids' is required and cannot be empty")
        
    # Validate currency if provided
    valid_currencies = {"DKK", "GBP", "SEK", "EUR", "USD"}
    if currency and currency not in valid_currencies:
        raise ValueError(f"Invalid currency '{currency}'. Must be one of {valid_currencies}")
        
    # Validate destination if provided
    valid_destinations = {"DK", "SE", "GB", "DE", "US"}
    if destination and destination not in valid_destinations:
        raise ValueError(f"Invalid destination '{destination}'. Must be one of {valid_destinations}")
    
    # Call external API to get flattened data
    api_data = call_external_api("boardgamegeek_api_server_bgg_price")
    
    # Construct nested structure matching output schema
    result = {
        "currency": api_data["currency"],
        "sitename": api_data["sitename"],
        "url": api_data["url"],
        "logo": api_data["logo"],
        "items": [
            {
                "name": api_data["item_0_name"],
                "id": api_data["item_0_id"],
                "external_id": api_data["item_0_external_id"],
                "image": api_data["item_0_image"],
                "thumbnail": api_data["item_0_thumbnail"],
                "url": api_data["item_0_url"],
                "prices": [
                    {
                        "country": api_data["item_0_price_0_country"],
                        "price": api_data["item_0_price_0_price"],
                        "product": api_data["item_0_price_0_product"],
                        "shipping": api_data["item_0_price_0_shipping"],
                        "stock": api_data["item_0_price_0_stock"],
                        "link": api_data["item_0_price_0_link"],
                        "fee": api_data["item_0_price_0_fee"],
                        "discount": api_data["item_0_price_0_discount"],
                        "shipping_known": api_data["item_0_price_0_shipping_known"]
                    }
                ],
                "versions": {
                    "lang": [
                        api_data["item_0_version_lang_0"],
                        api_data["item_0_version_lang_1"]
                    ]
                }
            },
            {
                "name": api_data["item_1_name"],
                "id": api_data["item_1_id"],
                "external_id": api_data["item_1_external_id"],
                "image": api_data["item_1_image"],
                "thumbnail": api_data["item_1_thumbnail"],
                "url": api_data["item_1_url"],
                "prices": [
                    {
                        "country": api_data["item_1_price_0_country"],
                        "price": api_data["item_1_price_0_price"],
                        "product": api_data["item_1_price_0_product"],
                        "shipping": api_data["item_1_price_0_shipping"],
                        "stock": api_data["item_1_price_0_stock"],
                        "link": api_data["item_1_price_0_link"],
                        "fee": api_data["item_1_price_0_fee"],
                        "discount": api_data["item_1_price_0_discount"],
                        "shipping_known": api_data["item_1_price_0_shipping_known"]
                    }
                ],
                "versions": {
                    "lang": [
                        api_data["item_1_version_lang_0"],
                        api_data["item_1_version_lang_1"]
                    ]
                }
            }
        ]
    }
    
    return result