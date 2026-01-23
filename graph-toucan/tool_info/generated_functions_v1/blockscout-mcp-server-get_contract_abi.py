from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for contract ABI retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - abi_0_type (str): Type of first ABI entry (e.g., 'function')
        - abi_0_name (str): Name of first ABI entry
        - abi_0_stateMutability (str): State mutability of first function
        - abi_0_anonymous (bool): Anonymous flag if event
        - abi_1_type (str): Type of second ABI entry
        - abi_1_name (str): Name of second ABI entry
        - abi_1_stateMutability (str): State mutability of second function
        - abi_1_anonymous (bool): Anonymous flag if event
        - contract_address (str): Contract address
        - chain_id (str): Blockchain network ID
        - fetched_at (str): ISO 8601 timestamp when ABI was fetched
        - is_verified (bool): Whether contract is verified
        - input_0_name (str): Name of first input parameter in first function
        - input_0_type (str): Type of first input parameter
        - input_0_indexed (bool): Whether first input is indexed (for events)
        - input_1_name (str): Name of second input parameter
        - input_1_type (str): Type of second input parameter
        - input_1_indexed (bool): Whether second input is indexed
        - output_0_name (str): Name of first output parameter
        - output_0_type (str): Type of first output parameter
        - output_1_name (str): Name of second output parameter
        - output_1_type (str): Type of second output parameter
    """
    return {
        "abi_0_type": "function",
        "abi_0_name": "transfer",
        "abi_0_stateMutability": "nonpayable",
        "abi_0_anonymous": False,
        "abi_1_type": "event",
        "abi_1_name": "Transfer",
        "abi_1_stateMutability": "",
        "abi_1_anonymous": False,
        "contract_address": "0x1234567890123456789012345678901234567890",
        "chain_id": "1",
        "fetched_at": datetime.now().isoformat(),
        "is_verified": True,
        "input_0_name": "to",
        "input_0_type": "address",
        "input_0_indexed": False,
        "input_1_name": "value",
        "input_1_type": "uint256",
        "input_1_indexed": False,
        "output_0_name": "success",
        "output_0_type": "bool",
        "output_1_name": "",
        "output_1_type": ""
    }

def blockscout_mcp_server_get_contract_abi(address: str, chain_id: str) -> Dict[str, Any]:
    """
    Get smart contract ABI (Application Binary Interface).
    
    The ABI defines all functions, events, their parameters, and return types.
    It is required to format function calls or interpret contract data.
    
    Args:
        address (str): Smart contract address
        chain_id (str): The ID of the blockchain
    
    Returns:
        Dict containing:
        - abi (List[Dict]): List of ABI entries representing functions, events, or constructor
        - contract_address (str): The blockchain address of the smart contract
        - chain_id (str): The ID of the blockchain network
        - fetched_at (str): ISO 8601 timestamp when ABI was fetched
        - is_verified (bool): Whether contract source code is verified
    
    Each ABI entry contains:
    - type (str): 'function', 'event', 'constructor', etc.
    - name (str): Name of function/event
    - inputs (List[Dict]): List of input parameters with 'name', 'type', 'indexed'
    - outputs (List[Dict]): List of output parameters with 'name', 'type'
    - stateMutability (str): For functions: 'pure', 'view', 'nonpayable', 'payable'
    - anonymous (bool): For events only, indicates if event is anonymous
    """
    # Input validation
    if not address:
        raise ValueError("Address is required")
    if not chain_id:
        raise ValueError("Chain ID is required")
    
    # Call external API to get flattened data
    api_data = call_external_api("blockscout-mcp-server-get_contract_abi")
    
    # Construct inputs for first ABI entry
    inputs_0 = [
        {
            "name": api_data["input_0_name"],
            "type": api_data["input_0_type"],
            "indexed": api_data["input_0_indexed"]
        },
        {
            "name": api_data["input_1_name"],
            "type": api_data["input_1_type"],
            "indexed": api_data["input_1_indexed"]
        }
    ]
    
    # Construct outputs for first ABI entry
    outputs_0 = [
        {
            "name": api_data["output_0_name"],
            "type": api_data["output_0_type"]
        }
    ]
    
    # Only include non-empty output
    if api_data["output_1_name"] or api_data["output_1_type"]:
        outputs_0.append({
            "name": api_data["output_1_name"],
            "type": api_data["output_1_type"]
        })
    
    # Construct second ABI entry (event) inputs
    event_inputs = [
        {
            "name": api_data["input_0_name"],
            "type": api_data["input_0_type"],
            "indexed": True  # Typically 'to' is indexed in Transfer event
        },
        {
            "name": api_data["input_1_name"],
            "type": api_data["input_1_type"],
            "indexed": False
        }
    ]
    
    # Build ABI list
    abi = [
        {
            "type": api_data["abi_0_type"],
            "name": api_data["abi_0_name"],
            "inputs": inputs_0,
            "outputs": outputs_0,
            "stateMutability": api_data["abi_0_stateMutability"],
        },
        {
            "type": api_data["abi_1_type"],
            "name": api_data["abi_1_name"],
            "inputs": event_inputs,
            "anonymous": api_data["abi_1_anonymous"],
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "abi": abi,
        "contract_address": api_data["contract_address"],
        "chain_id": api_data["chain_id"],
        "fetched_at": api_data["fetched_at"],
        "is_verified": api_data["is_verified"]
    }
    
    return result