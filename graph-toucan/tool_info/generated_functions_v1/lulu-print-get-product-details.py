from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Lulu product details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - product_id (str): unique identifier for the Lulu product
        - name (str): name of the product as displayed by Lulu
        - type (str): type of the product, e.g., "Paperback", "Hardcover"
        - dimensions (str): physical dimensions of the product in format like "6x9 inches"
        - message (str): additional informational message about the data, such as mock status or API notes
    """
    return {
        "product_id": "9781234567890",
        "name": "The Art of Python Programming",
        "type": "Paperback",
        "dimensions": "6x9 inches",
        "message": "Mock data provided for demonstration purposes."
    }

def lulu_print_get_product_details(product_id: str) -> Dict[str, Any]:
    """
    Get specifications and details for a Lulu product based on the provided product ID.
    
    This function retrieves product information such as name, type, dimensions, and additional
    messages by querying an external API through a helper function. The response is structured
    to match the expected output schema.
    
    Args:
        product_id (str): Lulu product ID (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - product_id (str): unique identifier for the Lulu product
            - name (str): name of the product as displayed by Lulu
            - type (str): type of the product, e.g., "Paperback", "Hardcover"
            - dimensions (str): physical dimensions of the product in format like "6x9 inches"
            - message (str): additional informational message about the data
    
    Raises:
        ValueError: If product_id is empty or not a string
    """
    if not product_id or not isinstance(product_id, str):
        raise ValueError("product_id must be a non-empty string")

    # Fetch data from external API (simulated)
    api_data = call_external_api("lulu-print-get-product-details")
    
    # Construct result dictionary matching the output schema
    result = {
        "product_id": api_data["product_id"],
        "name": api_data["name"],
        "type": api_data["type"],
        "dimensions": api_data["dimensions"],
        "message": api_data["message"]
    }
    
    return result