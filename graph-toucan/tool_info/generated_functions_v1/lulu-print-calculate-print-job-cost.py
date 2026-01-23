from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for print job cost calculation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - product_id (str): Lulu product ID for which the cost was calculated
        - quantity (int): Number of copies included in the print job
        - unit_cost (float): Cost per unit in the specified currency
        - total_cost (float): Total cost for the entire print job (unit_cost × quantity)
        - currency (str): Currency code in which the cost is expressed, e.g., "USD"
        - message (str): Additional informational message from the system
    """
    # Simulate realistic pricing logic based on product_id and quantity
    base_price_map = {
        "POD-BK-001": 5.99,
        "POD-BK-002": 8.50,
        "POD-MG-001": 3.25,
        "POD-TP-001": 12.00,
    }
    
    # Default to a base price if product_id not in map
    base_price = base_price_map.get("POD-BK-001", 5.99)
    
    # Adjust price slightly by product_id hash to simulate variation
    price_modifier = sum(ord(c) for c in tool_name) % 10 / 100
    unit_cost = round(base_price * (1 + price_modifier), 2)
    
    # Calculate total cost
    total_cost = round(unit_cost * 100, 2)  # Assume quantity 100 for simulation
    
    return {
        "product_id": "POD-BK-001",
        "quantity": 100,
        "unit_cost": unit_cost,
        "total_cost": total_cost,
        "currency": "USD",
        "message": "Cost estimate generated successfully. No print job created."
    }

def lulu_print_calculate_print_job_cost(product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Calculate the cost of a print job without creating it.
    
    This function simulates calling an external API to calculate the cost of printing
    a certain quantity of a product, returning detailed cost information including
    unit cost, total cost, and currency.
    
    Args:
        product_id (str): Lulu product ID (required)
        quantity (int): Number of copies (required)
    
    Returns:
        Dict containing:
        - product_id (str): the Lulu product ID for which the cost was calculated
        - quantity (int): number of copies included in the print job
        - unit_cost (float): cost per unit in the specified currency
        - total_cost (float): total cost for the entire print job (unit_cost × quantity)
        - currency (str): the currency code in which the cost is expressed, e.g., "USD"
        - message (str): additional informational message from the system
    
    Raises:
        ValueError: If product_id is empty or quantity is less than 1
    """
    # Input validation
    if not product_id or not product_id.strip():
        raise ValueError("product_id is required")
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    
    # Clean inputs
    product_id = product_id.strip()
    
    # Call external API (simulation)
    api_data = call_external_api("lulu-print-calculate-print-job-cost")
    
    # Extract base values from API response
    unit_cost = api_data["unit_cost"]
    currency = api_data["currency"]
    message = api_data["message"]
    
    # Recalculate total cost based on actual input quantity
    total_cost = round(unit_cost * quantity, 2)
    
    # Construct result matching output schema
    result = {
        "product_id": product_id,
        "quantity": quantity,
        "unit_cost": unit_cost,
        "total_cost": total_cost,
        "currency": currency,
        "message": message
    }
    
    return result