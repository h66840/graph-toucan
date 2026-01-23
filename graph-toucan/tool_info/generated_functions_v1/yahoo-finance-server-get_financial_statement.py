from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching financial statement data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - financial_data_0_date (str): Date of the first financial report
        - financial_data_0_Revenue (float): Revenue for the first period
        - financial_data_0_GrossProfit (float): Gross profit for the first period
        - financial_data_0_NetIncome (float): Net income for the first period
        - financial_data_1_date (str): Date of the second financial report
        - financial_data_1_Revenue (float): Revenue for the second period
        - financial_data_1_GrossProfit (float): Gross profit for the second period
        - financial_data_1_NetIncome (float): Net income for the second period
    """
    return {
        "financial_data_0_date": "2023-12-31",
        "financial_data_0_Revenue": 117154000000.0,
        "financial_data_0_GrossProfit": 44281000000.0,
        "financial_data_0_NetIncome": 29998000000.0,
        "financial_data_1_date": "2022-12-31",
        "financial_data_1_Revenue": 111439000000.0,
        "financial_data_1_GrossProfit": 42567000000.0,
        "financial_data_1_NetIncome": 28759000000.0,
    }

def yahoo_finance_server_get_financial_statement(ticker: str, financial_type: str) -> List[Dict[str, Any]]:
    """
    Get financial statement for a given ticker symbol from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to get financial statement for, e.g. "AAPL"
        financial_type (str): The type of financial statement to get. Options: income_stmt, 
                             quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, 
                             cashflow, quarterly_cashflow.
    
    Returns:
        List[Dict]: List of financial statement entries, each representing a reporting period 
                   with 'date' and various financial metrics as key-value pairs.
    
    Raises:
        ValueError: If ticker or financial_type is empty or invalid.
    """
    # Input validation
    if not ticker:
        raise ValueError("Ticker symbol must not be empty")
    
    if not financial_type:
        raise ValueError("Financial type must not be empty")
        
    valid_types = [
        "income_stmt", "quarterly_income_stmt", 
        "balance_sheet", "quarterly_balance_sheet", 
        "cashflow", "quarterly_cashflow"
    ]
    
    if financial_type not in valid_types:
        raise ValueError(f"Invalid financial_type. Must be one of {valid_types}")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("yahoo-finance-server-get_financial_statement")
    
    # Construct financial data list from flattened API response
    financial_data = [
        {
            "date": api_data["financial_data_0_date"],
            "Revenue": api_data["financial_data_0_Revenue"],
            "GrossProfit": api_data["financial_data_0_GrossProfit"],
            "NetIncome": api_data["financial_data_0_NetIncome"]
        },
        {
            "date": api_data["financial_data_1_date"],
            "Revenue": api_data["financial_data_1_Revenue"],
            "GrossProfit": api_data["financial_data_1_GrossProfit"],
            "NetIncome": api_data["financial_data_1_NetIncome"]
        }
    ]
    
    return financial_data