from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NFT tokens by address.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_collection_type (str): Type of the NFT collection (e.g., ERC-721)
        - data_0_collection_address (str): Contract address of the collection
        - data_0_collection_name (str): Name of the NFT collection
        - data_0_collection_symbol (str): Symbol of the NFT collection
        - data_0_collection_holders_count (int): Number of holders in the collection
        - data_0_collection_total_supply (int): Total supply of the collection
        - data_0_amount (str): Number of tokens held from this collection
        - data_0_token_instances_0_id (str): Token ID of the first token instance
        - data_0_token_instances_0_name (str): Name of the first token instance
        - data_0_token_instances_0_description (str): Description of the first token instance
        - data_0_token_instances_0_image_url (str): Image URL of the first token instance
        - data_0_token_instances_0_external_app_url (str): External app URL of the first token instance
        - data_0_token_instances_0_metadata_attributes_0_display_type (str): Display type of the first metadata attribute
        - data_0_token_instances_0_metadata_attributes_0_trait_type (str): Trait type of the first metadata attribute
        - data_0_token_instances_0_metadata_attributes_0_value (str): Value of the first metadata attribute
        - data_description (str): Description of the data if provided
        - notes (str): Additional notes from the API if present
        - instructions (str): Instructions for next steps or usage if provided
        - pagination_next_page_params_cursor (str): Pagination cursor for next page if available
    """
    return {
        "data_0_collection_type": "ERC-721",
        "data_0_collection_address": "0x1234567890abcdef1234567890abcdef12345678",
        "data_0_collection_name": "CryptoPunks",
        "data_0_collection_symbol": "PUNK",
        "data_0_collection_holders_count": 5000,
        "data_0_collection_total_supply": 10000,
        "data_0_amount": "2",
        "data_0_token_instances_0_id": "123",
        "data_0_token_instances_0_name": "CryptoPunk #123",
        "data_0_token_instances_0_description": "A rare CryptoPunk with unique features.",
        "data_0_token_instances_0_image_url": "https://example.com/punk123.png",
        "data_0_token_instances_0_external_app_url": "https://cryptopunks.app/punk/123",
        "data_0_token_instances_0_metadata_attributes_0_display_type": "number",
        "data_0_token_instances_0_metadata_attributes_0_trait_type": "Accessories",
        "data_0_token_instances_0_metadata_attributes_0_value": "3",
        "data_description": "NFT tokens owned by the address grouped by collection.",
        "notes": None,
        "instructions": "Use cursor to fetch next page if pagination is present.",
        "pagination_next_page_params_cursor": "abc123xyz"
    }

def blockscout_mcp_server_nft_tokens_by_address(address: str, chain_id: str, cursor: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve NFT tokens (ERC-721, ERC-404, ERC-1155) owned by an address, grouped by collection.
    
    Provides collection details (type, address, name, symbol, total supply, holder count)
    and individual token instance data (ID, name, description, external URL, metadata attributes).
    Supports pagination via cursor parameter.

    Args:
        address (str): NFT owner address
        chain_id (str): The ID of the blockchain
        cursor (Optional[str]): Pagination cursor from a previous response to get the next page

    Returns:
        Dict containing:
        - data (List[Dict]): list of NFT collections owned by the address
        - data_description (str): description of the data if provided
        - notes (str): additional notes from the API if present
        - instructions (str): instructions for next steps or usage if provided
        - pagination (Dict): pagination info with next_page_params if more results exist

        Each data item contains:
        - collection (Dict): type, address, name, symbol, holders_count, total_supply
        - amount (str): number of tokens held from this collection
        - token_instances (List[Dict]): individual token instances with id, name, description,
          image_url, external_app_url, and metadata_attributes (list of dicts with display_type,
          trait_type, value)
    """
    # Input validation
    if not address:
        raise ValueError("Address is required.")
    if not chain_id:
        raise ValueError("Chain ID is required.")

    # Call external API (simulated)
    api_data = call_external_api("blockscout-mcp-server-nft_tokens_by_address")

    # Construct token instances
    token_instance = {
        "id": api_data["data_0_token_instances_0_id"],
        "name": api_data["data_0_token_instances_0_name"],
        "description": api_data["data_0_token_instances_0_description"],
        "image_url": api_data["data_0_token_instances_0_image_url"],
        "external_app_url": api_data["data_0_token_instances_0_external_app_url"],
        "metadata_attributes": [
            {
                "display_type": api_data["data_0_token_instances_0_metadata_attributes_0_display_type"],
                "trait_type": api_data["data_0_token_instances_0_metadata_attributes_0_trait_type"],
                "value": api_data["data_0_token_instances_0_metadata_attributes_0_value"]
            }
        ]
    }

    # Construct collection
    collection = {
        "type": api_data["data_0_collection_type"],
        "address": api_data["data_0_collection_address"],
        "name": api_data["data_0_collection_name"],
        "symbol": api_data["data_0_collection_symbol"],
        "holders_count": api_data["data_0_collection_holders_count"],
        "total_supply": api_data["data_0_collection_total_supply"]
    }

    # Construct data item
    data_item = {
        "collection": collection,
        "amount": api_data["data_0_amount"],
        "token_instances": [token_instance]
    }

    # Construct pagination
    pagination = None
    if api_data.get("pagination_next_page_params_cursor"):
        pagination = {
            "next_page_params": {
                "cursor": api_data["pagination_next_page_params_cursor"]
            }
        }

    # Construct final result
    result = {
        "data": [data_item],
        "data_description": api_data["data_description"],
        "notes": api_data["notes"],
        "instructions": api_data["instructions"],
        "pagination": pagination
    }

    return result