from typing import Dict, Any

def model_context_protocol_server_calculate_bmi(height_m: float, weight_kg: float) -> Dict[str, Any]:
    """
    Calculate Body Mass Index (BMI) given weight in kilograms and height in meters.
    
    BMI is calculated using the formula: BMI = weight (kg) / (height (m))²
    The result is returned as a floating-point number.

    Parameters:
        height_m (float): Height in meters. Must be a positive number.
        weight_kg (float): Weight in kilograms. Must be a positive number.

    Returns:
        Dict[str, Any]: A dictionary containing the calculated BMI value.
            - bmi (float): The calculated Body Mass Index value.

    Raises:
        ValueError: If height_m or weight_kg is not positive.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    bmi = weight_kg / (height_m ** 2)
    
    return {"bmi": float(bmi)}