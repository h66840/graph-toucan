from typing import Dict, List, Any
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for coin information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - code (str): response status code
        - msg (str): human-readable message
        - requestTime (int): timestamp in milliseconds
        - data_0_coinId (str): unique identifier for the coin
        - data_0_coin (str): name of the cryptocurrency
        - data_0_transfer (str): transferability ("true" or "false")
        - data_0_areaCoin (str): region restriction ("yes" or "no")
        - data_0_chains_0_chain (str): blockchain name
        - data_0_chains_0_needTag (str): tag required ("true" or "false")
        - data_0_chains_0_withdrawable (str): withdrawal supported
        - data_0_chains_0_rechargeable (str): deposit supported
        - data_0_chains_0_withdrawFee (str): withdrawal fee
        - data_0_chains_0_extraWithdrawFee (str): extra withdrawal fee
        - data_0_chains_0_depositConfirm (str): deposit confirmation count
        - data_0_chains_0_withdrawConfirm (str): withdrawal confirmation count
        - data_0_chains_0_minDepositAmount (str): minimum deposit amount
        - data_0_chains_0_minWithdrawAmount (str): minimum withdrawal amount
        - data_0_chains_0_browserUrl (str): blockchain explorer URL
        - data_0_chains_0_contractAddress (str): contract address or "null"
        - data_0_chains_0_withdrawStep (str): withdrawal step increment
        - data_0_chains_0_withdrawMinScale (str): minimum decimal precision
        - data_0_chains_0_congestion (str): network status ("normal" or "congested")
    """
    return {
        "code": "200",
        "msg": "Success",
        "requestTime": int(time.time() * 1000),
        "data_0_coinId": "solana-123",
        "data_0_coin": "SOL",
        "data_0_transfer": "true",
        "data_0_areaCoin": "no",
        "data_0_chains_0_chain": "SOL",
        "data_0_chains_0_needTag": "false",
        "data_0_chains_0_withdrawable": "true",
        "data_0_chains_0_rechargeable": "true",
        "data_0_chains_0_withdrawFee": "0.01",
        "data_0_chains_0_extraWithdrawFee": "0.0",
        "data_0_chains_0_depositConfirm": "1",
        "data_0_chains_0_withdrawConfirm": "1",
        "data_0_chains_0_minDepositAmount": "0.001",
        "data_0_chains_0_minWithdrawAmount": "0.01",
        "data_0_chains_0_browserUrl": "https://explorer.solana.com",
        "data_0_chains_0_contractAddress": "null",
        "data_0_chains_0_withdrawStep": "0",
        "data_0_chains_0_withdrawMinScale": "9",
        "data_0_chains_0_congestion": "normal"
    }


def coin_mcp_server_getCoinInfo(coin: str) -> Dict[str, Any]:
    """
    Get spot coin information for a given cryptocurrency.

    Args:
        coin (str): The name of the coin to retrieve information for (e.g., "SOL", "ETH").

    Returns:
        Dict containing:
        - code (str): response status code indicating success or error
        - msg (str): human-readable message describing the result
        - requestTime (int): timestamp in milliseconds when the request was processed
        - data (List[Dict]): list of coin information objects with supported chains

    Each data item contains:
        - coinId (str): unique identifier for the coin
        - coin (str): name of the cryptocurrency
        - transfer (str): transferability ("true" or "false")
        - areaCoin (str): region restriction ("yes" or "no")
        - chains (List[Dict]): list of blockchain networks supporting this coin

    Each chain contains:
        - chain (str): blockchain name
        - needTag (str): whether a tag is required
        - withdrawable (str): whether withdrawals are supported
        - rechargeable (str): whether deposits are supported
        - withdrawFee (str): fixed withdrawal fee
        - extraWithdrawFee (str): additional fee or burn rate
        - depositConfirm (str): required deposit confirmations
        - withdrawConfirm (str): required withdrawal confirmations
        - minDepositAmount (str): minimum deposit amount
        - minWithdrawAmount (str): minimum withdrawal amount
        - browserUrl (str): blockchain explorer URL
        - contractAddress (str or None): token contract address or null
        - withdrawStep (str): withdrawal amount step
        - withdrawMinScale (str): minimum decimal precision
        - congestion (str): network status ("normal" or "congested")
    """
    # Input validation
    if not coin or not isinstance(coin, str):
        return {
            "code": "400",
            "msg": "Invalid input: coin must be a non-empty string",
            "requestTime": int(time.time() * 1000),
            "data": []
        }

    try:
        # Call external API to get flat data
        api_data = call_external_api("coin-mcp-server-getCoinInfo")

        # Construct chains list from indexed fields
        chains = [
            {
                "chain": api_data["data_0_chains_0_chain"],
                "needTag": api_data["data_0_chains_0_needTag"],
                "withdrawable": api_data["data_0_chains_0_withdrawable"],
                "rechargeable": api_data["data_0_chains_0_rechargeable"],
                "withdrawFee": api_data["data_0_chains_0_withdrawFee"],
                "extraWithdrawFee": api_data["data_0_chains_0_extraWithdrawFee"],
                "depositConfirm": api_data["data_0_chains_0_depositConfirm"],
                "withdrawConfirm": api_data["data_0_chains_0_withdrawConfirm"],
                "minDepositAmount": api_data["data_0_chains_0_minDepositAmount"],
                "minWithdrawAmount": api_data["data_0_chains_0_minWithdrawAmount"],
                "browserUrl": api_data["data_0_chains_0_browserUrl"],
                "contractAddress": None if api_data["data_0_chains_0_contractAddress"] == "null" else api_data["data_0_chains_0_contractAddress"],
                "withdrawStep": api_data["data_0_chains_0_withdrawStep"],
                "withdrawMinScale": api_data["data_0_chains_0_withdrawMinScale"],
                "congestion": api_data["data_0_chains_0_congestion"]
            }
        ]

        # Construct final data structure
        data = [
            {
                "coinId": api_data["data_0_coinId"],
                "coin": api_data["data_0_coin"],
                "transfer": api_data["data_0_transfer"],
                "areaCoin": api_data["data_0_areaCoin"],
                "chains": chains
            }
        ]

        return {
            "code": api_data["code"],
            "msg": api_data["msg"],
            "requestTime": api_data["requestTime"],
            "data": data
        }

    except Exception as e:
        return {
            "code": "500",
            "msg": f"Internal server error: {str(e)}",
            "requestTime": int(time.time() * 1000),
            "data": []
        }