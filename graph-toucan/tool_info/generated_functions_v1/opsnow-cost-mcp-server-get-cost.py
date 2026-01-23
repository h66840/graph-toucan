from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cloud cost information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - cost_summary_0_vendor (str): Vendor name for first cost entry
        - cost_summary_0_month (str): Month in YYYY-MM format for first cost entry
        - cost_summary_0_total_cost (float): Total cost for first entry
        - cost_summary_1_vendor (str): Vendor name for second cost entry
        - cost_summary_1_month (str): Month in YYYY-MM format for second cost entry
        - cost_summary_1_total_cost (float): Total cost for second entry
        - vendor_costs_AWS (float): Total cost for AWS across months
        - vendor_costs_Azure (float): Total cost for Azure across months
        - monthly_totals_2024_04 (float): Total cost for April 2024 across vendors
        - monthly_totals_2024_05 (float): Total cost for May 2024 across vendors
        - currency (str): Currency code used for all costs
    """
    return {
        "cost_summary_0_vendor": "AWS",
        "cost_summary_0_month": "2024-04",
        "cost_summary_0_total_cost": 1500.50,
        "cost_summary_1_vendor": "Azure",
        "cost_summary_1_month": "2024-05",
        "cost_summary_1_total_cost": 1200.75,
        "vendor_costs_AWS": 1500.50,
        "vendor_costs_Azure": 1200.75,
        "monthly_totals_2024_04": 1500.50,
        "monthly_totals_2024_05": 1200.75,
        "currency": "USD"
    }


def opsnow_cost_mcp_server_get_cost(
    months: Optional[List[str]] = None,
    vendors: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get cloud cost summary for multiple vendors and months.

    Args:
        months (Optional[List[str]]): List of months in YYYY-MM format (e.g. ['2024-04', '2024-05'])
        vendors (Optional[List[str]]): List of cloud vendor names (e.g. ['AWS', 'Azure'])

    Returns:
        Dict containing:
        - cost_summary (List[Dict]): list of cost entries with 'vendor', 'month', and 'total_cost'
        - vendor_costs (Dict): mapping of vendor names to their total costs
        - monthly_totals (Dict): mapping of month (YYYY-MM) to total cost across vendors
        - currency (str): currency code used for all cost values

    Raises:
        ValueError: If provided months are not in valid YYYY-MM format
    """
    # Validate months format if provided
    if months:
        for month in months:
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                raise ValueError(f"Invalid month format: {month}. Expected YYYY-MM")

    # Fetch data from external API (simulated)
    api_data = call_external_api("opsnow-cost-mcp-server-get-cost")

    # Construct cost_summary list from indexed fields
    cost_summary = [
        {
            "vendor": api_data["cost_summary_0_vendor"],
            "month": api_data["cost_summary_0_month"],
            "total_cost": api_data["cost_summary_0_total_cost"]
        },
        {
            "vendor": api_data["cost_summary_1_vendor"],
            "month": api_data["cost_summary_1_month"],
            "total_cost": api_data["cost_summary_1_total_cost"]
        }
    ]

    # Filter cost_summary by requested months and vendors if specified
    if months or vendors:
        filtered_summary = []
        for entry in cost_summary:
            month_match = True if not months else entry["month"] in months
            vendor_match = True if not vendors else entry["vendor"] in vendors
            if month_match and vendor_match:
                filtered_summary.append(entry)
        cost_summary = filtered_summary

    # Reconstruct vendor_costs dictionary
    vendor_costs = {}
    if "vendor_costs_AWS" in api_data:
        vendor_costs["AWS"] = api_data["vendor_costs_AWS"]
    if "vendor_costs_Azure" in api_data:
        vendor_costs["Azure"] = api_data["vendor_costs_Azure"]

    # Reconstruct monthly_totals dictionary
    monthly_totals = {}
    if "monthly_totals_2024_04" in api_data:
        monthly_totals["2024-04"] = api_data["monthly_totals_2024_04"]
    if "monthly_totals_2024_05" in api_data:
        monthly_totals["2024-05"] = api_data["monthly_totals_2024_05"]

    # Apply filtering to monthly_totals if months are specified
    if months:
        monthly_totals = {k: v for k, v in monthly_totals.items() if k in months}

    # Apply filtering to vendor_costs if vendors are specified
    if vendors:
        vendor_costs = {k: v for k, v in vendor_costs.items() if k in vendors}

    # Construct final result
    result = {
        "cost_summary": cost_summary,
        "vendor_costs": vendor_costs,
        "monthly_totals": monthly_totals,
        "currency": api_data["currency"]
    }

    return result