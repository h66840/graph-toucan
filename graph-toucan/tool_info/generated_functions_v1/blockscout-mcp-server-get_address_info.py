from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for address information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - basic_info_hash (str): The address hash
        - basic_info_balance (str): Native token balance as string
        - basic_info_is_contract (bool): Whether the address is a contract
        - basic_info_is_verified (bool): Whether the contract is verified
        - basic_info_ens_name (str): ENS name associated with the address, if any
        - basic_info_token_name (str): Token name if the contract is a token
        - basic_info_token_symbol (str): Token symbol if the contract is a token
        - basic_info_token_decimals (int): Token decimals if the contract is a token
        - basic_info_token_total_supply (str): Token total supply as string
        - basic_info_is_proxy (bool): Whether the contract is a proxy
        - basic_info_proxy_type (str): Type of proxy (e.g., 'EIP1967')
        - basic_info_implementation_address (str): Implementation contract address
        - metadata_tags_0_slug (str): First tag slug
        - metadata_tags_0_name (str): First tag name
        - metadata_tags_0_tagType (str): First tag type
        - metadata_tags_0_ordinal (int): First tag ordinal
        - metadata_tags_0_meta_description (str): First tag meta description
        - metadata_tags_1_slug (str): Second tag slug
        - metadata_tags_1_name (str): Second tag name
        - metadata_tags_1_tagType (str): Second tag type
        - metadata_tags_1_ordinal (int): Second tag ordinal
        - metadata_tags_1_meta_description (str): Second tag meta description
        - data_description (str): Description of the data returned
        - notes (str): Additional notes or explanations
        - instructions (str): Instructions for next steps
        - pagination_next_page_url (str): URL for next page, if paginated
        - pagination_prev_page_url (str): URL for previous page, if paginated
        - pagination_current_page (int): Current page number
        - pagination_total_pages (int): Total number of pages
    """
    return {
        "basic_info_hash": "0x1234567890abcdef1234567890abcdef12345678",
        "basic_info_balance": "1234567890000000000",
        "basic_info_is_contract": True,
        "basic_info_is_verified": True,
        "basic_info_ens_name": "vitalik.eth",
        "basic_info_token_name": "Ethereum",
        "basic_info_token_symbol": "ETH",
        "basic_info_token_decimals": 18,
        "basic_info_token_total_supply": "120000000000000000000000000",
        "basic_info_is_proxy": True,
        "basic_info_proxy_type": "EIP1967",
        "basic_info_implementation_address": "0x9876543210abcdef9876543210abcdef98765432",
        "metadata_tags_0_slug": "defi-core",
        "metadata_tags_0_name": "DeFi Core",
        "metadata_tags_0_tagType": "category",
        "metadata_tags_0_ordinal": 1,
        "metadata_tags_0_meta_description": "Core DeFi protocol",
        "metadata_tags_1_slug": "audited",
        "metadata_tags_1_name": "Audited",
        "metadata_tags_1_tagType": "security",
        "metadata_tags_1_ordinal": 2,
        "metadata_tags_1_meta_description": "Contract has been audited",
        "data_description": "Comprehensive address information including contract and token details",
        "notes": "Address is a verified proxy contract. Use implementation address for bytecode analysis.",
        "instructions": "Review implementation contract for actual logic. Check ENS resolver for ownership details.",
        "pagination_next_page_url": None,
        "pagination_prev_page_url": None,
        "pagination_current_page": 1,
        "pagination_total_pages": 1,
    }

def blockscout_mcp_server_get_address_info(address: str, chain_id: str) -> Dict[str, Any]:
    """
    Get comprehensive information about an address, including balance, contract status, token details,
    ENS name, proxy information, and metadata.

    Args:
        address (str): The blockchain address to query
        chain_id (str): The ID of the blockchain (e.g., '1' for Ethereum mainnet)

    Returns:
        Dict containing:
        - basic_info (Dict): Core information about the address
        - metadata (Dict): Optional metadata with tags
        - data_description (str): Description of the returned data
        - notes (str): Additional system notes
        - instructions (str): Guidance for interpretation
        - pagination (Dict): Pagination information if results are paginated

    Raises:
        ValueError: If address or chain_id is empty
    """
    if not address:
        raise ValueError("Address is required")
    if not chain_id:
        raise ValueError("Chain ID is required")

    # Normalize address
    address = address.lower().strip()
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError("Invalid Ethereum address format")

    # Fetch data from external API (simulated)
    api_data = call_external_api("blockscout-mcp-server-get_address_info")

    # Construct basic_info
    basic_info = {
        "hash": api_data["basic_info_hash"],
        "balance": api_data["basic_info_balance"],
        "is_contract": api_data["basic_info_is_contract"],
        "is_verified": api_data["basic_info_is_verified"],
        "ens_name": api_data["basic_info_ens_name"],
        "token_name": api_data["basic_info_token_name"],
        "token_symbol": api_data["basic_info_token_symbol"],
        "token_decimals": api_data["basic_info_token_decimals"],
        "token_total_supply": api_data["basic_info_token_total_supply"],
        "is_proxy": api_data["basic_info_is_proxy"],
        "proxy_type": api_data["basic_info_proxy_type"],
        "implementation_address": api_data["basic_info_implementation_address"],
    }

    # Construct metadata tags
    tags = [
        {
            "slug": api_data["metadata_tags_0_slug"],
            "name": api_data["metadata_tags_0_name"],
            "tagType": api_data["metadata_tags_0_tagType"],
            "ordinal": api_data["metadata_tags_0_ordinal"],
            "meta": {"description": api_data["metadata_tags_0_meta_description"]},
        },
        {
            "slug": api_data["metadata_tags_1_slug"],
            "name": api_data["metadata_tags_1_name"],
            "tagType": api_data["metadata_tags_1_tagType"],
            "ordinal": api_data["metadata_tags_1_ordinal"],
            "meta": {"description": api_data["metadata_tags_1_meta_description"]},
        },
    ]

    metadata = {"tags": tags}

    # Construct pagination
    pagination = {
        "next_page_url": api_data["pagination_next_page_url"],
        "prev_page_url": api_data["pagination_prev_page_url"],
        "current_page": api_data["pagination_current_page"],
        "total_pages": api_data["pagination_total_pages"],
    }

    # Return final structured response
    return {
        "basic_info": basic_info,
        "metadata": metadata,
        "data_description": api_data["data_description"],
        "notes": api_data["notes"],
        "instructions": api_data["instructions"],
        "pagination": pagination,
    }