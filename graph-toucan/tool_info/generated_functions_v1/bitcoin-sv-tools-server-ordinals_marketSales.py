from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ordinals market sales.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - sales_0_token_id (str): Token ID of the first sale
        - sales_0_ticker (str): Ticker symbol of the first sale
        - sales_0_sale_price (float): Sale price in BSV of the first sale
        - sales_0_tx_hash (str): Transaction hash of the first sale
        - sales_0_seller_address (str): Seller address of the first sale
        - sales_0_buyer_address (str): Buyer address of the first sale
        - sales_0_timestamp (str): ISO 8601 timestamp of the first sale
        - sales_0_token_type (str): Type of token (BSV-20 or BSV-21) for the first sale
        - sales_1_token_id (str): Token ID of the second sale
        - sales_1_ticker (str): Ticker symbol of the second sale
        - sales_1_sale_price (float): Sale price in BSV of the second sale
        - sales_1_tx_hash (str): Transaction hash of the second sale
        - sales_1_seller_address (str): Seller address of the second sale
        - sales_1_buyer_address (str): Buyer address of the second sale
        - sales_1_timestamp (str): ISO 8601 timestamp of the second sale
        - sales_1_token_type (str): Type of token (BSV-20 or BSV-21) for the second sale
        - total_count (int): Total number of matching sales across all pages
        - limit (int): Number of results returned in this response
        - offset (int): Pagination offset used in this query
        - has_more (bool): Whether more results are available beyond current page
        - filters_applied_tokenType (str): Applied filter for token type
        - filters_applied_tick (str): Applied filter for ticker symbol
        - filters_applied_id (str): Applied filter for token ID
        - filters_applied_address (str): Applied filter for address
        - filters_applied_pending (bool): Whether pending inclusion was filtered
        - timestamp (str): ISO 8601 timestamp when data was fetched
    """
    return {
        "sales_0_token_id": "a1b2c3d4e5f6g7h8i9j0",
        "sales_0_ticker": "TEST",
        "sales_0_sale_price": 0.5,
        "sales_0_tx_hash": "txhash1234567890abcdef",
        "sales_0_seller_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "sales_0_buyer_address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        "sales_0_timestamp": "2023-10-01T12:34:56Z",
        "sales_0_token_type": "BSV-20",
        "sales_1_token_id": "z9y8x7w6v5u4t3s2r1q0",
        "sales_1_ticker": "ORDI",
        "sales_1_sale_price": 1.25,
        "sales_1_tx_hash": "txhash0987654321fedcba",
        "sales_1_seller_address": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX",
        "sales_1_buyer_address": "1HLoD9E4SDFFPDiYfNYnktdV8H5PGo97Tw",
        "sales_1_timestamp": "2023-10-01T13:45:00Z",
        "sales_1_token_type": "BSV-21",
        "total_count": 150,
        "limit": 2,
        "offset": 0,
        "has_more": True,
        "filters_applied_tokenType": "BSV-20,BSV-21",
        "filters_applied_tick": "TEST",
        "filters_applied_id": "",
        "filters_applied_address": "",
        "filters_applied_pending": False,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def bitcoin_sv_tools_server_ordinals_marketSales(args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Retrieves recent sales data for BSV-20 and BSV-21 tokens on the ordinals marketplace.
    
    This function simulates querying market sales data with support for filtering by token ID,
    ticker symbol, or seller address. It returns a structured response containing sale records,
    pagination info, applied filters, and metadata.

    Args:
        args (Dict[str, Any], optional): Input parameters for filtering and pagination.
            Supported keys:
            - tick (str): Filter by ticker symbol
            - id (str): Filter by token ID
            - address (str): Filter by seller address
            - tokenType (str): Filter by token type ('BSV-20', 'BSV-21', or both)
            - limit (int): Number of results per page (default: 2)
            - offset (int): Pagination offset (default: 0)

    Returns:
        Dict containing:
        - sales (List[Dict]): List of sale records with token ID, ticker, price, tx hash,
          seller/buyer addresses, timestamp, and token type
        - total_count (int): Total number of matching sales across all pages
        - limit (int): Number of results returned in this response
        - offset (int): Pagination offset used
        - has_more (bool): Whether more results exist beyond current page
        - filters_applied (Dict): Summary of active filters
        - timestamp (str): ISO 8601 timestamp of data generation

    Example:
        >>> result = bitcoin_sv_tools_server_ordinals_marketSales({"tick": "TEST", "limit": 2})
        >>> print(result["sales"][0]["ticker"])
        TEST
    """
    if args is None:
        args = {}

    # Validate input types
    if not isinstance(args, dict):
        raise ValueError("args must be a dictionary")

    # Call external API (simulated)
    api_data = call_external_api("bitcoin-sv-tools-server-ordinals_marketSales")

    # Construct sales list from indexed fields
    sales = [
        {
            "token_id": api_data["sales_0_token_id"],
            "ticker": api_data["sales_0_ticker"],
            "sale_price": api_data["sales_0_sale_price"],
            "tx_hash": api_data["sales_0_tx_hash"],
            "seller_address": api_data["sales_0_seller_address"],
            "buyer_address": api_data["sales_0_buyer_address"],
            "timestamp": api_data["sales_0_timestamp"],
            "token_type": api_data["sales_0_token_type"]
        },
        {
            "token_id": api_data["sales_1_token_id"],
            "ticker": api_data["sales_1_ticker"],
            "sale_price": api_data["sales_1_sale_price"],
            "tx_hash": api_data["sales_1_tx_hash"],
            "seller_address": api_data["sales_1_seller_address"],
            "buyer_address": api_data["sales_1_buyer_address"],
            "timestamp": api_data["sales_1_timestamp"],
            "token_type": api_data["sales_1_token_type"]
        }
    ]

    # Construct filters_applied dictionary
    filters_applied = {
        "tokenType": api_data["filters_applied_tokenType"],
        "tick": api_data["filters_applied_tick"],
        "id": api_data["filters_applied_id"],
        "address": api_data["filters_applied_address"],
        "pending": api_data["filters_applied_pending"]
    }

    # Build final result structure
    result = {
        "sales": sales,
        "total_count": api_data["total_count"],
        "limit": api_data["limit"],
        "offset": api_data["offset"],
        "has_more": api_data["has_more"],
        "filters_applied": filters_applied,
        "timestamp": api_data["timestamp"]
    }

    return result