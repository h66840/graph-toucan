from typing import Dict, Any

def mcp_server_get_bmi(height: float, weight: float) -> Dict[str, Any]:
    """
    Calculate the Body Mass Index (BMI) of a person given their height and weight.
    
    BMI is calculated using the formula: BMI = weight (kg) / (height (m))²
    The result is returned as a numerical value.

    Parameters:
        height (float): Height of the person in meters. Must be a positive number.
        weight (float): Weight of the person in kilograms. Must be a positive number.

    Returns:
        Dict[str, Any]: A dictionary containing the calculated BMI value.
            - bmi_value (float): The calculated Body Mass Index (BMI) as a numerical value.

    Raises:
        ValueError: If height or weight is not a positive number.
    """
    # Input validation
    if not isinstance(height, (int, float)) or not isinstance(weight, (int, float)):
        raise TypeError("Height and weight must be numeric values.")
    
    if height <= 0:
        raise ValueError("Height must be a positive number.")
    
    if weight <= 0:
        raise ValueError("Weight must be a positive number.")
    
    # Calculate BMI
    bmi_value = weight / (height ** 2)
    
    return {
        "bmi_value": round(bmi_value, 2)  # Round to 2 decimal places for readability
    }