from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching bond data from external API for Tesouro Direto.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - criteria_bondType (str): Bond type used in search criteria
        - criteria_maturityAfter (str): Maturity after date in YYYY-MM-DD
        - criteria_maturityBefore (str): Maturity before date in YYYY-MM-DD
        - total_results (int): Total number of matching bonds
        - bond_0_code (int): First bond code
        - bond_0_name (str): First bond name
        - bond_0_type (str): First bond type
        - bond_0_maturity_date (str): First bond maturity date (ISO format)
        - bond_0_investment_rate (float): First bond investment rate
        - bond_0_redemption_rate (float): First bond redemption rate
        - bond_0_minimum_investment (float): First bond minimum investment
        - bond_1_code (int): Second bond code
        - bond_1_name (str): Second bond name
        - bond_1_type (str): Second bond type
        - bond_1_maturity_date (str): Second bond maturity date (ISO format)
        - bond_1_investment_rate (float): Second bond investment rate
        - bond_1_redemption_rate (float): Second bond redemption rate
        - bond_1_minimum_investment (float): Second bond minimum investment
    """
    return {
        "criteria_bondType": "IPCA",
        "criteria_maturityAfter": "2025-01-01",
        "criteria_maturityBefore": "2030-12-31",
        "total_results": 2,
        "bond_0_code": 1001,
        "bond_0_name": "Tesouro IPCA+ 2026",
        "bond_0_type": "IPCA",
        "bond_0_maturity_date": "2026-08-15",
        "bond_0_investment_rate": 0.052,
        "bond_0_redemption_rate": 0.015,
        "bond_0_minimum_investment": 30.0,
        "bond_1_code": 1002,
        "bond_1_name": "Tesouro IPCA+ 2028",
        "bond_1_type": "IPCA",
        "bond_1_maturity_date": "2028-02-01",
        "bond_1_investment_rate": 0.055,
        "bond_1_redemption_rate": 0.017,
        "bond_1_minimum_investment": 30.0,
    }

def tesouro_direto_mcp_server_search_bonds(
    bondType: Optional[str] = None,
    maturityAfter: Optional[str] = None,
    maturityBefore: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for Brazilian government bonds (Tesouro Direto) by bond type or maturity date range.

    Args:
        bondType (Optional[str]): Filter by bond type. One of: ANY, SELIC, IPCA, PREFIXADO. Defaults to ANY.
        maturityAfter (Optional[str]): Filter bonds maturing after this date (YYYY-MM-DD).
        maturityBefore (Optional[str]): Filter bonds maturing before this date (YYYY-MM-DD).

    Returns:
        Dict containing:
        - criteria (Dict): The search criteria used
        - total_results (int): Number of bonds matching criteria
        - bonds (List[Dict]): List of bond details with code, name, type, maturity_date,
          investment_rate, redemption_rate, and minimum_investment

    Raises:
        ValueError: If maturity dates are not in valid YYYY-MM-DD format
    """
    # Validate date formats if provided
    for date_str, name in [(maturityAfter, "maturityAfter"), (maturityBefore, "maturityBefore")]:
        if date_str is not None:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format for {name}: {date_str}. Expected YYYY-MM-DD")

    # Normalize bond type
    valid_types = ["ANY", "SELIC", "IPCA", "PREFIXADO"]
    if bondType is None:
        bondType = "ANY"
    bondType = bondType.upper()
    if bondType not in valid_types:
        raise ValueError(f"Invalid bondType: {bondType}. Must be one of {valid_types}")

    # Fetch data from external API (simulated)
    api_data = call_external_api("tesouro_direto_mcp_server_search_bonds")

    # Construct criteria object
    criteria = {
        "bondType": bondType,
        "maturityAfter": maturityAfter or api_data.get("criteria_maturityAfter"),
        "maturityBefore": maturityBefore or api_data.get("criteria_maturityBefore")
    }

    # Reconstruct bonds list from flattened API response
    bonds = [
        {
            "code": api_data["bond_0_code"],
            "name": api_data["bond_0_name"],
            "type": api_data["bond_0_type"],
            "maturity_date": api_data["bond_0_maturity_date"],
            "investment_rate": api_data["bond_0_investment_rate"],
            "redemption_rate": api_data["bond_0_redemption_rate"],
            "minimum_investment": api_data["bond_0_minimum_investment"]
        },
        {
            "code": api_data["bond_1_code"],
            "name": api_data["bond_1_name"],
            "type": api_data["bond_1_type"],
            "maturity_date": api_data["bond_1_maturity_date"],
            "investment_rate": api_data["bond_1_investment_rate"],
            "redemption_rate": api_data["bond_1_redemption_rate"],
            "minimum_investment": api_data["bond_1_minimum_investment"]
        }
    ]

    # Apply filtering logic based on input parameters
    filtered_bonds = []
    for bond in bonds:
        # Filter by bond type
        if bondType != "ANY" and bond["type"] != bondType:
            continue

        # Filter by maturity date range
        bond_date = datetime.strptime(bond["maturity_date"], "%Y-%m-%d")
        if maturityAfter is not None:
            after_date = datetime.strptime(maturityAfter, "%Y-%m-%d")
            if bond_date <= after_date:
                continue
        if maturityBefore is not None:
            before_date = datetime.strptime(maturityBefore, "%Y-%m-%d")
            if bond_date >= before_date:
                continue

        filtered_bonds.append(bond)

    # Return final result structure
    return {
        "criteria": criteria,
        "total_results": len(filtered_bonds),
        "bonds": filtered_bonds
    }