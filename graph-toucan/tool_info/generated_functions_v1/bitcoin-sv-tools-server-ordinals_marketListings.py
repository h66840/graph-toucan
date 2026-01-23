from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bitcoin SV ordinals marketplace listings.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - listing_0_txid (str): Transaction ID of the first listing
        - listing_0_vout (int): Output index of the first listing
        - listing_0_outpoint (str): Outpoint (txid:vout) of the first listing
        - listing_0_satoshis (int): Amount in satoshis of the first listing
        - listing_0_height (int): Block height of the first listing
        - listing_0_owner (str): Owner address of the first listing
        - listing_0_origin_txid (str): Origin transaction ID of the inscription for the first listing
        - listing_0_origin_vout (int): Origin output index of the inscription for the first listing
        - listing_0_origin_offset (int): Offset within the origin output for the first listing
        - listing_0_data_price (int): Listing price in satoshis for the first listing
        - listing_0_data_payout (str): Payout script for the first listing
        - listing_0_data_state (str): Sale status of the first listing
        - listing_1_txid (str): Transaction ID of the second listing
        - listing_1_vout (int): Output index of the second listing
        - listing_1_outpoint (str): Outpoint (txid:vout) of the second listing
        - listing_1_satoshis (int): Amount in satoshis of the second listing
        - listing_1_height (int): Block height of the second listing
        - listing_1_owner (str): Owner address of the second listing
        - listing_1_origin_txid (str): Origin transaction ID of the inscription for the second listing
        - listing_1_origin_vout (int): Origin output index of the inscription for the second listing
        - listing_1_origin_offset (int): Offset within the origin output for the second listing
        - listing_1_data_price (int): Listing price in satoshis for the second listing
        - listing_1_data_payout (str): Payout script for the second listing
        - listing_1_data_state (str): Sale status of the second listing
    """
    return {
        "listing_0_txid": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "listing_0_vout": 0,
        "listing_0_outpoint": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2:0",
        "listing_0_satoshis": 10000,
        "listing_0_height": 800000,
        "listing_0_owner": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "listing_0_origin_txid": "z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8",
        "listing_0_origin_vout": 1,
        "listing_0_origin_offset": 0,
        "listing_0_data_price": 50000,
        "listing_0_data_payout": "76a914000000000000000000000000000000000000000088ac",
        "listing_0_data_state": "listed",
        "listing_1_txid": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "listing_1_vout": 1,
        "listing_1_outpoint": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3:1",
        "listing_1_satoshis": 15000,
        "listing_1_height": 800005,
        "listing_1_owner": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        "listing_1_origin_txid": "y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7",
        "listing_1_origin_vout": 0,
        "listing_1_origin_offset": 1,
        "listing_1_data_price": 75000,
        "listing_1_data_payout": "76a914111111111111111111111111111111111111111188ac",
        "listing_1_data_state": "active"
    }

def bitcoin_sv_tools_server_ordinals_marketListings(args: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieves current marketplace listings for Bitcoin SV ordinals with flexible filtering.
    
    This function simulates querying a marketplace API for Bitcoin SV ordinals listings,
    supporting multiple asset types (NFTs, BSV-20 tokens, BSV-21 tokens) through a unified interface.
    The results include listing prices, asset details, and seller information.
    
    Args:
        args (Dict[str, Any]): Input parameters for filtering the marketplace listings.
            Example keys might include: 'asset_type', 'min_price', 'max_price', 'seller', etc.
            Note: In this simulation, args are not used as external data is mocked.
    
    Returns:
        Dict containing a single key 'listings' with a list of marketplace listings.
        Each listing contains:
            - txid (str): Transaction ID
            - vout (int): Output index
            - outpoint (str): Transaction outpoint (txid:vout)
            - satoshis (int): Amount in satoshis
            - height (int): Block height
            - owner (str): Owner's address
            - origin (Dict): Origin inscription data with keys 'txid', 'vout', 'offset'
            - data (Dict): Listing data with keys 'price', 'payout', 'state'
    
    Example:
        {
            "listings": [
                {
                    "txid": "a1b2c3d4e5f6...",
                    "vout": 0,
                    "outpoint": "a1b2c3d4e5f6...:0",
                    "satoshis": 10000,
                    "height": 800000,
                    "owner": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                    "origin": {
                        "txid": "z9y8x7w6v5u4...",
                        "vout": 1,
                        "offset": 0
                    },
                    "data": {
                        "price": 50000,
                        "payout": "76a914000000000000000000000000000000000000000088ac",
                        "state": "listed"
                    }
                },
                ...
            ]
        }
    """
    try:
        # Validate input
        if not isinstance(args, dict):
            raise ValueError("Input parameter 'args' must be a dictionary.")
        
        # Fetch simulated external data
        api_data = call_external_api("bitcoin-sv-tools-server-ordinals_marketListings")
        
        # Construct listings from flat API data
        listings = []
        
        # Process first listing
        listing_0 = {
            "txid": api_data["listing_0_txid"],
            "vout": api_data["listing_0_vout"],
            "outpoint": api_data["listing_0_outpoint"],
            "satoshis": api_data["listing_0_satoshis"],
            "height": api_data["listing_0_height"],
            "owner": api_data["listing_0_owner"],
            "origin": {
                "txid": api_data["listing_0_origin_txid"],
                "vout": api_data["listing_0_origin_vout"],
                "offset": api_data["listing_0_origin_offset"]
            },
            "data": {
                "price": api_data["listing_0_data_price"],
                "payout": api_data["listing_0_data_payout"],
                "state": api_data["listing_0_data_state"]
            }
        }
        listings.append(listing_0)
        
        # Process second listing
        listing_1 = {
            "txid": api_data["listing_1_txid"],
            "vout": api_data["listing_1_vout"],
            "outpoint": api_data["listing_1_outpoint"],
            "satoshis": api_data["listing_1_satoshis"],
            "height": api_data["listing_1_height"],
            "owner": api_data["listing_1_owner"],
            "origin": {
                "txid": api_data["listing_1_origin_txid"],
                "vout": api_data["listing_1_origin_vout"],
                "offset": api_data["listing_1_origin_offset"]
            },
            "data": {
                "price": api_data["listing_1_data_price"],
                "payout": api_data["listing_1_data_payout"],
                "state": api_data["listing_1_data_state"]
            }
        }
        listings.append(listing_1)
        
        return {"listings": listings}
        
    except Exception as e:
        # In a real implementation, this might log the error
        # For now, re-raise to be handled by caller
        raise e