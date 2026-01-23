from typing import Dict, Any

def medical_calculation_server_bmi_bsa_calculator(weight: float, height: float, height_unit: str = 'cm') -> Dict[str, Any]:
    """
    Calculates Body Mass Index (BMI) and Body Surface Area (BSA) based on weight and height.
    
    Parameters:
    -----------
    weight : float
        Weight in kilograms. Must be a positive number.
    height : float
        Height in centimeters (default) or meters. Must be a positive number.
    height_unit : str, optional
        Unit of height measurement, either 'cm' for centimeters or 'm' for meters. Default is 'cm'.
    
    Returns:
    --------
    dict
        Dictionary containing:
        - bmi (float): Body Mass Index value calculated as weight(kg) / height(m)²
        - bsa (float): Body Surface Area in square meters using Mosteller formula
        - bmi_classification (str): Classification category based on BMI value
        - formulas (Dict): Mathematical formulas used for BMI and BSA calculations
    
    Raises:
    -------
    ValueError
        If weight or height is not positive, or if height_unit is not 'cm' or 'm'
    """
    # Input validation
    if weight <= 0:
        raise ValueError("Weight must be a positive number.")
    if height <= 0:
        raise ValueError("Height must be a positive number.")
    if height_unit not in ['cm', 'm']:
        raise ValueError("Height unit must be either 'cm' or 'm'.")
    
    # Convert height to meters if in centimeters
    if height_unit == 'cm':
        height_m = height / 100.0
        height_cm = height
    else:  # height_unit == 'm'
        height_m = height
        height_cm = height * 100.0
    
    # Calculate BMI: weight(kg) / height(m)^2
    bmi = weight / (height_m ** 2)
    
    # Classify BMI
    if bmi < 18.5:
        bmi_classification = "Underweight"
    elif 18.5 <= bmi < 25:
        bmi_classification = "Normal weight"
    elif 25 <= bmi < 30:
        bmi_classification = "Overweight"
    else:  # bmi >= 30
        bmi_classification = "Obese"
    
    # Calculate BSA using Mosteller formula: √(height(cm) × weight(kg) / 3600)
    bsa = (height_cm * weight / 3600) ** 0.5
    
    # Formulas used
    formulas = {
        "bmi": "BMI = weight(kg) / height(m)²",
        "bsa": "BSA = √(height(cm) × weight(kg) / 3600)"
    }
    
    return {
        "bmi": round(bmi, 2),
        "bsa": round(bsa, 2),
        "bmi_classification": bmi_classification,
        "formulas": formulas
    }