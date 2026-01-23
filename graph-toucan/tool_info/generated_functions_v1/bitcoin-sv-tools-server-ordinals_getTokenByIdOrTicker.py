from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BSV-20 token information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - txid (str): transaction ID of the token creation inscription
        - vout (int): output index of the transaction where the token was inscribed
        - height (int): blockchain height (block number) at which the token was created
        - idx (str): unique ordinal index identifier for the inscription
        - status (int): current status of the token (e.g., 1 for active, 0 for inactive)
        - fundTotal (str): total BSV amount allocated for mint funding
        - fundUsed (str): amount of BSV from fund that has been used
        - fundBalance (str): remaining BSV balance in the mint fund
        - tick (str): ticker symbol of the BSV-20 token
        - max (str): maximum total supply of the token
        - lim (str): limit per mint transaction
        - dec (int): number of decimal places supported by the token
        - supply (str): current total supply that has been minted so far
        - available (str): amount of tokens still available for minting
        - pctMinted (str): percentage of the total supply that has already been minted
        - accounts (int): number of unique accounts (addresses) holding this token
        - fundAddress (str): Bitcoin SV address designated to receive mint funding
    """
    return {
        "txid": "f8f9d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8",
        "vout": 0,
        "height": 800000,
        "idx": "800000:0:0",
        "status": 1,
        "fundTotal": "10.0",
        "fundUsed": "3.5",
        "fundBalance": "6.5",
        "tick": "BSV20",
        "max": "21000000",
        "lim": "1000",
        "dec": 18,
        "supply": "1500000",
        "available": "19500000",
        "pctMinted": "7.14",
        "accounts": 425,
        "fundAddress": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    }

def bitcoin_sv_tools_server_ordinals_getTokenByIdOrTicker(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific BSV-20 token by its ID or ticker symbol.
    
    This function simulates querying an external service to get complete token data
    including ticker symbol, supply information, decimals, and current status.
    
    Args:
        args (Dict[str, Any]): Input parameters containing either 'id' or 'ticker'
                              to identify the token. Example: {'id': 'txid:vout'} or {'ticker': 'BSV20'}
    
    Returns:
        Dict[str, Any]: Complete token data with the following fields:
            - txid (str): transaction ID of the token creation inscription
            - vout (int): output index of the transaction where the token was inscribed
            - height (int): blockchain height (block number) at which the token was created
            - idx (str): unique ordinal index identifier for the inscription
            - status (int): current status of the token (e.g., 1 for active, 0 for inactive)
            - fundTotal (str): total BSV amount allocated for mint funding
            - fundUsed (str): amount of BSV from fund that has been used
            - fundBalance (str): remaining BSV balance in the mint fund
            - tick (str): ticker symbol of the BSV-20 token
            - max (str): maximum total supply of the token
            - lim (str): limit per mint transaction
            - dec (int): number of decimal places supported by the token
            - supply (str): current total supply that has been minted so far
            - available (str): amount of tokens still available for minting
            - pctMinted (str): percentage of the total supply that has already been minted
            - accounts (int): number of unique accounts (addresses) holding this token
            - fundAddress (str): Bitcoin SV address designated to receive mint funding
    
    Raises:
        ValueError: If required arguments are missing or invalid
        KeyError: If the requested token is not found
    """
    # Input validation
    if not args:
        raise ValueError("Arguments are required")
    
    if 'id' not in args and 'ticker' not in args:
        raise ValueError("Either 'id' or 'ticker' must be provided in args")
    
    # Simulate API call to get flat data
    api_data = call_external_api("bitcoin-sv-tools-server-ordinals_getTokenByIdOrTicker")
    
    # Construct the nested response structure as per output schema
    result = {
        "txid": api_data["txid"],
        "vout": api_data["vout"],
        "height": api_data["height"],
        "idx": api_data["idx"],
        "status": api_data["status"],
        "fundTotal": api_data["fundTotal"],
        "fundUsed": api_data["fundUsed"],
        "fundBalance": api_data["fundBalance"],
        "tick": api_data["tick"],
        "max": api_data["max"],
        "lim": api_data["lim"],
        "dec": api_data["dec"],
        "supply": api_data["supply"],
        "available": api_data["available"],
        "pctMinted": api_data["pctMinted"],
        "accounts": api_data["accounts"],
        "fundAddress": api_data["fundAddress"]
    }
    
    return result