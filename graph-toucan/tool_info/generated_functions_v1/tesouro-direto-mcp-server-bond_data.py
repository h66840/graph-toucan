from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching bond data from external API for Tesouro Direto.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - code (int): unique numeric identifier of the bond
        - name (str): official name of the bond
        - features (str): description of the bond's payment structure and key characteristics
        - maturity_date (str): ISO 8601 date string indicating when the bond matures
        - minimum_investment_amount (float): minimum amount required to invest in BRL
        - unitary_investment_value (float): current unit value for investment in BRL
        - investment_stability (str): promotional or descriptive text about investment stability
        - semiannual_interest_indicator (bool): indicates if interest is paid semi-annually
        - receiving_income (str): target investor profile or income reception details
        - annual_investment_rate (float): annual interest rate applicable to investments in percentage
        - annual_redemption_rate (float): annual interest rate applicable at redemption in percentage
        - minimum_redemption_quantity (float): minimum quantity that can be redeemed
        - unitary_redemption_value (float): current unit value for redemption in BRL
        - minimum_redemption_value (float): minimum monetary value required for redemption in BRL
        - isin_code (str): International Securities Identification Number for the bond
        - financial_index_code (int): code of the financial index linked to the bond
        - financial_index_name (str): name of the financial index linked to the bond
        - withdrawal_date (str): ISO 8601 date string for withdrawal if applicable, otherwise null as string
        - conversion_date (str): ISO 8601 date string indicating when the bond converts to payment phase
        - business_segment_code (int): code identifying the product segment
        - business_segment_name (str): name identifying the product segment
        - amortization_quota_quantity (int): number of monthly amortization installments available after conversion
        - treasury_bond_type_code (int): code describing the bond category
        - treasury_bond_type_name (str): name describing the bond category
        - treasury_bond_type_custody_rate (float): custody rate for the bond category, or null as float
        - treasury_bond_type_gross_price (float): gross price for the bond category, or null as float
    """
    return {
        "code": 12345,
        "name": "Tesouro Selic 2025",
        "features": "Bond linked to Selic rate with daily liquidity",
        "maturity_date": "2025-08-15T00:00:00",
        "minimum_investment_amount": 30.0,
        "unitary_investment_value": 10.55,
        "investment_stability": "Low risk, government-backed investment",
        "semiannual_interest_indicator": False,
        "receiving_income": "General public, long-term investors",
        "annual_investment_rate": 13.75,
        "annual_redemption_rate": 13.50,
        "minimum_redemption_quantity": 1.0,
        "unitary_redemption_value": 10.53,
        "minimum_redemption_value": 30.0,
        "isin_code": "BRSTSRF000Q7",
        "financial_index_code": 1,
        "financial_index_name": "SELIC",
        "withdrawal_date": None,
        "conversion_date": "2025-08-15T00:00:00",
        "business_segment_code": 101,
        "business_segment_name": "Renda+",
        "amortization_quota_quantity": 12,
        "treasury_bond_type_code": 5,
        "treasury_bond_type_name": "Tesouro Selic",
        "treasury_bond_type_custody_rate": 0.003,
        "treasury_bond_type_gross_price": None
    }

def tesouro_direto_mcp_server_bond_data(code: int) -> Dict[str, Any]:
    """
    Retrieves detailed data for a specific bond from Tesouro Direto.
    
    Args:
        code (int): The numeric code of the bond to retrieve
        
    Returns:
        Dict containing detailed bond information with the following structure:
        - code (int): unique numeric identifier of the bond
        - name (str): official name of the bond
        - features (str): description of the bond's payment structure and key characteristics
        - maturity_date (str): ISO 8601 date string indicating when the bond matures
        - minimum_investment_amount (float): minimum amount required to invest in BRL
        - unitary_investment_value (float): current unit value for investment in BRL
        - investment_stability (str): promotional or descriptive text about investment stability
        - semiannual_interest_indicator (bool): indicates if interest is paid semi-annually
        - receiving_income (str): target investor profile or income reception details
        - annual_investment_rate (float): annual interest rate applicable to investments in percentage
        - annual_redemption_rate (float): annual interest rate applicable at redemption in percentage
        - minimum_redemption_quantity (float): minimum quantity that can be redeemed
        - unitary_redemption_value (float): current unit value for redemption in BRL
        - minimum_redemption_value (float): minimum monetary value required for redemption in BRL
        - isin_code (str): International Securities Identification Number for the bond
        - financial_index (Dict): contains 'code' (int) and 'name' (str) of the financial index
        - withdrawal_date (str or None): ISO 8601 date string for withdrawal if applicable
        - conversion_date (str): ISO 8601 date string indicating when the bond converts to payment phase
        - business_segment (Dict): contains 'code' (int) and 'name' (str) identifying the product segment
        - amortization_quota_quantity (int): number of monthly amortization installments available
        - treasury_bond_type (Dict): contains 'code', 'name', 'custody_rate', 'gross_price' of bond category
    """
    if not isinstance(code, int) or code <= 0:
        raise ValueError("Bond code must be a positive integer")
        
    api_data = call_external_api("tesouro-direto-mcp-server-bond_data")
    
    # Construct nested structure matching output schema
    result = {
        "code": api_data["code"],
        "name": api_data["name"],
        "features": api_data["features"],
        "maturity_date": api_data["maturity_date"],
        "minimum_investment_amount": api_data["minimum_investment_amount"],
        "unitary_investment_value": api_data["unitary_investment_value"],
        "investment_stability": api_data["investment_stability"],
        "semiannual_interest_indicator": api_data["semiannual_interest_indicator"],
        "receiving_income": api_data["receiving_income"],
        "annual_investment_rate": api_data["annual_investment_rate"],
        "annual_redemption_rate": api_data["annual_redemption_rate"],
        "minimum_redemption_quantity": api_data["minimum_redemption_quantity"],
        "unitary_redemption_value": api_data["unitary_redemption_value"],
        "minimum_redemption_value": api_data["minimum_redemption_value"],
        "isin_code": api_data["isin_code"],
        "financial_index": {
            "code": api_data["financial_index_code"],
            "name": api_data["financial_index_name"]
        },
        "withdrawal_date": api_data["withdrawal_date"],
        "conversion_date": api_data["conversion_date"],
        "business_segment": {
            "code": api_data["business_segment_code"],
            "name": api_data["business_segment_name"]
        },
        "amortization_quota_quantity": api_data["amortization_quota_quantity"],
        "treasury_bond_type": {
            "code": api_data["treasury_bond_type_code"],
            "name": api_data["treasury_bond_type_name"],
            "custody_rate": api_data["treasury_bond_type_custody_rate"],
            "gross_price": api_data["treasury_bond_type_gross_price"]
        }
    }
    
    return result