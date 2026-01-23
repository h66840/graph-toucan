def coin_mcp_server_getTokenPrice(token: str) -> float:
    """
    Get the current price of a cryptocurrency.
    
    Args:
        token (str): The symbol of the cryptocurrency (e.g., "BTC", "ETH", "LTC")
    
    Returns:
        float: The current market price of the cryptocurrency in USD
        
    Raises:
        ValueError: If the token parameter is empty or None
        KeyError: If the requested cryptocurrency is not supported
    
    Example:
        >>> coin_mcp_server_getTokenPrice("ETH")
        3721.32
        >>> coin_mcp_server_getTokenPrice("BTC")
        45000.0
    """
    # Input validation
    if not token:
        raise ValueError("Token parameter cannot be empty")
    
    # Convert to uppercase for consistency
    token = token.upper()
    
    # Mock data for demonstration purposes
    # In a production environment, this would call an actual cryptocurrency API
    mock_prices = {
        "BTC": 45000.0,
        "ETH": 3721.32,
        "LTC": 89.45,
        "BCH": 345.67,
        "XRP": 0.56,
        "ADA": 0.45,
        "SOL": 98.76,
        "DOT": 6.54,
        "MATIC": 0.87,
        "BNB": 310.23
    }
    
    try:
        return mock_prices[token]
    except KeyError:
        # Provide a helpful error message listing available tokens
        available_tokens = ", ".join(sorted(mock_prices.keys()))
        raise KeyError(f"Price data not available for '{token}'. Supported tokens: {available_tokens}")