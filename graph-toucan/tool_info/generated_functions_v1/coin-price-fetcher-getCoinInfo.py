from typing import Dict, List, Any
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for coin information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - code (str): Response status code
        - msg (str): Message describing the result
        - requestTime (int): Timestamp in milliseconds when request was processed
        - data_0_coin (str): Token name for first chain entry
        - data_0_transfer (bool): Transferability for first chain entry
        - data_0_chains_0_chain (str): First supported chain name
        - data_0_chains_0_needTag (bool): Whether tag is needed for first chain
        - data_0_chains_0_withdrawable (bool): Whether withdrawal is supported on first chain
        - data_0_chains_0_rechargeable (bool): Whether deposit is supported on first chain
        - data_0_chains_0_withdrawFee (float): Withdrawal transaction fee for first chain
        - data_0_chains_0_extraWithdrawFee (float): Extra charge percentage for first chain
        - data_0_chains_0_browserUrl (str): Blockchain explorer URL for first chain
        - data_0_chains_0_contractAddress (str): Contract address for first chain
        - data_0_chains_0_withdrawStep (int): Withdrawal count step for first chain
        - data_0_chains_0_withdrawMinScale (int): Decimal places limit for withdrawal amount on first chain
        - data_0_chains_0_congestion (str): Network status of first chain (normal/congested)
        - data_0_chains_1_chain (str): Second supported chain name
        - data_0_chains_1_needTag (bool): Whether tag is needed for second chain
        - data_0_chains_1_withdrawable (bool): Whether withdrawal is supported on second chain
        - data_0_chains_1_rechargeable (bool): Whether deposit is supported on second chain
        - data_0_chains_1_withdrawFee (float): Withdrawal transaction fee for second chain
        - data_0_chains_1_extraWithdrawFee (float): Extra charge percentage for second chain
        - data_0_chains_1_browserUrl (str): Blockchain explorer URL for second chain
        - data_0_chains_1_contractAddress (str): Contract address for second chain
        - data_0_chains_1_withdrawStep (int): Withdrawal count step for second chain
        - data_0_chains_1_withdrawMinScale (int): Decimal places limit for withdrawal amount on second chain
        - data_0_chains_1_congestion (str): Network status of second chain (normal/congested)
    """
    return {
        "code": "200",
        "msg": "success",
        "requestTime": int(time.time() * 1000),
        "data_0_coin": "USDT",
        "data_0_transfer": True,
        "data_0_chains_0_chain": "ERC20",
        "data_0_chains_0_needTag": False,
        "data_0_chains_0_withdrawable": True,
        "data_0_chains_0_rechargeable": True,
        "data_0_chains_0_withdrawFee": 15.0,
        "data_0_chains_0_extraWithdrawFee": 0.0,
        "data_0_chains_0_browserUrl": "https://etherscan.io",
        "data_0_chains_0_contractAddress": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "data_0_chains_0_withdrawStep": 0,
        "data_0_chains_0_withdrawMinScale": 6,
        "data_0_chains_0_congestion": "normal",
        "data_0_chains_1_chain": "TRC20",
        "data_0_chains_1_needTag": False,
        "data_0_chains_1_withdrawable": True,
        "data_0_chains_1_rechargeable": True,
        "data_0_chains_1_withdrawFee": 1.0,
        "data_0_chains_1_extraWithdrawFee": 0.0,
        "data_0_chains_1_browserUrl": "https://tronscan.org",
        "data_0_chains_1_contractAddress": "TABC123DEF456GHI789JKL",
        "data_0_chains_1_withdrawStep": 0,
        "data_0_chains_1_withdrawMinScale": 6,
        "data_0_chains_1_congestion": "normal"
    }


def coin_price_fetcher_getCoinInfo(coin: str) -> Dict[str, Any]:
    """
    Get spot coin information for a given cryptocurrency.

    Args:
        coin (str): The name of the coin to fetch information for (e.g., "USDT", "BTC").

    Returns:
        Dict[str, Any]: A dictionary containing:
            - code (str): Response status code indicating success or error.
            - msg (str): Message describing the result of the request.
            - requestTime (int): Timestamp in milliseconds when the request was processed.
            - data (List[Dict]): List of coin information objects with nested chain details.

    Example:
        {
            "code": "200",
            "msg": "success",
            "requestTime": 1700000000000,
            "data": [
                {
                    "coin": "USDT",
                    "transfer": True,
                    "chains": [
                        {
                            "chain": "ERC20",
                            "needTag": False,
                            "withdrawable": True,
                            "rechargeable": True,
                            "withdrawFee": 15.0,
                            "extraWithdrawFee": 0.0,
                            "browserUrl": "https://etherscan.io",
                            "contractAddress": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                            "withdrawStep": 0,
                            "withdrawMinScale": 6,
                            "congestion": "normal"
                        },
                        {
                            "chain": "TRC20",
                            "needTag": False,
                            "withdrawable": True,
                            "rechargeable": True,
                            "withdrawFee": 1.0,
                            "extraWithdrawFee": 0.0,
                            "browserUrl": "https://tronscan.org",
                            "contractAddress": "TABC123DEF456GHI789JKL",
                            "withdrawStep": 0,
                            "withdrawMinScale": 6,
                            "congestion": "normal"
                        }
                    ]
                }
            ]
        }
    """
    if not coin or not isinstance(coin, str):
        return {
            "code": "400",
            "msg": "Invalid input: coin must be a non-empty string",
            "requestTime": int(time.time() * 1000),
            "data": []
        }

    try:
        api_data = call_external_api("coin-price-fetcher-getCoinInfo")

        # Construct chains list
        chains = [
            {
                "chain": api_data["data_0_chains_0_chain"],
                "needTag": api_data["data_0_chains_0_needTag"],
                "withdrawable": api_data["data_0_chains_0_withdrawable"],
                "rechargeable": api_data["data_0_chains_0_rechargeable"],
                "withdrawFee": api_data["data_0_chains_0_withdrawFee"],
                "extraWithdrawFee": api_data["data_0_chains_0_extraWithdrawFee"],
                "browserUrl": api_data["data_0_chains_0_browserUrl"],
                "contractAddress": api_data["data_0_chains_0_contractAddress"],
                "withdrawStep": api_data["data_0_chains_0_withdrawStep"],
                "withdrawMinScale": api_data["data_0_chains_0_withdrawMinScale"],
                "congestion": api_data["data_0_chains_0_congestion"]
            },
            {
                "chain": api_data["data_0_chains_1_chain"],
                "needTag": api_data["data_0_chains_1_needTag"],
                "withdrawable": api_data["data_0_chains_1_withdrawable"],
                "rechargeable": api_data["data_0_chains_1_rechargeable"],
                "withdrawFee": api_data["data_0_chains_1_withdrawFee"],
                "extraWithdrawFee": api_data["data_0_chains_1_extraWithdrawFee"],
                "browserUrl": api_data["data_0_chains_1_browserUrl"],
                "contractAddress": api_data["data_0_chains_1_contractAddress"],
                "withdrawStep": api_data["data_0_chains_1_withdrawStep"],
                "withdrawMinScale": api_data["data_0_chains_1_withdrawMinScale"],
                "congestion": api_data["data_0_chains_1_congestion"]
            }
        ]

        return {
            "code": api_data["code"],
            "msg": api_data["msg"],
            "requestTime": api_data["requestTime"],
            "data": [
                {
                    "coin": api_data["data_0_coin"],
                    "transfer": api_data["data_0_transfer"],
                    "chains": chains
                }
            ]
        }

    except Exception as e:
        return {
            "code": "500",
            "msg": f"Internal server error: {str(e)}",
            "requestTime": int(time.time() * 1000),
            "data": []
        }