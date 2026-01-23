from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for transaction summary.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - summary (str): Human-readable description of the transaction
        - category (str): High-level classification of the transaction type
        - detected_protocols_0 (str): First detected protocol name
        - detected_protocols_1 (str): Second detected protocol name
        - involved_tokens_0_symbol (str): Symbol of first involved token
        - involved_tokens_0_amount (str): Amount of first involved token
        - involved_tokens_0_contract_address (str): Contract address of first token
        - involved_tokens_0_decimals (int): Decimals of first token
        - involved_tokens_1_symbol (str): Symbol of second involved token
        - involved_tokens_1_amount (str): Amount of second involved token
        - involved_tokens_1_contract_address (str): Contract address of second token
        - involved_tokens_1_decimals (int): Decimals of second token
        - nfts_0_collection_name (str): Collection name of first NFT
        - nfts_0_token_id (str): Token ID of first NFT
        - nfts_0_contract_address (str): Contract address of first NFT
        - nfts_0_action (str): Action type for first NFT ('mint', 'sale', 'transfer')
        - nfts_1_collection_name (str): Collection name of second NFT
        - nfts_1_token_id (str): Token ID of second NFT
        - nfts_1_contract_address (str): Contract address of second NFT
        - nfts_1_action (str): Action type for second NFT ('mint', 'sale', 'transfer')
        - raw_events_count (int): Total number of blockchain events/logs
        - success (bool): Whether the transaction was successfully interpreted
        - error (str): Error message if interpretation failed, otherwise None
        - confidence (str): Confidence level ('high', 'medium', 'low')
        - timestamp (str): ISO 8601 timestamp when summary was generated
    """
    return {
        "summary": "Swapped ETH for DAI on Uniswap",
        "category": "swap",
        "detected_protocols_0": "Uniswap",
        "detected_protocols_1": "WETH Gateway",
        "involved_tokens_0_symbol": "ETH",
        "involved_tokens_0_amount": "0.5",
        "involved_tokens_0_contract_address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "involved_tokens_0_decimals": 18,
        "involved_tokens_1_symbol": "DAI",
        "involved_tokens_1_amount": "1500.25",
        "involved_tokens_1_contract_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "involved_tokens_1_decimals": 18,
        "nfts_0_collection_name": "",
        "nfts_0_token_id": "",
        "nfts_0_contract_address": "",
        "nfts_0_action": "",
        "nfts_1_collection_name": "",
        "nfts_1_token_id": "",
        "nfts_1_contract_address": "",
        "nfts_1_action": "",
        "raw_events_count": 4,
        "success": True,
        "error": None,
        "confidence": "high",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def blockscout_mcp_server_transaction_summary(chain_id: str, transaction_hash: str) -> Dict[str, Any]:
    """
    Get human-readable transaction summaries from Blockscout Transaction Interpreter.
    
    Automatically classifies transactions into natural language descriptions such as
    transfers, swaps, NFT sales, and DeFi operations. Essential for rapid transaction
    comprehension, dashboard displays, and initial analysis.
    
    Note: Not all transactions can be summarized and accuracy is not guaranteed for complex patterns.

    Args:
        chain_id (str): The ID of the blockchain
        transaction_hash (str): Transaction hash

    Returns:
        Dict containing:
        - summary (str): Human-readable natural language description of the transaction purpose
        - category (str): High-level classification of the transaction type
        - detected_protocols (List[str]): Names of detected DeFi protocols or applications
        - involved_tokens (List[Dict]): List of tokens involved with symbol, amount, contract_address, decimals
        - nfts (List[Dict]): List of NFTs involved with collection_name, token_id, contract_address, action
        - raw_events_count (int): Total number of blockchain events/logs emitted
        - success (bool): Whether the transaction was successfully processed and interpreted
        - error (Optional[str]): Error message if interpretation failed, otherwise None
        - confidence (str): Confidence level ('high', 'medium', 'low')
        - timestamp (str): ISO 8601 timestamp when the summary was generated
    """
    # Input validation
    if not chain_id or not isinstance(chain_id, str):
        raise ValueError("chain_id must be a non-empty string")
    if not transaction_hash or not isinstance(transaction_hash, str):
        raise ValueError("transaction_hash must be a non-empty string")

    # Call external API to get flat data
    api_data = call_external_api("blockscout-mcp-server-transaction_summary")

    # Construct detected_protocols list
    detected_protocols = []
    if api_data.get("detected_protocols_0"):
        detected_protocols.append(api_data["detected_protocols_0"])
    if api_data.get("detected_protocols_1"):
        detected_protocols.append(api_data["detected_protocols_1"])

    # Construct involved_tokens list
    involved_tokens = []
    if api_data.get("involved_tokens_0_symbol"):
        involved_tokens.append({
            "symbol": api_data["involved_tokens_0_symbol"],
            "amount": api_data["involved_tokens_0_amount"],
            "contract_address": api_data["involved_tokens_0_contract_address"],
            "decimals": api_data["involved_tokens_0_decimals"]
        })
    if api_data.get("involved_tokens_1_symbol"):
        involved_tokens.append({
            "symbol": api_data["involved_tokens_1_symbol"],
            "amount": api_data["involved_tokens_1_amount"],
            "contract_address": api_data["involved_tokens_1_contract_address"],
            "decimals": api_data["involved_tokens_1_decimals"]
        })

    # Construct nfts list
    nfts = []
    if api_data.get("nfts_0_collection_name") and api_data["nfts_0_collection_name"].strip():
        nfts.append({
            "collection_name": api_data["nfts_0_collection_name"],
            "token_id": api_data["nfts_0_token_id"],
            "contract_address": api_data["nfts_0_contract_address"],
            "action": api_data["nfts_0_action"]
        })
    if api_data.get("nfts_1_collection_name") and api_data["nfts_1_collection_name"].strip():
        nfts.append({
            "collection_name": api_data["nfts_1_collection_name"],
            "token_id": api_data["nfts_1_token_id"],
            "contract_address": api_data["nfts_1_contract_address"],
            "action": api_data["nfts_1_action"]
        })

    # Build final result structure
    result = {
        "summary": api_data["summary"],
        "category": api_data["category"],
        "detected_protocols": detected_protocols,
        "involved_tokens": involved_tokens,
        "nfts": nfts,
        "raw_events_count": api_data["raw_events_count"],
        "success": api_data["success"],
        "error": api_data["error"],
        "confidence": api_data["confidence"],
        "timestamp": api_data["timestamp"]
    }

    return result