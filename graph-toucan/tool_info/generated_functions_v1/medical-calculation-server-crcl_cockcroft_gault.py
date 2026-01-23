from typing import Dict, Any

def medical_calculation_server_crcl_cockcroft_gault(age: int, height: float, scr: float, sex: str, weight: float) -> Dict[str, Any]:
    """
    Calculate Creatinine Clearance using the Cockcroft-Gault formula.
    
    Parameters:
    -----------
    age : int
        Age in years
    weight : float
        Actual body weight in kg
    height : float
        Height in inches
    scr : float
        Serum creatinine in mg/dL
    sex : str
        Gender ('male' or 'female')
    
    Returns:
    --------
    dict
        Dictionary containing:
        - creatinine_clearance (float): estimated creatinine clearance in mL/min
        - ibw (float): ideal body weight in kg
        - abw (float): adjusted body weight in kg
        - weight_used (str): description of which weight was used and BMI category
    """
    # Input validation
    if age <= 0:
        raise ValueError("Age must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")
    if scr <= 0:
        raise ValueError("Serum creatinine must be positive")
    if sex.lower() not in ['male', 'female']:
        raise ValueError("Sex must be 'male' or 'female'")
    
    # Convert height from inches to cm
    height_cm = height * 2.54
    
    # Calculate Ideal Body Weight (IBW)
    if sex.lower() == 'male':
        if height_cm > 152.4:
            ibw = 50.0 + 2.3 * (height_cm - 152.4) / 2.54
        else:
            ibw = 50.0
    else:  # female
        if height_cm > 152.4:
            ibw = 45.5 + 2.3 * (height_cm - 152.4) / 2.54
        else:
            ibw = 45.5
    
    # Calculate BMI
    bmi = weight / ((height_cm / 100) ** 2)
    
    # Determine weight to use and calculate ABW
    if bmi < 18.5:
        weight_used_value = weight
        weight_used_desc = "Actual body weight (Underweight BMI)"
    elif 18.5 <= bmi <= 25:
        weight_used_value = ibw
        weight_used_desc = "IBW (Normal BMI)"
    elif 25 < bmi < 40:
        # Calculate Adjusted Body Weight (ABW)
        abw = ibw + 0.4 * (weight - ibw)
        weight_used_value = abw
        weight_used_desc = "ABW (Overweight/Obese BMI)"
    else:  # bmi >= 40
        weight_used_value = ibw
        weight_used_desc = "IBW (Morbidly Obese BMI)"
    
    # Calculate Creatinine Clearance using Cockcroft-Gault formula
    if sex.lower() == 'male':
        crcl = ((140 - age) * weight_used_value) / (72 * scr)
    else:
        crcl = ((140 - age) * weight_used_value * 0.85) / (72 * scr)
    
    # Round results
    crcl = round(crcl, 2)
    ibw = round(ibw, 2)
    
    # Prepare result
    result = {
        "creatinine_clearance": crcl,
        "ibw": ibw,
        "abw": weight_used_value if 'abw' in locals() else None,
        "weight_used": weight_used_desc
    }
    
    return result