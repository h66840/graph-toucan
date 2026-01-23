from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching balance sheet data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - report_0_date (str): Reporting date for first record (ISO format)
        - report_0_currency (str): Currency code for first record
        - report_0_total_assets (float): Total assets for first record
        - report_0_current_assets (float): Current assets for first record
        - report_0_cash_and_equivalents (float): Cash and equivalents for first record
        - report_0_total_liabilities (float): Total liabilities for first record
        - report_0_current_liabilities (float): Current liabilities for first record
        - report_0_equity (float): Shareholders' equity for first record
        - report_0_current_ratio (float): Current ratio for first record
        - report_0_debt_to_assets (float): Debt to assets ratio for first record
        - report_1_date (str): Reporting date for second record (ISO format)
        - report_1_currency (str): Currency code for second record
        - report_1_total_assets (float): Total assets for second record
        - report_1_current_assets (float): Current assets for second record
        - report_1_cash_and_equivalents (float): Cash and equivalents for second record
        - report_1_total_liabilities (float): Total liabilities for second record
        - report_1_current_liabilities (float): Current liabilities for second record
        - report_1_equity (float): Shareholders' equity for second record
        - report_1_current_ratio (float): Current ratio for second record
        - report_1_debt_to_assets (float): Debt to assets ratio for second record
    """
    base_date = datetime.now().date()
    return {
        "report_0_date": (base_date - timedelta(days=365)).isoformat(),
        "report_0_currency": "CNY",
        "report_0_total_assets": 1000000000.0,
        "report_0_current_assets": 600000000.0,
        "report_0_cash_and_equivalents": 200000000.0,
        "report_0_total_liabilities": 400000000.0,
        "report_0_current_liabilities": 250000000.0,
        "report_0_equity": 600000000.0,
        "report_0_current_ratio": 2.4,
        "report_0_debt_to_assets": 0.4,

        "report_1_date": (base_date - timedelta(days=730)).isoformat(),
        "report_1_currency": "CNY",
        "report_1_total_assets": 900000000.0,
        "report_1_current_assets": 550000000.0,
        "report_1_cash_and_equivalents": 180000000.0,
        "report_1_total_liabilities": 380000000.0,
        "report_1_current_liabilities": 240000000.0,
        "report_1_equity": 520000000.0,
        "report_1_current_ratio": 2.29,
        "report_1_debt_to_assets": 0.42,
    }


def akshare_one_mcp_server_get_balance_sheet(symbol: str, recent_n: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get company balance sheet data.

    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001')
        recent_n (Optional[int]): Number of most recent records to return

    Returns:
        Dict containing:
        - balance_sheet_data (List[Dict]): list of balance sheet records, each containing financial metrics
          for a specific reporting period. Keys include 'report_date' (timestamp), 'currency',
          various asset/liability/equity components (e.g., 'total_assets', 'current_assets',
          'cash_and_equivalents'), and financial ratios like 'current_ratio' and 'debt_to_assets'.
          All monetary values are in the specified currency.

    Raises:
        ValueError: If symbol is empty or not provided
    """
    if not symbol:
        raise ValueError("Symbol is required")

    # Fetch data from external API
    api_data = call_external_api("akshare-one-mcp-server-get_balance_sheet")

    # Construct balance sheet records from flat API data
    balance_sheet_data = []

    # Process first record (most recent)
    balance_sheet_data.append({
        "report_date": api_data["report_0_date"],
        "currency": api_data["report_0_currency"],
        "total_assets": api_data["report_0_total_assets"],
        "current_assets": api_data["report_0_current_assets"],
        "cash_and_equivalents": api_data["report_0_cash_and_equivalents"],
        "total_liabilities": api_data["report_0_total_liabilities"],
        "current_liabilities": api_data["report_0_current_liabilities"],
        "equity": api_data["report_0_equity"],
        "current_ratio": api_data["report_0_current_ratio"],
        "debt_to_assets": api_data["report_0_debt_to_assets"],
    })

    # Process second record (older)
    balance_sheet_data.append({
        "report_date": api_data["report_1_date"],
        "currency": api_data["report_1_currency"],
        "total_assets": api_data["report_1_total_assets"],
        "current_assets": api_data["report_1_current_assets"],
        "cash_and_equivalents": api_data["report_1_cash_and_equivalents"],
        "total_liabilities": api_data["report_1_total_liabilities"],
        "current_liabilities": api_data["report_1_current_liabilities"],
        "equity": api_data["report_1_equity"],
        "current_ratio": api_data["report_1_current_ratio"],
        "debt_to_assets": api_data["report_1_debt_to_assets"],
    })

    # Apply recent_n filter if specified
    if recent_n is not None:
        balance_sheet_data = balance_sheet_data[:recent_n]

    return {"balance_sheet_data": balance_sheet_data}