from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching decoded Bitcoin SV transaction data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - transaction_id (str): The unique identifier (txid) of the decoded Bitcoin SV transaction
        - version (int): The transaction version number indicating format and capabilities
        - lock_time (int): The block height or timestamp when the transaction is finalized for inclusion
        - input_0_prev_txid (str): Previous transaction ID for first input
        - input_0_output_index (int): Output index in previous transaction for first input
        - input_0_script_sig (str): Script signature of first input
        - input_0_sequence (int): Sequence number of first input
        - input_0_address (str): Address used in first input, if available
        - input_0_value (float): Value of first input in BSV, if available
        - input_0_is_coinbase (bool): Whether the first input is a coinbase input
        - output_0_value (float): Value of first output in BSV
        - output_0_script_pubkey (str): Script pubkey of first output
        - output_0_address (str): Address of first output
        - output_0_type (str): Type of first output (e.g., P2PKH, OP_RETURN)
        - fee (float): Transaction fee in BSV, calculated as sum of inputs minus outputs
        - fee_rate (float): Fee rate in satoshis per byte
        - size (int): Size of the transaction in bytes
        - virtual_size (int): Virtual size of the transaction for fee calculation purposes
        - block_hash (str): Hash of the block containing this transaction; null if unconfirmed
        - block_height (int): Block number where transaction was confirmed; null if unconfirmed
        - confirmations (int): Number of confirmations on the blockchain
        - timestamp (str): ISO 8601 timestamp of when the transaction was included in a block; null if unconfirmed
        - raw_hex (str): Raw hexadecimal representation of the transaction
        - is_coinbase_transaction (bool): Indicates whether this is a coinbase (mining reward) transaction
        - has_op_return (bool): Indicates if the transaction contains an OP_RETURN output for metadata
        - op_return_data_0 (str): First decoded data string from OP_RETURN outputs, if present
        - script_analysis_input_count_by_type (str): JSON string of input script type counts
        - script_analysis_output_count_by_type (str): JSON string of output script type counts
        - script_analysis_common_patterns (str): Common script patterns detected
        - network (str): Identified network (e.g., 'mainnet', 'testnet') based on context and addresses
        - status (str): Decoding status: 'success', 'partial', or 'error'
        - error_message (str): Description of any decoding issues if status is not 'success'
    """
    return {
        "transaction_id": "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",
        "version": 1,
        "lock_time": 550000,
        "input_0_prev_txid": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890",
        "input_0_output_index": 0,
        "input_0_script_sig": "483045022100e2ac...",
        "input_0_sequence": 4294967295,
        "input_0_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "input_0_value": 50.0,
        "input_0_is_coinbase": False,
        "output_0_value": 45.0,
        "output_0_script_pubkey": "76a914010966776006953d5567439e5e39f86a0d273bee88ac",
        "output_0_address": "1HLoD9E4SDFFPDiYfNYnkstGoZRGwNQq17",
        "output_0_type": "P2PKH",
        "fee": 5.0,
        "fee_rate": 100.0,
        "size": 225,
        "virtual_size": 225,
        "block_hash": "00000000000000000007f8a8f1b1b1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1",
        "block_height": 550001,
        "confirmations": 100,
        "timestamp": "2023-04-05T12:34:56Z",
        "raw_hex": "0100000001a1b2c3d4...",
        "is_coinbase_transaction": False,
        "has_op_return": True,
        "op_return_data_0": "Hello Bitcoin SV",
        "script_analysis_input_count_by_type": '{"P2PKH": 1}',
        "script_analysis_output_count_by_type": '{"P2PKH": 1, "OP_RETURN": 1}',
        "script_analysis_common_patterns": "Standard P2PKH spend with OP_RETURN metadata",
        "network": "mainnet",
        "status": "success",
        "error_message": ""
    }

def bitcoin_sv_tools_server_bsv_decodeTransaction(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decodes and analyzes Bitcoin SV transactions to provide detailed insights.
    
    This function accepts either a transaction ID or raw transaction data and returns comprehensive
    information including inputs, outputs, fee calculations, script details, and blockchain context.
    It supports both hex and base64 encoded transactions and automatically fetches additional
    on-chain data when available.
    
    Args:
        args (Dict[str, Any]): Input parameters containing either:
            - 'txid' (str): Transaction ID to fetch and decode
            - 'raw_tx' (str): Raw transaction data in hex or base64 format
            - 'encoding' (str, optional): Encoding type ('hex' or 'base64'), defaults to 'hex'
    
    Returns:
        Dict[str, Any]: Decoded transaction data with the following structure:
            - transaction_id (str): Unique identifier (txid) of the transaction
            - version (int): Transaction version number
            - lock_time (int): Block height or timestamp for finalization
            - inputs (List[Dict]): List of input objects with prev_txid, output_index, script_sig,
              sequence, address, value, is_coinbase
            - outputs (List[Dict]): List of output objects with value, script_pubkey, address, type
            - fee (float): Transaction fee in BSV
            - fee_rate (float): Fee rate in satoshis per byte
            - size (int): Size of transaction in bytes
            - virtual_size (int): Virtual size for fee calculation
            - block_hash (str): Block hash containing transaction (null if unconfirmed)
            - block_height (int): Block number where confirmed (null if unconfirmed)
            - confirmations (int): Number of confirmations
            - timestamp (str): ISO 8601 timestamp of block inclusion (null if unconfirmed)
            - raw_hex (str): Raw hexadecimal representation
            - is_coinbase_transaction (bool): Whether it's a coinbase transaction
            - has_op_return (bool): Whether it contains OP_RETURN output
            - op_return_data (List[str]): List of decoded OP_RETURN data strings
            - script_analysis (Dict): Analysis of scripts with input/output counts and patterns
            - network (str): Identified network (mainnet/testnet)
            - status (str): Decoding status ('success', 'partial', 'error')
            - error_message (str): Description of any decoding issues
    """
    try:
        # Validate input
        if not isinstance(args, dict):
            return {
                "transaction_id": "",
                "version": 0,
                "lock_time": 0,
                "inputs": [],
                "outputs": [],
                "fee": 0.0,
                "fee_rate": 0.0,
                "size": 0,
                "virtual_size": 0,
                "block_hash": None,
                "block_height": None,
                "confirmations": 0,
                "timestamp": None,
                "raw_hex": "",
                "is_coinbase_transaction": False,
                "has_op_return": False,
                "op_return_data": [],
                "script_analysis": {
                    "input_count_by_type": {},
                    "output_count_by_type": {},
                    "common_patterns": ""
                },
                "network": "unknown",
                "status": "error",
                "error_message": "Invalid input: args must be a dictionary"
            }
        
        # Check for required parameters
        if 'txid' not in args and 'raw_tx' not in args:
            return {
                "transaction_id": "",
                "version": 0,
                "lock_time": 0,
                "inputs": [],
                "outputs": [],
                "fee": 0.0,
                "fee_rate": 0.0,
                "size": 0,
                "virtual_size": 0,
                "block_hash": None,
                "block_height": None,
                "confirmations": 0,
                "timestamp": None,
                "raw_hex": "",
                "is_coinbase_transaction": False,
                "has_op_return": False,
                "op_return_data": [],
                "script_analysis": {
                    "input_count_by_type": {},
                    "output_count_by_type": {},
                    "common_patterns": ""
                },
                "network": "unknown",
                "status": "error",
                "error_message": "Either 'txid' or 'raw_tx' parameter is required"
            }
        
        # Call external API to get transaction data
        api_data = call_external_api("bitcoin-sv-tools-server-bsv_decodeTransaction")
        
        # Construct inputs list
        inputs = []
        if "input_0_prev_txid" in api_data:
            inputs.append({
                "prev_txid": api_data["input_0_prev_txid"],
                "output_index": api_data["input_0_output_index"],
                "script_sig": api_data["input_0_script_sig"],
                "sequence": api_data["input_0_sequence"],
                "address": api_data["input_0_address"] if "input_0_address" in api_data else None,
                "value": api_data["input_0_value"] if "input_0_value" in api_data else None,
                "is_coinbase": api_data["input_0_is_coinbase"]
            })
        
        # Construct outputs list
        outputs = []
        if "output_0_value" in api_data:
            outputs.append({
                "value": api_data["output_0_value"],
                "script_pubkey": api_data["output_0_script_pubkey"],
                "address": api_data["output_0_address"] if "output_0_address" in api_data else None,
                "type": api_data["output_0_type"]
            })
        
        # Construct op_return_data list
        op_return_data = []
        if api_data.get("has_op_return", False) and "op_return_data_0" in api_data:
            op_return_data.append(api_data["op_return_data_0"])
        
        # Parse script analysis JSON strings if present, otherwise use defaults
        import json
        try:
            input_count_by_type = json.loads(api_data["script_analysis_input_count_by_type"]) if "script_analysis_input_count_by_type" in api_data else {}
        except:
            input_count_by_type = {}
        
        try:
            output_count_by_type = json.loads(api_data["script_analysis_output_count_by_type"]) if "script_analysis_output_count_by_type" in api_data else {}
        except:
            output_count_by_type = {}
        
        # Build final result
        result = {
            "transaction_id": api_data["transaction_id"],
            "version": api_data["version"],
            "lock_time": api_data["lock_time"],
            "inputs": inputs,
            "outputs": outputs,
            "fee": float(api_data["fee"]),
            "fee_rate": float(api_data["fee_rate"]),
            "size": int(api_data["size"]),
            "virtual_size": int(api_data["virtual_size"]),
            "block_hash": api_data["block_hash"] if api_data["block_hash"] else None,
            "block_height": api_data["block_height"] if api_data["block_height"] else None,
            "confirmations": int(api_data["confirmations"]),
            "timestamp": api_data["timestamp"] if api_data["timestamp"] else None,
            "raw_hex": api_data["raw_hex"],
            "is_coinbase_transaction": bool(api_data["is_coinbase_transaction"]),
            "has_op_return": bool(api_data["has_op_return"]),
            "op_return_data": op_return_data,
            "script_analysis": {
                "input_count_by_type": input_count_by_type,
                "output_count_by_type": output_count_by_type,
                "common_patterns": api_data.get("script_analysis_common_patterns", "")
            },
            "network": api_data["network"],
            "status": api_data["status"],
            "error_message": api_data["error_message"] if api_data["error_message"] else ""
        }
        
        return result
        
    except Exception as e:
        return {
            "transaction_id": "",
            "version": 0,
            "lock_time": 0,
            "inputs": [],
            "outputs": [],
            "fee": 0.0,
            "fee_rate": 0.0,
            "size": 0,
            "virtual_size": 0,
            "block_hash": None,
            "block_height": None,
            "confirmations": 0,
            "timestamp": None,
            "raw_hex": "",
            "is_coinbase_transaction": False,
            "has_op_return": False,
            "op_return_data": [],
            "script_analysis": {
                "input_count_by_type": {},
                "output_count_by_type": {},
                "common_patterns": ""
            },
            "network": "unknown",
            "status": "error",
            "error_message": f"Unexpected error during transaction decoding: {str(e)}"
        }