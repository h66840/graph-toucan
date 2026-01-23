from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cash flow data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - report_date (str): Reporting period end date (YYYY-MM-DD)
        - currency (str): Currency code (e.g., 'CNY')
        - net_cash_flow_from_operations (float): Net cash flow from operating activities
        - net_cash_flow_from_investing (float): Net cash flow from investing activities
        - net_cash_flow_from_financing (float): Net cash flow from financing activities
        - change_in_cash_and_equivalents (float): Change in cash and cash equivalents
        - ending_cash_balance (float): Ending cash and cash equivalents balance
        - beginning_cash_balance (float): Beginning cash and cash equivalents balance
        - total_cash_inflow_from_operations (float): Total cash inflow from operations
        - total_cash_outflow_from_operations (float): Total cash outflow from operations
        - total_cash_inflow_from_investing (float): Total cash inflow from investing
        - total_cash_outflow_from_investing (float): Total cash outflow from investing
        - total_cash_inflow_from_financing (float): Total cash inflow from financing
        - total_cash_outflow_from_financing (float): Total cash outflow from financing
        - cash_from_sales (float): Cash received from sales of goods/services
        - tax_refunds_received (float): Tax refunds received
        - cash_paid_to_employees (float): Cash paid to employees
        - taxes_paid (float): Taxes paid
        - cash_from_investment_recovery (float): Cash from recovery of investments
        - cash_from_investment_income (float): Cash from investment income
        - cash_from_asset_sales (float): Cash from sale of assets
        - issuance_or_repayment_of_debt_securities (float): Cash from issuance/repayment of debt
        - issuance_or_purchase_of_equity_shares (float): Cash from issuance/purchase of equity
        - cash_paid_for_dividends_and_interest (float): Cash paid for dividends and interest
        - cash_paid_for_debt_repayment (float): Cash paid for debt repayment
        - effect_of_exchange_rate_changes (float): Effect of exchange rate changes on cash
        - capital_expenditure (float): Capital expenditures
        - business_acquisitions_and_disposals (float): Cash from business acquisitions/disposals
    """
    return {
        "report_date": "2023-12-31",
        "currency": "CNY",
        "net_cash_flow_from_operations": 15000000.0,
        "net_cash_flow_from_investing": -5000000.0,
        "net_cash_flow_from_financing": 2000000.0,
        "change_in_cash_and_equivalents": 12000000.0,
        "ending_cash_balance": 25000000.0,
        "beginning_cash_balance": 13000000.0,
        "total_cash_inflow_from_operations": 25000000.0,
        "total_cash_outflow_from_operations": 10000000.0,
        "total_cash_inflow_from_investing": 3000000.0,
        "total_cash_outflow_from_investing": 8000000.0,
        "total_cash_inflow_from_financing": 7000000.0,
        "total_cash_outflow_from_financing": 5000000.0,
        "cash_from_sales": 22000000.0,
        "tax_refunds_received": 500000.0,
        "cash_paid_to_employees": 4000000.0,
        "taxes_paid": 1500000.0,
        "cash_from_investment_recovery": 1000000.0,
        "cash_from_investment_income": 2000000.0,
        "cash_from_asset_sales": 3000000.0,
        "issuance_or_repayment_of_debt_securities": 3000000.0,
        "issuance_or_purchase_of_equity_shares": 4000000.0,
        "cash_paid_for_dividends_and_interest": 2500000.0,
        "cash_paid_for_debt_repayment": 1500000.0,
        "effect_of_exchange_rate_changes": 100000.0,
        "capital_expenditure": 6000000.0,
        "business_acquisitions_and_disposals": 1000000.0,
    }

def akshare_one_mcp_server_get_cash_flow(
    symbol: str,
    recent_n: Optional[int] = None,
    source: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get company cash flow statement data.
    
    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001')
        recent_n (Optional[int]): Number of most recent records to return
        source (Optional[str]): Data source
    
    Returns:
        Dict containing cash_flow_data which is a list of cash flow statement records.
        Each record includes financial metrics for a reporting period with fields:
        - report_date
        - currency
        - net_cash_flow_from_operations
        - net_cash_flow_from_investing
        - net_cash_flow_from_financing
        - change_in_cash_and_equivalents
        - ending_cash_balance
        - beginning_cash_balance
        - total_cash_inflow_from_operations
        - total_cash_outflow_from_operations
        - total_cash_inflow_from_investing
        - total_cash_outflow_from_investing
        - total_cash_inflow_from_financing
        - total_cash_outflow_from_financing
        - cash_from_sales
        - tax_refunds_received
        - cash_paid_to_employees
        - taxes_paid
        - cash_from_investment_recovery
        - cash_from_investment_income
        - cash_from_asset_sales
        - issuance_or_repayment_of_debt_securities
        - issuance_or_purchase_of_equity_shares
        - cash_paid_for_dividends_and_interest
        - cash_paid_for_debt_repayment
        - effect_of_exchange_rate_changes
        - capital_expenditure
        - business_acquisitions_and_disposals
    
    Raises:
        ValueError: If symbol is empty or invalid
    """
    if not symbol or not symbol.strip():
        raise ValueError("Symbol is required and cannot be empty")
    
    # Validate recent_n if provided
    if recent_n is not None and (not isinstance(recent_n, int) or recent_n <= 0):
        raise ValueError("recent_n must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("akshare-one-mcp-server-get_cash_flow")
    
    # Construct the cash flow record from flat API data
    cash_flow_record = {
        "report_date": api_data["report_date"],
        "currency": api_data["currency"],
        "net_cash_flow_from_operations": api_data["net_cash_flow_from_operations"],
        "net_cash_flow_from_investing": api_data["net_cash_flow_from_investing"],
        "net_cash_flow_from_financing": api_data["net_cash_flow_from_financing"],
        "change_in_cash_and_equivalents": api_data["change_in_cash_and_equivalents"],
        "ending_cash_balance": api_data["ending_cash_balance"],
        "beginning_cash_balance": api_data["beginning_cash_balance"],
        "total_cash_inflow_from_operations": api_data["total_cash_inflow_from_operations"],
        "total_cash_outflow_from_operations": api_data["total_cash_outflow_from_operations"],
        "total_cash_inflow_from_investing": api_data["total_cash_inflow_from_investing"],
        "total_cash_outflow_from_investing": api_data["total_cash_outflow_from_investing"],
        "total_cash_inflow_from_financing": api_data["total_cash_inflow_from_financing"],
        "total_cash_outflow_from_financing": api_data["total_cash_outflow_from_financing"],
        "cash_from_sales": api_data["cash_from_sales"],
        "tax_refunds_received": api_data["tax_refunds_received"],
        "cash_paid_to_employees": api_data["cash_paid_to_employees"],
        "taxes_paid": api_data["taxes_paid"],
        "cash_from_investment_recovery": api_data["cash_from_investment_recovery"],
        "cash_from_investment_income": api_data["cash_from_investment_income"],
        "cash_from_asset_sales": api_data["cash_from_asset_sales"],
        "issuance_or_repayment_of_debt_securities": api_data["issuance_or_repayment_of_debt_securities"],
        "issuance_or_purchase_of_equity_shares": api_data["issuance_or_purchase_of_equity_shares"],
        "cash_paid_for_dividends_and_interest": api_data["cash_paid_for_dividends_and_interest"],
        "cash_paid_for_debt_repayment": api_data["cash_paid_for_debt_repayment"],
        "effect_of_exchange_rate_changes": api_data["effect_of_exchange_rate_changes"],
        "capital_expenditure": api_data["capital_expenditure"],
        "business_acquisitions_and_disposals": api_data["business_acquisitions_and_disposals"],
    }
    
    # Create list with one item (as only one record is simulated)
    cash_flow_data = [cash_flow_record]
    
    # Apply recent_n filter if specified
    if recent_n is not None:
        cash_flow_data = cash_flow_data[-recent_n:]
    
    return {
        "cash_flow_data": cash_flow_data
    }