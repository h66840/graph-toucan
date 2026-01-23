from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching financial statement data from external API for SET stock.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - business_type (str): Description of the company's business operations in Thai
        - unit (str): Unit of measurement for financial values (e.g., "Million THB")
        - income_statement_0_accountCode (str): Account code for first income statement item
        - income_statement_0_accountName (str): Account name for first income statement item
        - income_statement_0_2024 (float): Value for 2024 of first income statement item
        - income_statement_1_accountCode (str): Account code for second income statement item
        - income_statement_1_accountName (str): Account name for second income statement item
        - income_statement_1_2024 (float): Value for 2024 of second income statement item
        - balance_sheet_0_accountCode (str): Account code for first balance sheet item
        - balance_sheet_0_accountName (str): Account name for first balance sheet item
        - balance_sheet_0_2024 (float): Value for 2024 of first balance sheet item
        - balance_sheet_1_accountCode (str): Account code for second balance sheet item
        - balance_sheet_1_accountName (str): Account name for second balance sheet item
        - balance_sheet_1_2024 (float): Value for 2024 of second balance sheet item
        - cash_flow_statement_0_accountCode (str): Account code for first cash flow item
        - cash_flow_statement_0_accountName (str): Account name for first cash flow item
        - cash_flow_statement_0_2024 (float): Value for 2024 of first cash flow item
        - cash_flow_statement_1_accountCode (str): Account code for second cash flow item
        - cash_flow_statement_1_accountName (str): Account name for second cash flow item
        - cash_flow_statement_1_2024 (float): Value for 2024 of second cash flow item
    """
    return {
        "business_type": "บริษัทดำเนินธุรกิจด้านการผลิตและจำหน่ายสินค้าอุปโภคบริโภค",
        "unit": "Million THB",
        "income_statement_0_accountCode": "REV",
        "income_statement_0_accountName": "Revenue",
        "income_statement_0_2024": 15000.0,
        "income_statement_1_accountCode": "NET",
        "income_statement_1_accountName": "Net Profit",
        "income_statement_1_2024": 2500.0,
        "balance_sheet_0_accountCode": "AST",
        "balance_sheet_0_accountName": "Total Assets",
        "balance_sheet_0_2024": 30000.0,
        "balance_sheet_1_accountCode": "LIA",
        "balance_sheet_1_accountName": "Total Liabilities",
        "balance_sheet_1_2024": 18000.0,
        "cash_flow_statement_0_accountCode": "OPR",
        "cash_flow_statement_0_accountName": "Operating Cash Flow",
        "cash_flow_statement_0_2024": 3200.0,
        "cash_flow_statement_1_accountCode": "INV",
        "cash_flow_statement_1_accountName": "Investing Cash Flow",
        "cash_flow_statement_1_2024": -1200.0,
    }

def set_mcp_get_financial_statement(symbol: str, from_year: int, to_year: int) -> str:
    """
    Get the balance sheet of stock in The Securities Exchange of Thailand (SET).
    
    Args:
        symbol (str): Stock symbol in The Securities Exchange of Thailand (SET).
        from_year (int): The start YEAR of the financial statement (e.g., 2024).
        to_year (int): The end YEAR of the financial statement (e.g., 2024).
    
    Returns:
        str: The constructed financial statement including Income Statement, Balance Sheet,
             and Cash Flow Statement in CSV format with | as the delimiter.
    
    Raises:
        ValueError: If symbol is empty or years are invalid.
    """
    if not symbol:
        raise ValueError("Symbol must not be empty.")
    if from_year < 1900 or from_year > 2100 or to_year < 1900 or to_year > 2100:
        raise ValueError("Year must be between 1900 and 2100.")
    if from_year > to_year:
        raise ValueError("from_year cannot be greater than to_year.")

    # Call external API to get flat data
    api_data = call_external_api("set-mcp-get_financial_statement")

    # Construct nested structures from flat API data
    income_statement = [
        {
            "accountCode": api_data["income_statement_0_accountCode"],
            "accountName": api_data["income_statement_0_accountName"],
            from_year: api_data["income_statement_0_2024"]
        },
        {
            "accountCode": api_data["income_statement_1_accountCode"],
            "accountName": api_data["income_statement_1_accountName"],
            from_year: api_data["income_statement_1_2024"]
        }
    ]

    balance_sheet = [
        {
            "accountCode": api_data["balance_sheet_0_accountCode"],
            "accountName": api_data["balance_sheet_0_accountName"],
            from_year: api_data["balance_sheet_0_2024"]
        },
        {
            "accountCode": api_data["balance_sheet_1_accountCode"],
            "accountName": api_data["balance_sheet_1_accountName"],
            from_year: api_data["balance_sheet_1_2024"]
        }
    ]

    cash_flow_statement = [
        {
            "accountCode": api_data["cash_flow_statement_0_accountCode"],
            "accountName": api_data["cash_flow_statement_0_accountName"],
            from_year: api_data["cash_flow_statement_0_2024"]
        },
        {
            "accountCode": api_data["cash_flow_statement_1_accountCode"],
            "accountName": api_data["cash_flow_statement_1_accountName"],
            from_year: api_data["cash_flow_statement_1_2024"]
        }
    ]

    # Build CSV content with | delimiter
    csv_lines = []

    # Header line
    header = ["Statement", "Account Code", "Account Name", str(from_year)]
    if from_year != to_year:
        header.append(str(to_year))
    csv_lines.append("|".join(header))

    # Add Income Statement
    csv_lines.append("Income Statement|||")
    for item in income_statement:
        row = [
            "",
            item["accountCode"],
            item["accountName"],
            str(item.get(from_year, ""))
        ]
        csv_lines.append("|".join(row))

    # Add Balance Sheet
    csv_lines.append("Balance Sheet|||")
    for item in balance_sheet:
        row = [
            "",
            item["accountCode"],
            item["accountName"],
            str(item.get(from_year, ""))
        ]
        csv_lines.append("|".join(row))

    # Add Cash Flow Statement
    csv_lines.append("Cash Flow Statement|||")
    for item in cash_flow_statement:
        row = [
            "",
            item["accountCode"],
            item["accountName"],
            str(item.get(from_year, ""))
        ]
        csv_lines.append("|".join(row))

    return "\n".join(csv_lines)