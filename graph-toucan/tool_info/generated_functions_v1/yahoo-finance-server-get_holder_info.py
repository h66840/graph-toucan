from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching holder information from Yahoo Finance API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - holders_data_0_holder_name (str): Name of the first holder
        - holders_data_0_shares_held (int): Number of shares held by first holder
        - holders_data_0_percentage_ownership (float): Percentage ownership of first holder
        - holders_data_0_change_in_shares (int): Change in shares for first holder (can be negative)
        - holders_data_0_market_value (float): Market value of holdings for first holder
        - holders_data_1_holder_name (str): Name of the second holder
        - holders_data_1_shares_held (int): Number of shares held by second holder
        - holders_data_1_percentage_ownership (float): Percentage ownership of second holder
        - holders_data_1_change_in_shares (int): Change in shares for second holder (can be negative)
        - holders_data_1_market_value (float): Market value of holdings for second holder
        - holder_type (str): Type of holder data requested
        - ticker (str): Stock ticker symbol
        - total_holders_count (int): Total number of holders returned
        - as_of_date (str): ISO 8601 date string when data was last updated
        - source (str): Source of the data
        - metadata_notes (str): Additional notes or warnings about the data
        - metadata_data_freshness (str): Freshness status of the data
    """
    # Generate realistic mock data based on inputs
    holder_types = [
        "major_holders", 
        "institutional_holders", 
        "mutualfund_holders", 
        "insider_transactions", 
        "insider_purchases", 
        "insider_roster_holders"
    ]
    
    selected_holder_type = random.choice(holder_types)
    ticker = ''.join(random.choices(string.ascii_uppercase, k=4))
    
    # Generate random date within last 30 days
    as_of_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
    
    return {
        "holders_data_0_holder_name": f"Vanguard Group Inc" if selected_holder_type != "insider_roster_holders" 
                                     else f"John Smith",
        "holders_data_0_shares_held": random.randint(1000000, 50000000),
        "holders_data_0_percentage_ownership": round(random.uniform(1.5, 15.0), 2),
        "holders_data_0_change_in_shares": random.randint(-500000, 1000000),
        "holders_data_0_market_value": round(random.uniform(50000000, 2000000000), 2),
        "holders_data_1_holder_name": f"BlackRock Inc" if selected_holder_type != "insider_roster_holders" 
                                     else f"Jane Doe",
        "holders_data_1_shares_held": random.randint(800000, 45000000),
        "holders_data_1_percentage_ownership": round(random.uniform(1.0, 12.0), 2),
        "holders_data_1_change_in_shares": random.randint(-400000, 800000),
        "holders_data_1_market_value": round(random.uniform(40000000, 1800000000), 2),
        "holder_type": selected_holder_type,
        "ticker": ticker,
        "total_holders_count": random.randint(10, 100),
        "as_of_date": as_of_date,
        "source": "Yahoo Finance",
        "metadata_notes": "Insider transactions may be delayed by regulatory filing schedules" 
                        if "insider" in selected_holder_type 
                        else "Data reflects latest available institutional filings",
        "metadata_data_freshness": "recent" if random.random() > 0.3 else "delayed"
    }

def yahoo_finance_server_get_holder_info(ticker: str, holder_type: str) -> Dict[str, Any]:
    """
    Get holder information for a given ticker symbol from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to get holder information for, e.g. "AAPL"
        holder_type (str): The type of holder information to get. Valid options are:
                         major_holders, institutional_holders, mutualfund_holders,
                         insider_transactions, insider_purchases, insider_roster_holders
    
    Returns:
        Dict containing:
        - holders_data (List[Dict]): List of dictionaries with holder-specific information
        - holder_type (str): The type of holder data returned
        - ticker (str): The ticker symbol for which data was retrieved
        - total_holders_count (int): Total number of holders returned
        - as_of_date (str): ISO 8601 date string indicating when data was last updated
        - source (str): Source of the data
        - metadata (Dict): Additional context about the request and response
    
    Raises:
        ValueError: If ticker is empty or holder_type is not one of the allowed values
    """
    # Input validation
    if not ticker or not ticker.strip():
        raise ValueError("Ticker symbol must not be empty")
    
    valid_holder_types = [
        "major_holders", 
        "institutional_holders", 
        "mutualfund_holders", 
        "insider_transactions", 
        "insider_purchases", 
        "insider_roster_holders"
    ]
    
    if holder_type not in valid_holder_types:
        raise ValueError(f"holder_type must be one of {valid_holder_types}")
    
    # Call external API to get data (returns only simple scalar fields)
    api_data = call_external_api("yahoo-finance-server-get_holder_info")
    
    # Construct holders_data list from indexed fields
    holders_data = [
        {
            "holder_name": api_data["holders_data_0_holder_name"],
            "shares_held": api_data["holders_data_0_shares_held"],
            "percentage_ownership": api_data["holders_data_0_percentage_ownership"],
            "change_in_shares": api_data["holders_data_0_change_in_shares"],
            "market_value": api_data["holders_data_0_market_value"]
        },
        {
            "holder_name": api_data["holders_data_1_holder_name"],
            "shares_held": api_data["holders_data_1_shares_held"],
            "percentage_ownership": api_data["holders_data_1_percentage_ownership"],
            "change_in_shares": api_data["holders_data_1_change_in_shares"],
            "market_value": api_data["holders_data_1_market_value"]
        }
    ]
    
    # Construct metadata dictionary
    metadata = {
        "notes": api_data["metadata_notes"],
        "data_freshness": api_data["metadata_data_freshness"]
    }
    
    # Construct final result matching output schema
    result = {
        "holders_data": holders_data,
        "holder_type": api_data["holder_type"],
        "ticker": api_data["ticker"],
        "total_holders_count": api_data["total_holders_count"],
        "as_of_date": api_data["as_of_date"],
        "source": api_data["source"],
        "metadata": metadata
    }
    
    return result