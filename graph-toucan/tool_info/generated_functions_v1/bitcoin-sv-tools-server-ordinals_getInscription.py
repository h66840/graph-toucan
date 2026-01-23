from typing import Dict, List, Any, Optional
import base64
import random
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching inscription data from external API for Bitcoin SV ordinals.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - inscription_id (str): Unique identifier for the inscription
        - outpoint (str): The outpoint (txid_vout) that contains the inscription
        - content_type (str): MIME type of the inscribed content
        - content_bytes (int): Size of the inscribed content in bytes
        - content (str): Base64-encoded representation of the inscribed data
        - timestamp (str): Timestamp when the inscription was confirmed (ISO 8601)
        - block_height (int): Block height at which the inscription was confirmed
        - genesis_transaction (str): Transaction ID where the inscription was created
        - genesis_address (str): Bitcoin address that created the inscription
        - current_owner (str): Current owner's Bitcoin address
        - location (str): Current outpoint where the inscription is located
        - offset (int): Byte offset within the transaction
        - is_cursed (bool): Whether the inscription is cursed
        - is_unsafe (bool): Whether the inscription is unsafe
        - sat_ordinal (str): Ordinal number of the inscribed satoshi
        - sat_rarity (str): Rarity level of the sat
        - sat_coinbase_height (int): Block height when the satoshi was mined
        - parent (str): ID of parent inscription if any
        - metadata_name (str): Name from metadata
        - metadata_description (str): Description from metadata
        - metadata_collection (str): Collection name from metadata
        - metadata_creator (str): Creator from metadata
        - flag_0 (str): First flag (e.g., 'transferred')
        - flag_1 (str): Second flag (e.g., 'explicit_content')
    """
    # Generate realistic mock data
    txid = ''.join(random.choices('0123456789abcdef', k=64))
    vout = str(random.randint(0, 10))
    height = random.randint(700000, 800000)
    
    # Random timestamp in the last 2 years
    start_date = datetime.now() - timedelta(days=730)
    random_seconds = random.randint(0, 730*24*3600)
    timestamp = (start_date + timedelta(seconds=random_seconds)).isoformat()

    # Random content type
    content_types = ['image/png', 'image/jpeg', 'text/html', 'application/json', 'text/plain']
    ctype = random.choice(content_types)
    
    # Generate base64-encoded dummy content
    content_size = random.randint(100, 5000)
    dummy_data = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=content_size))
    content_b64 = base64.b64encode(dummy_data.encode()).decode()

    # Rarity levels
    rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']
    
    # Flags
    all_flags = ['transferred', 'explicit_content', 'verified', 'locked', 'burned']
    chosen_flags = random.sample(all_flags, 2)

    return {
        "inscription_id": f"{txid}i{vout}",
        "outpoint": f"{txid}:{vout}",
        "content_type": ctype,
        "content_bytes": content_size,
        "content": content_b64,
        "timestamp": timestamp,
        "block_height": height,
        "genesis_transaction": txid,
        "genesis_address": f"1{ ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=33)) }",
        "current_owner": f"1{ ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=33)) }",
        "location": f"{txid}:{vout}",
        "offset": random.randint(0, 1000),
        "is_cursed": random.choice([True, False]),
        "is_unsafe": random.choice([True, False]),
        "sat_ordinal": str(random.randint(10**12, 10**15)),
        "sat_rarity": random.choice(rarities),
        "sat_coinbase_height": random.randint(1, 700000),
        "parent": f"{ ''.join(random.choices('0123456789abcdef', k=64)) }i{random.randint(0,10)}" if random.random() < 0.3 else "",
        "metadata_name": f"Ordinal #{random.randint(1, 10000)}",
        "metadata_description": f"A rare digital artifact inscribed on Bitcoin SV blockchain at block {height}.",
        "metadata_collection": "BSV Genesis Collection" if random.random() < 0.5 else "Digital Artifacts 2023",
        "metadata_creator": f"1{ ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=33)) }",
        "flag_0": chosen_flags[0],
        "flag_1": chosen_flags[1]
    }


def bitcoin_sv_tools_server_ordinals_getInscription(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific ordinal inscription by its outpoint.
    
    This function simulates querying a server for Bitcoin SV ordinal inscription data.
    It returns complete inscription data including content type, file information,
    inscription origin, and current status. Useful for verifying NFT authenticity
    or retrieving metadata about digital artifacts.

    Args:
        args (Dict[str, Any]): Input parameters for the query. Expected to contain:
            - outpoint (str): The transaction outpoint (txid:vout) of the inscription
            - network (str, optional): Blockchain network ('main', 'test'). Default: 'main'
            - include_content (bool, optional): Whether to include base64-encoded content. Default: True

    Returns:
        Dict[str, Any]: Complete inscription data with the following structure:
            - inscription_id (str): Unique identifier for the inscription
            - outpoint (str): The outpoint (txid_vout) that contains the inscription
            - content_type (str): MIME type of the inscribed content
            - content_bytes (int): Size of the inscribed content in bytes
            - content (str): Base64-encoded representation of the inscribed data
            - timestamp (str): Timestamp when the inscription was confirmed (ISO 8601)
            - block_height (int): Block height at which the inscription was confirmed
            - genesis_transaction (str): Transaction ID where the inscription was created
            - genesis_address (str): Bitcoin address that created the inscription
            - current_owner (str): Current owner's Bitcoin address
            - location (str): Current outpoint where the inscription is located
            - offset (int): Byte offset within the transaction
            - is_cursed (bool): Whether the inscription is cursed
            - is_unsafe (bool): Whether the inscription is unsafe
            - sat_ordinal (str): Ordinal number of the inscribed satoshi
            - sat_rarity (str): Rarity level of the sat
            - sat_coinbase_height (int): Block height when the satoshi was mined
            - parent (str): ID of parent inscription if any
            - metadata (Dict): Additional key-value pairs (name, description, collection, creator)
            - flags (List[str]): List of flags applied to the inscription
    """
    # Input validation
    if not isinstance(args, dict):
        raise TypeError("args must be a dictionary")
    
    if "outpoint" not in args:
        raise ValueError("Missing required parameter: outpoint")
    
    if not isinstance(args["outpoint"], str) or ":" not in args["outpoint"]:
        raise ValueError("outpoint must be a string in format 'txid:vout'")
    
    # Optional parameters with defaults
    include_content = args.get("include_content", True)
    if not isinstance(include_content, bool):
        raise ValueError("include_content must be a boolean")
    
    network = args.get("network", "main")
    if network not in ["main", "test"]:
        raise ValueError("network must be 'main' or 'test'")
    
    # Call external API (mocked)
    api_data = call_external_api("bitcoin-sv-tools-server-ordinals_getInscription")
    
    # Construct metadata dictionary
    metadata = {
        "name": api_data["metadata_name"],
        "description": api_data["metadata_description"]
    }
    
    # Add collection and creator if available
    if api_data.get("metadata_collection"):
        metadata["collection"] = api_data["metadata_collection"]
    if api_data.get("metadata_creator"):
        metadata["creator"] = api_data["metadata_creator"]
    
    # Construct flags list
    flags = []
    if api_data.get("flag_0"):
        flags.append(api_data["flag_0"])
    if api_data.get("flag_1"):
        flags.append(api_data["flag_1"])
    
    # Build final result structure
    result = {
        "inscription_id": api_data["inscription_id"],
        "outpoint": api_data["outpoint"],
        "content_type": api_data["content_type"],
        "content_bytes": api_data["content_bytes"],
        "content": api_data["content"] if include_content else "",
        "timestamp": api_data["timestamp"],
        "block_height": api_data["block_height"],
        "genesis_transaction": api_data["genesis_transaction"],
        "genesis_address": api_data["genesis_address"],
        "current_owner": api_data["current_owner"],
        "location": api_data["location"],
        "offset": api_data["offset"],
        "is_cursed": api_data["is_cursed"],
        "is_unsafe": api_data["is_unsafe"],
        "sat_ordinal": api_data["sat_ordinal"],
        "sat_rarity": api_data["sat_rarity"],
        "sat_coinbase_height": api_data["sat_coinbase_height"],
        "parent": api_data["parent"],
        "metadata": metadata,
        "flags": flags
    }
    
    return result