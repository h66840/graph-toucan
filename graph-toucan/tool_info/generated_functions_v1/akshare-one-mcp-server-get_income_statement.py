from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching income statement data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - income_statement_0_report_date (str): Report date in YYYY-MM-DD format
        - income_statement_0_currency (str): Currency code (e.g., 'CNY')
        - income_statement_0_revenue (float): Total revenue
        - income_statement_0_operating_revenue (float): Operating revenue
        - income_statement_0_total_operating_costs (float): Total operating costs
        - income_statement_0_cost_of_revenue (float): Cost of revenue
        - income_statement_0_operating_profit (float): Operating profit
        - income_statement_0_selling_general_and_administrative_expenses (float): SG&A expenses
        - income_statement_0_operating_expense (float): Total operating expense
        - income_statement_0_research_and_development (float): R&D expense
        - income_statement_0_interest_expense (float): Interest expense
        - income_statement_0_ebit (float): Earnings before interest and taxes
        - income_statement_0_income_tax_expense (float): Income tax expense
        - income_statement_0_net_income (float): Net income
        - income_statement_0_net_income_common_stock (float): Net income attributable to common stockholders
        - income_statement_0_net_income_non_controlling_interests (float): Net income attributable to non-controlling interests
        - income_statement_0_earnings_per_share (float): Basic earnings per share
        - income_statement_0_earnings_per_share_diluted (float): Diluted earnings per share
        - income_statement_0_investment_income (float): Investment income
        - income_statement_0_fair_value_adjustments (float): Fair value gains/losses
        - income_statement_0_asset_impairment_loss (float): Asset impairment loss
        - income_statement_0_financial_expenses (float): Financial expenses
        - income_statement_0_taxes_and_surcharges (float): Taxes and surcharges
        - income_statement_0_other_comprehensive_income (float): Other comprehensive income
        - income_statement_0_total_comprehensive_income (float): Total comprehensive income
    """
    return {
        "income_statement_0_report_date": "2023-12-31",
        "income_statement_0_currency": "CNY",
        "income_statement_0_revenue": 5000000000.0,
        "income_statement_0_operating_revenue": 4950000000.0,
        "income_statement_0_total_operating_costs": 3500000000.0,
        "income_statement_0_cost_of_revenue": 3000000000.0,
        "income_statement_0_operating_profit": 1450000000.0,
        "income_statement_0_selling_general_and_administrative_expenses": 300000000.0,
        "income_statement_0_operating_expense": 350000000.0,
        "income_statement_0_research_and_development": 150000000.0,
        "income_statement_0_interest_expense": 50000000.0,
        "income_statement_0_ebit": 1400000000.0,
        "income_statement_0_income_tax_expense": 350000000.0,
        "income_statement_0_net_income": 1050000000.0,
        "income_statement_0_net_income_common_stock": 1020000000.0,
        "income_statement_0_net_income_non_controlling_interests": 30000000.0,
        "income_statement_0_earnings_per_share": 1.05,
        "income_statement_0_earnings_per_share_diluted": 1.02,
        "income_statement_0_investment_income": 80000000.0,
        "income_statement_0_fair_value_adjustments": 20000000.0,
        "income_statement_0_asset_impairment_loss": 40000000.0,
        "income_statement_0_financial_expenses": 60000000.0,
        "income_statement_0_taxes_and_surcharges": 70000000.0,
        "income_statement_0_other_comprehensive_income": 15000000.0,
        "income_statement_0_total_comprehensive_income": 1065000000.0,
    }


def akshare_one_mcp_server_get_income_statement(
    symbol: str, recent_n: Optional[int] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get company income statement data.

    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001')
        recent_n (Optional[int]): Number of most recent records to return. If None, returns all available.

    Returns:
        Dict containing a list of income statement records with financial metrics for reporting periods.
        Each record includes fields like 'report_date', 'currency', 'revenue', 'operating_revenue',
        'total_operating_costs', 'cost_of_revenue', 'operating_profit',
        'selling_general_and_administrative_expenses', 'operating_expense', 'research_and_development',
        'interest_expense', 'ebit', 'income_tax_expense', 'net_income', 'net_income_common_stock',
        'net_income_non_controlling_interests', 'earnings_per_share', 'earnings_per_share_diluted',
        'investment_income', 'fair_value_adjustments', 'asset_impairment_loss', 'financial_expenses',
        'taxes_and_surcharges', 'other_comprehensive_income', and 'total_comprehensive_income'.

    Raises:
        ValueError: If symbol is empty or invalid.
        TypeError: If recent_n is not None or a positive integer.
    """
    if not symbol or not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string.")

    if recent_n is not None:
        if not isinstance(recent_n, int) or recent_n <= 0:
            raise TypeError("recent_n must be a positive integer or None.")

    try:
        api_data = call_external_api("akshare-one-mcp-server-get_income_statement")

        income_statement = {
            "report_date": api_data["income_statement_0_report_date"],
            "currency": api_data["income_statement_0_currency"],
            "revenue": api_data["income_statement_0_revenue"],
            "operating_revenue": api_data["income_statement_0_operating_revenue"],
            "total_operating_costs": api_data["income_statement_0_total_operating_costs"],
            "cost_of_revenue": api_data["income_statement_0_cost_of_revenue"],
            "operating_profit": api_data["income_statement_0_operating_profit"],
            "selling_general_and_administrative_expenses": api_data[
                "income_statement_0_selling_general_and_administrative_expenses"
            ],
            "operating_expense": api_data["income_statement_0_operating_expense"],
            "research_and_development": api_data["income_statement_0_research_and_development"],
            "interest_expense": api_data["income_statement_0_interest_expense"],
            "ebit": api_data["income_statement_0_ebit"],
            "income_tax_expense": api_data["income_statement_0_income_tax_expense"],
            "net_income": api_data["income_statement_0_net_income"],
            "net_income_common_stock": api_data["income_statement_0_net_income_common_stock"],
            "net_income_non_controlling_interests": api_data[
                "income_statement_0_net_income_non_controlling_interests"
            ],
            "earnings_per_share": api_data["income_statement_0_earnings_per_share"],
            "earnings_per_share_diluted": api_data["income_statement_0_earnings_per_share_diluted"],
            "investment_income": api_data["income_statement_0_investment_income"],
            "fair_value_adjustments": api_data["income_statement_0_fair_value_adjustments"],
            "asset_impairment_loss": api_data["income_statement_0_asset_impairment_loss"],
            "financial_expenses": api_data["income_statement_0_financial_expenses"],
            "taxes_and_surcharges": api_data["income_statement_0_taxes_and_surcharges"],
            "other_comprehensive_income": api_data["income_statement_0_other_comprehensive_income"],
            "total_comprehensive_income": api_data["income_statement_0_total_comprehensive_income"],
        }

        income_statements = [income_statement]

        if recent_n is not None:
            income_statements = income_statements[-recent_n:]

        return {"income_statements": income_statements}

    except KeyError as e:
        raise RuntimeError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve income statement data: {e}")