from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching recommendations or upgrades/downgrades data from Yahoo Finance API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - recommendation_0_analyst (str): Name of the first analyst
        - recommendation_0_firm (str): Firm of the first analyst
        - recommendation_0_action (str): Action taken by first analyst (e.g., "upgrade")
        - recommendation_0_date (str): ISO 8601 date of first recommendation
        - recommendation_0_target_price (float): Target price from first recommendation, if available
        - recommendation_1_analyst (str): Name of the second analyst
        - recommendation_1_firm (str): Firm of the second analyst
        - recommendation_1_action (str): Action taken by second analyst
        - recommendation_1_date (str): ISO 8601 date of second recommendation
        - recommendation_1_target_price (float): Target price from second recommendation
        - summary_consensus (str): Consensus recommendation (e.g., "Buy")
        - summary_buy_count (int): Number of analysts with "Buy" rating
        - summary_hold_count (int): Number of analysts with "Hold" rating
        - summary_sell_count (int): Number of analysts with "Sell" rating
        - summary_timestamp (str): ISO 8601 timestamp of latest consensus
        - source (str): Source of the data ("Yahoo Finance")
        - last_updated (str): ISO 8601 timestamp when data was last updated
        - metadata_ticker (str): Ticker symbol queried
        - metadata_recommendation_type (str): Type of recommendation retrieved
        - metadata_months_back (int): Number of months back covered
    """
    now = datetime.now()
    past_date_1 = (now - timedelta(days=random.randint(1, 90))).isoformat()
    past_date_2 = (now - timedelta(days=random.randint(1, 90))).isoformat()
    
    actions = ["upgrade", "downgrade", "initiated", "maintained"]
    consensus_options = ["Buy", "Hold", "Sell", "Strong Buy", "Strong Sell"]
    
    return {
        "recommendation_0_analyst": "John Smith",
        "recommendation_0_firm": "Goldman Sachs",
        "recommendation_0_action": random.choice(actions),
        "recommendation_0_date": past_date_1,
        "recommendation_0_target_price": round(random.uniform(100, 200), 2),
        "recommendation_1_analyst": "Emily Chen",
        "recommendation_1_firm": "Morgan Stanley",
        "recommendation_1_action": random.choice(actions),
        "recommendation_1_date": past_date_2,
        "recommendation_1_target_price": round(random.uniform(100, 200), 2),
        "summary_consensus": random.choice(consensus_options),
        "summary_buy_count": random.randint(5, 15),
        "summary_hold_count": random.randint(2, 8),
        "summary_sell_count": random.randint(0, 5),
        "summary_timestamp": now.isoformat(),
        "source": "Yahoo Finance",
        "last_updated": now.isoformat(),
        "metadata_ticker": "AAPL",
        "metadata_recommendation_type": "upgrades_downgrades",
        "metadata_months_back": 12
    }


def yahoo_finance_server_get_recommendations(
    ticker: str, 
    recommendation_type: str, 
    months_back: Optional[int] = 12
) -> Dict[str, Any]:
    """
    Get recommendations or upgrades/downgrades for a given ticker symbol from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to get recommendations for, e.g. "AAPL"
        recommendation_type (str): The type of recommendation to get. Options: "recommendations", "upgrades_downgrades"
        months_back (int, optional): The number of months back to get upgrades/downgrades for. Default is 12.
    
    Returns:
        Dict containing:
        - recommendations (List[Dict]): List of recommendation records with analyst, firm, action, date, and target price
        - summary (Dict): Summary statistics including consensus recommendation and analyst counts
        - source (str): Source of the data ("Yahoo Finance")
        - last_updated (str): ISO 8601 timestamp indicating when the recommendations were last updated
        - metadata (Dict): Additional metadata such as ticker, recommendation type, and time range
    
    Raises:
        ValueError: If ticker is empty or recommendation_type is not one of the allowed values
    """
    # Input validation
    if not ticker or not ticker.strip():
        raise ValueError("Ticker symbol must not be empty")
    
    if recommendation_type not in ["recommendations", "upgrades_downgrades"]:
        raise ValueError("recommendation_type must be one of: recommendations, upgrades_downgrades")
    
    if months_back is None:
        months_back = 12
    elif months_back <= 0:
        raise ValueError("months_back must be a positive integer")
    
    # Call external API to get flattened data
    api_data = call_external_api("yahoo-finance-server-get_recommendations")
    
    # Construct recommendations list from indexed fields
    recommendations = [
        {
            "analyst": api_data["recommendation_0_analyst"],
            "firm": api_data["recommendation_0_firm"],
            "action": api_data["recommendation_0_action"],
            "date": api_data["recommendation_0_date"],
            "target_price": api_data["recommendation_0_target_price"]
        },
        {
            "analyst": api_data["recommendation_1_analyst"],
            "firm": api_data["recommendation_1_firm"],
            "action": api_data["recommendation_1_action"],
            "date": api_data["recommendation_1_date"],
            "target_price": api_data["recommendation_1_target_price"]
        }
    ]
    
    # Construct summary dictionary
    summary = {
        "consensus": api_data["summary_consensus"],
        "buy_count": api_data["summary_buy_count"],
        "hold_count": api_data["summary_hold_count"],
        "sell_count": api_data["summary_sell_count"],
        "timestamp": api_data["summary_timestamp"]
    }
    
    # Construct metadata dictionary
    metadata = {
        "ticker": ticker,
        "recommendation_type": recommendation_type,
        "time_range_months": months_back
    }
    
    # Return final structured response
    return {
        "recommendations": recommendations,
        "summary": summary,
        "source": api_data["source"],
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }