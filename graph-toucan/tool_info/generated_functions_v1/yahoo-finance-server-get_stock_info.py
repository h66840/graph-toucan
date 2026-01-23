from typing import Dict, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching stock data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - stock_price_info_current_price (float): Current stock price
        - stock_price_info_previous_close (float): Previous day's closing price
        - stock_price_info_open (float): Today's opening price
        - stock_price_info_bid_ask (str): Bid and ask prices as string
        - stock_price_info_day_range (str): Day's trading range
        - stock_price_info_year_range (str): 52-week trading range
        - stock_price_info_volume (int): Today's trading volume
        - stock_price_info_avg_volume (int): Average daily trading volume
        - stock_price_info_market_cap (str): Market capitalization as string
        - company_info_name (str): Company name
        - company_info_sector (str): Sector classification
        - company_info_industry (str): Industry classification
        - company_info_employees (int): Number of employees
        - company_info_headquarters (str): Headquarters location
        - company_info_website (str): Official website URL
        - company_info_description (str): Company description
        - financial_metrics_pe_ratio_ttm (float): P/E ratio (TTM)
        - financial_metrics_eps_ttm (float): EPS (TTM)
        - financial_metrics_forward_pe (float): Forward P/E ratio
        - financial_metrics_peg_ratio (float): PEG ratio
        - financial_metrics_price_to_sales (float): Price to sales ratio
        - financial_metrics_price_to_book (float): Price to book ratio
        - financial_metrics_enterprise_value (str): Enterprise value as string
        - earnings_revenue_revenue_ttm (str): Revenue (TTM) as string
        - earnings_revenue_gross_profit_ttm (str): Gross profit (TTM) as string
        - earnings_revenue_operating_income_ttm (str): Operating income (TTM) as string
        - earnings_revenue_net_income_ttm (str): Net income (TTM) as string
        - earnings_revenue_diluted_eps_ttm (float): Diluted EPS (TTM)
        - earnings_revenue_earnings_growth (float): Earnings growth rate
        - margins_returns_profit_margin (float): Net profit margin
        - margins_returns_operating_margin (float): Operating margin
        - margins_returns_roa (float): Return on assets
        - margins_returns_roe (float): Return on equity
        - margins_returns_free_cashflow (str): Free cash flow as string
        - dividends_dividend_yield (float): Dividend yield percentage
        - dividends_ex_dividend_date (str): Ex-dividend date
        - dividends_payout_ratio (float): Payout ratio
        - dividends_dividend_rate (float): Annual dividend rate
        - dividends_dividends_per_share (float): Dividends per share
        - balance_sheet_total_cash (str): Total cash as string
        - balance_sheet_total_debt (str): Total debt as string
        - balance_sheet_total_equity (str): Total equity as string
        - balance_sheet_current_ratio (float): Current ratio
        - balance_sheet_debt_to_equity (float): Debt to equity ratio
        - ownership_held_by_insiders (float): Percentage held by insiders
        - ownership_held_by_institutions (float): Percentage held by institutions
        - ownership_float_shares (int): Float shares count
        - ownership_shares_outstanding (int): Shares outstanding count
        - ownership_shares_short (int): Shares short count
        - analyst_coverage_target_mean_price (float): Average analyst target price
        - analyst_coverage_target_high_price (float): Highest analyst target price
        - analyst_coverage_target_low_price (float): Lowest analyst target price
        - analyst_coverage_number_of_analysts (int): Number of analysts covering
        - analyst_coverage_recommendation (str): Analyst consensus recommendation
        - risk_metrics_beta (float): Beta coefficient
        - risk_metrics_volatility_weekly (float): Weekly volatility
        - risk_metrics_volatility_monthly (float): Monthly volatility
        - risk_metrics_short_ratio (float): Short interest ratio
        - other_fiscal_year_ends (str): Fiscal year end date
        - other_last_split_factor (str): Last stock split factor
        - other_last_split_date (str): Last stock split date
        - other_esg_score (float): ESG score
        - timestamp (str): ISO 8601 timestamp when data was fetched
        - success (bool): Whether data retrieval was successful
        - error_message (str): Error message if unsuccessful
    """
    return {
        "stock_price_info_current_price": 150.75,
        "stock_price_info_previous_close": 149.80,
        "stock_price_info_open": 150.20,
        "stock_price_info_bid_ask": "150.70 x 150.78",
        "stock_price_info_day_range": "149.50 - 151.20",
        "stock_price_info_year_range": "120.40 - 180.60",
        "stock_price_info_volume": 25345000,
        "stock_price_info_avg_volume": 30000000,
        "stock_price_info_market_cap": "2.25T",
        "company_info_name": "Apple Inc.",
        "company_info_sector": "Technology",
        "company_info_industry": "Consumer Electronics",
        "company_info_employees": 164000,
        "company_info_headquarters": "Cupertino, CA",
        "company_info_website": "https://www.apple.com",
        "company_info_description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
        "financial_metrics_pe_ratio_ttm": 28.5,
        "financial_metrics_eps_ttm": 5.27,
        "financial_metrics_forward_pe": 26.3,
        "financial_metrics_peg_ratio": 1.85,
        "financial_metrics_price_to_sales": 7.2,
        "financial_metrics_price_to_book": 38.4,
        "financial_metrics_enterprise_value": "2.45T",
        "earnings_revenue_revenue_ttm": "394.3B",
        "earnings_revenue_gross_profit_ttm": "170.3B",
        "earnings_revenue_operating_income_ttm": "114.2B",
        "earnings_revenue_net_income_ttm": "99.8B",
        "earnings_revenue_diluted_eps_ttm": 5.27,
        "earnings_revenue_earnings_growth": 12.4,
        "margins_returns_profit_margin": 25.3,
        "margins_returns_operating_margin": 28.9,
        "margins_returns_roa": 26.1,
        "margins_returns_roe": 165.4,
        "margins_returns_free_cashflow": "98.7B",
        "dividends_dividend_yield": 0.5,
        "dividends_ex_dividend_date": "2023-08-10",
        "dividends_payout_ratio": 0.22,
        "dividends_dividend_rate": 0.96,
        "dividends_dividends_per_share": 0.24,
        "balance_sheet_total_cash": "34.9B",
        "balance_sheet_total_debt": "109.5B",
        "balance_sheet_total_equity": "64.5B",
        "balance_sheet_current_ratio": 1.05,
        "balance_sheet_debt_to_equity": 1.69,
        "ownership_held_by_insiders": 0.006,
        "ownership_held_by_institutions": 0.587,
        "ownership_float_shares": 16400000000,
        "ownership_shares_outstanding": 16400000000,
        "ownership_shares_short": 120000000,
        "analyst_coverage_target_mean_price": 175.50,
        "analyst_coverage_target_high_price": 200.00,
        "analyst_coverage_target_low_price": 140.00,
        "analyst_coverage_number_of_analysts": 35,
        "analyst_coverage_recommendation": "Buy",
        "risk_metrics_beta": 1.23,
        "risk_metrics_volatility_weekly": 3.2,
        "risk_metrics_volatility_monthly": 6.8,
        "risk_metrics_short_ratio": 1.8,
        "other_fiscal_year_ends": "2023-09-30",
        "other_last_split_factor": "4:1",
        "other_last_split_date": "2020-08-31",
        "other_esg_score": 78.5,
        "timestamp": "2023-10-05T14:30:00Z",
        "success": True,
        "error_message": ""
    }


def yahoo_finance_server_get_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Get stock information for a given ticker symbol from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol of the stock to get information for, e.g. "AAPL"

    Returns:
        Dict containing comprehensive stock information with the following keys:
        - stock_price_info (Dict): Current trading information including price, volume, market cap, and related metrics
        - company_info (Dict): Basic company details
        - financial_metrics (Dict): Key financial ratios and metrics
        - earnings_revenue (Dict): Earnings and revenue data
        - margins_returns (Dict): Profitability margins and return ratios
        - dividends (Dict): Dividend-related information
        - balance_sheet (Dict): Key balance sheet items
        - ownership (Dict): Ownership structure
        - analyst_coverage (Dict): Analyst sentiment and price targets
        - risk_metrics (Dict): Risk assessments
        - other (Dict): Miscellaneous additional data
        - timestamp (str): ISO 8601 timestamp when the data was fetched
        - success (bool): Indicates whether the data retrieval was successful
        - error_message (str): Error details if success is False

    Example:
        >>> data = yahoo_finance_server_get_stock_info("AAPL")
        >>> print(data["company_info"]["name"])
        Apple Inc.
    """
    # Input validation
    if not ticker or not isinstance(ticker, str) or not ticker.strip():
        return {
            "stock_price_info": {},
            "company_info": {},
            "financial_metrics": {},
            "earnings_revenue": {},
            "margins_returns": {},
            "dividends": {},
            "balance_sheet": {},
            "ownership": {},
            "analyst_coverage": {},
            "risk_metrics": {},
            "other": {},
            "timestamp": datetime.now().isoformat() + "Z",
            "success": False,
            "error_message": "Ticker symbol is required and must be a non-empty string"
        }

    try:
        # Fetch data from external API simulation
        api_data = call_external_api("yahoo-finance-server-get_stock_info")

        # Construct nested output structure
        result = {
            "stock_price_info": {
                "current_price": api_data["stock_price_info_current_price"],
                "previous_close": api_data["stock_price_info_previous_close"],
                "open": api_data["stock_price_info_open"],
                "bid/ask": api_data["stock_price_info_bid_ask"],
                "day_range": api_data["stock_price_info_day_range"],
                "year_range": api_data["stock_price_info_year_range"],
                "volume": api_data["stock_price_info_volume"],
                "avg_volume": api_data["stock_price_info_avg_volume"],
                "market_cap": api_data["stock_price_info_market_cap"]
            },
            "company_info": {
                "name": api_data["company_info_name"],
                "sector": api_data["company_info_sector"],
                "industry": api_data["company_info_industry"],
                "employees": api_data["company_info_employees"],
                "headquarters": api_data["company_info_headquarters"],
                "website": api_data["company_info_website"],
                "description": api_data["company_info_description"]
            },
            "financial_metrics": {
                "pe_ratio_ttm": api_data["financial_metrics_pe_ratio_ttm"],
                "eps_ttm": api_data["financial_metrics_eps_ttm"],
                "forward_pe": api_data["financial_metrics_forward_pe"],
                "peg_ratio": api_data["financial_metrics_peg_ratio"],
                "price_to_sales": api_data["financial_metrics_price_to_sales"],
                "price_to_book": api_data["financial_metrics_price_to_book"],
                "enterprise_value": api_data["financial_metrics_enterprise_value"]
            },
            "earnings_revenue": {
                "revenue_ttm": api_data["earnings_revenue_revenue_ttm"],
                "gross_profit_ttm": api_data["earnings_revenue_gross_profit_ttm"],
                "operating_income_ttm": api_data["earnings_revenue_operating_income_ttm"],
                "net_income_ttm": api_data["earnings_revenue_net_income_ttm"],
                "diluted_eps_ttm": api_data["earnings_revenue_diluted_eps_ttm"],
                "earnings_growth": api_data["earnings_revenue_earnings_growth"]
            },
            "margins_returns": {
                "profit_margin": api_data["margins_returns_profit_margin"],
                "operating_margin": api_data["margins_returns_operating_margin"],
                "roa": api_data["margins_returns_roa"],
                "roe": api_data["margins_returns_roe"],
                "free_cashflow": api_data["margins_returns_free_cashflow"]
            },
            "dividends": {
                "dividend_yield": api_data["dividends_dividend_yield"],
                "ex_dividend_date": api_data["dividends_ex_dividend_date"],
                "payout_ratio": api_data["dividends_payout_ratio"],
                "dividend_rate": api_data["dividends_dividend_rate"],
                "dividends_per_share": api_data["dividends_dividends_per_share"]
            },
            "balance_sheet": {
                "total_cash": api_data["balance_sheet_total_cash"],
                "total_debt": api_data["balance_sheet_total_debt"],
                "total_equity": api_data["balance_sheet_total_equity"],
                "current_ratio": api_data["balance_sheet_current_ratio"],
                "debt_to_equity": api_data["balance_sheet_debt_to_equity"]
            },
            "ownership": {
                "held_by_insiders": api_data["ownership_held_by_insiders"],
                "held_by_institutions": api_data["ownership_held_by_institutions"],
                "float_shares": api_data["ownership_float_shares"],
                "shares_outstanding": api_data["ownership_shares_outstanding"],
                "shares_short": api_data["ownership_shares_short"]
            },
            "analyst_coverage": {
                "target_mean_price": api_data["analyst_coverage_target_mean_price"],
                "target_high_price": api_data["analyst_coverage_target_high_price"],
                "target_low_price": api_data["analyst_coverage_target_low_price"],
                "number_of_analysts": api_data["analyst_coverage_number_of_analysts"],
                "recommendation": api_data["analyst_coverage_recommendation"]
            },
            "risk_metrics": {
                "beta": api_data["risk_metrics_beta"],
                "volatility_weekly_monthly": [
                    api_data["risk_metrics_volatility_weekly"],
                    api_data["risk_metrics_volatility_monthly"]
                ],
                "short_ratio": api_data["risk_metrics_short_ratio"]
            },
            "other": {
                "fiscal_year_ends": api_data["other_fiscal_year_ends"],
                "last_split_factor": api_data["other_last_split_factor"],
                "last_split_date": api_data["other_last_split_date"],
                "esg_score": api_data["other_esg_score"]
            },
            "timestamp": api_data["timestamp"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }

        return result

    except Exception as e:
        return {
            "stock_price_info": {},
            "company_info": {},
            "financial_metrics": {},
            "earnings_revenue": {},
            "margins_returns": {},
            "dividends": {},
            "balance_sheet": {},
            "ownership": {},
            "analyst_coverage": {},
            "risk_metrics": {},
            "other": {},
            "timestamp": datetime.now().isoformat() + "Z",
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}"
        }