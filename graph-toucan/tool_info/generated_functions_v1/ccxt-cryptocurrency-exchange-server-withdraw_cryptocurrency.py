from typing import Dict, Any, Optional
import time
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cryptocurrency withdrawal.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - withdrawal_id (str): Unique identifier for the withdrawal transaction
        - currency (str): Currency code withdrawn (e.g., 'BTC', 'ETH')
        - amount (float): Amount withdrawn
        - address (str): Destination address
        - tag (str): Optional tag/memo if applicable
        - network (str): Blockchain network used (e.g., 'ERC20', 'BEP20')
        - status (str): Current status of withdrawal
        - timestamp (int): Unix timestamp in milliseconds
        - datetime (str): ISO 8601 datetime string
        - fee_amount (float): Transaction fee amount
        - fee_currency (str): Currency of the fee
        - info_withdrawalId (str): Raw withdrawal ID from exchange
        - info_txid (str): Transaction hash if available
        - additional_params_feeToUser (bool): Example additional parameter
        - additional_params_internalId (str): Internal tracking ID
    """
    timestamp_ms = int(time.time() * 1000)
    withdrawal_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    txid = ''.join(random.choices(string.hexdigits.lower(), k=64))
    networks = ['ERC20', 'BEP20', 'TRC20', 'Polygon', 'Solana']
    statuses = ['pending', 'succeeded', 'failed', 'canceled']

    return {
        "withdrawal_id": f"WD{withdrawal_id}",
        "currency": "BTC",
        "amount": 0.005,
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "tag": "",
        "network": random.choice(networks),
        "status": random.choice(statuses),
        "timestamp": timestamp_ms,
        "datetime": time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime()),
        "fee_amount": round(random.uniform(0.0001, 0.001), 6),
        "fee_currency": "BTC",
        "info_withdrawalId": f"WD{withdrawal_id}",
        "info_txid": txid,
        "additional_params_feeToUser": False,
        "additional_params_internalId": ''.join(random.choices(string.digits, k=10))
    }


def ccxt_cryptocurrency_exchange_server_withdraw_cryptocurrency(
    address: str,
    amount: float,
    code: str,
    exchange_id: str,
    api_key: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    passphrase: Optional[str] = None,
    secret_key: Optional[str] = None,
    tag: Optional[str] = None
) -> Dict[str, Any]:
    """
    Initiates a cryptocurrency withdrawal to a specified address using a cryptocurrency exchange API.

    This function simulates the withdrawal process via an external API call. It validates inputs,
    constructs the request, and returns a structured response mimicking real exchange behavior.

    Args:
        address (str): The destination address for the withdrawal. Required.
        amount (float): The amount of currency to withdraw. Must be greater than 0. Required.
        code (str): Currency code for the withdrawal (e.g., 'BTC', 'ETH'). Required.
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'ftx'). Case-insensitive. Required.
        api_key (Optional[str]): API key with withdrawal permissions. Optional if pre-configured.
        params (Optional[Dict[str, Any]]): Extra parameters like network (e.g., {'network': 'BEP20'}).
        passphrase (Optional[str]): API passphrase if required by the exchange.
        secret_key (Optional[str]): Secret key for API authentication.
        tag (Optional[str]): Destination tag, memo, or payment ID for certain currencies.

    Returns:
        Dict[str, Any]: A dictionary containing withdrawal details with the following structure:
            - withdrawal_id (str): Unique identifier assigned by the exchange.
            - currency (str): Currency code withdrawn.
            - amount (float): Amount successfully withdrawn.
            - address (str): Destination address.
            - tag (str): Optional tag/memo used.
            - network (str): Blockchain network used.
            - status (str): Current status ('pending', 'succeeded', etc.).
            - timestamp (int): Unix timestamp in milliseconds.
            - datetime (str): ISO 8601 datetime string.
            - fee (Dict): Fee details including amount and currency.
            - info (Dict): Raw response data from the exchange.
            - additional_params (Dict): Other exchange-specific fields.

    Raises:
        ValueError: If required fields are missing or invalid (e.g., amount <= 0, empty address/code).
    """
    # Input validation
    if not address:
        raise ValueError("Address is required and cannot be empty.")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")
    if not code:
        raise ValueError("Currency code (code) is required.")
    if not exchange_id:
        raise ValueError("Exchange ID is required.")

    # Normalize exchange_id to lowercase
    exchange_id = exchange_id.lower().strip()

    # Simulate calling external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-withdraw_cryptocurrency")

    # Construct nested output structure as per schema
    result = {
        "withdrawal_id": api_data["withdrawal_id"],
        "currency": code,
        "amount": amount,
        "address": address,
        "tag": tag or api_data["tag"],
        "network": params.get("network", api_data["network"]) if params else api_data["network"],
        "status": api_data["status"],
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "fee": {
            "amount": api_data["fee_amount"],
            "currency": api_data["fee_currency"]
        },
        "info": {
            "withdrawalId": api_data["info_withdrawalId"],
            "txid": api_data["info_txid"]
        },
        "additional_params": {
            "feeToUser": api_data["additional_params_feeToUser"],
            "internalId": api_data["additional_params_internalId"]
        }
    }

    return result