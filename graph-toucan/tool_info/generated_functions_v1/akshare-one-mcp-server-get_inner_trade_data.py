from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching insider trading data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - insider_0_date (str): Date of first insider trade (YYYY-MM-DD)
        - insider_0_symbol (str): Stock symbol for first trade
        - insider_0_name (str): Name of insider for first trade
        - insider_0_relation (str): Relationship to company for first trade
        - insider_0_type (str): Type of transaction (e.g., Buy/Sell)
        - insider_0_volume (int): Volume of shares traded
        - insider_0_price (float): Price per share
        - insider_0_amount (float): Total amount of transaction
        - insider_0_change (str): Change in ownership (e.g., +, -)
        - insider_1_date (str): Date of second insider trade (YYYY-MM-DD)
        - insider_1_symbol (str): Stock symbol for second trade
        - insider_1_name (str): Name of insider for second trade
        - insider_1_relation (str): Relationship to company for second trade
        - insider_1_type (str): Type of transaction (e.g., Buy/Sell)
        - insider_1_volume (int): Volume of shares traded
        - insider_1_price (float): Price per share
        - insider_1_amount (float): Total amount of transaction
        - insider_1_change (str): Change in ownership (e.g., +, -)
    """
    return {
        "insider_0_date": "2023-10-01",
        "insider_0_symbol": "000001",
        "insider_0_name": "Zhang San",
        "insider_0_relation": "Director",
        "insider_0_type": "Buy",
        "insider_0_volume": 10000,
        "insider_0_price": 15.5,
        "insider_0_amount": 155000.0,
        "insider_0_change": "+",
        "insider_1_date": "2023-09-28",
        "insider_1_symbol": "000001",
        "insider_1_name": "Li Si",
        "insider_1_relation": "Major Shareholder",
        "insider_1_type": "Sell",
        "insider_1_volume": 5000,
        "insider_1_price": 16.2,
        "insider_1_amount": 81000.0,
        "insider_1_change": "-"
    }

def akshare_one_mcp_server_get_inner_trade_data(symbol: str) -> Dict[str, Any]:
    """
    Get company insider trading data for a given stock symbol.
    
    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001')
        
    Returns:
        Dict containing a list of insider trade records. Each record includes:
        - date (str): Trade date in YYYY-MM-DD format
        - symbol (str): Stock symbol
        - name (str): Name of the insider
        - relation (str): Relationship to the company
        - type (str): Type of transaction (e.g., Buy/Sell)
        - volume (int): Number of shares traded
        - price (float): Price per share
        - amount (float): Total transaction amount
        - change (str): Change in ownership (+ for increase, - for decrease)
        
    Raises:
        ValueError: If symbol is empty or not a string
    """
    # Input validation
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("akshare-one-mcp-server-get_inner_trade_data")
    
    # Construct insider trades list from flattened API response
    insider_trades: List[Dict[str, Any]] = [
        {
            "date": api_data["insider_0_date"],
            "symbol": api_data["insider_0_symbol"],
            "name": api_data["insider_0_name"],
            "relation": api_data["insider_0_relation"],
            "type": api_data["insider_0_type"],
            "volume": api_data["insider_0_volume"],
            "price": api_data["insider_0_price"],
            "amount": api_data["insider_0_amount"],
            "change": api_data["insider_0_change"]
        },
        {
            "date": api_data["insider_1_date"],
            "symbol": api_data["insider_1_symbol"],
            "name": api_data["insider_1_name"],
            "relation": api_data["insider_1_relation"],
            "type": api_data["insider_1_type"],
            "volume": api_data["insider_1_volume"],
            "price": api_data["insider_1_price"],
            "amount": api_data["insider_1_amount"],
            "change": api_data["insider_1_change"]
        }
    ]
    
    # Filter trades by symbol if needed (in real case might filter, here we just ensure structure)
    filtered_trades = [trade for trade in insider_trades if trade["symbol"] == symbol]
    
    return {
        "insider_trades": filtered_trades
    }