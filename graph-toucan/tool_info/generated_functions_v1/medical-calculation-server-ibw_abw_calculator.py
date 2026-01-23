from typing import Dict, Any

def medical_calculation_server_ibw_abw_calculator(weight_kg: float, height_inches: float, male: bool) -> Dict[str, Any]:
    """
    Ideal Body Weight and Adjusted Body Weight Calculator using the Devine formula.
    
    Parameters:
    -----------
    weight_kg : float
        Actual body weight in kilograms
    height_inches : float
        Height in inches
    male : bool
        True if patient is male, False if female
    
    Returns:
    --------
    dict
        Dictionary containing:
        - ideal_body_weight_kg: Ideal body weight in kg
        - adjusted_body_weight_kg: Adjusted body weight in kg
        - ibw_formula_used: Description of the IBW formula applied
        - deviation_from_ibw_percent: Percentage deviation of actual weight from IBW
        - is_overweight_for_ibw: True if actual weight exceeds IBW
        - calculation_details: Structured breakdown of inputs and calculation steps
    
    Raises:
    -------
    ValueError
        If weight_kg or height_inches are non-positive
    """
    # Input validation
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
    if height_inches <= 0:
        raise ValueError("Height must be positive")
    
    # Calculate height over 60 inches
    height_over_60 = max(0, height_inches - 60)
    
    # Calculate Ideal Body Weight (IBW) using Devine formula
    if male:
        ibw_kg = 50.0 + 2.3 * height_over_60
        ibw_formula_used = "Men: IBW = 50 kg + 2.3 kg × (height in inches - 60)"
    else:
        ibw_kg = 45.5 + 2.3 * height_over_60
        ibw_formula_used = "Women: IBW = 45.5 kg + 2.3 kg × (height in inches - 60)"
    
    # Calculate Adjusted Body Weight (ABW)
    abw_kg = ibw_kg + 0.4 * (weight_kg - ibw_kg)
    
    # Calculate deviation from IBW in percentage
    deviation_from_ibw_percent = ((weight_kg - ibw_kg) / ibw_kg) * 100.0
    
    # Determine if patient is overweight compared to IBW
    is_overweight_for_ibw = weight_kg > ibw_kg
    
    # Construct calculation details
    calculation_details = {
        "height_inches": height_inches,
        "weight_kg": weight_kg,
        "sex": "male" if male else "female",
        "height_over_60_inches": height_over_60,
        "ibw_multiplier_kg_per_inch": 2.3,
        "base_ibw_kg": 50.0 if male else 45.5,
        "ibw_calculation_step": f"{calculation_details['base_ibw_kg']} + (2.3 × {calculation_details['height_over_60_inches']})",
        "abw_calculation_step": f"{ibw_kg} + 0.4 × ({weight_kg} - {ibw_kg})"
    }
    
    # Return result dictionary
    return {
        "ideal_body_weight_kg": round(ibw_kg, 2),
        "adjusted_body_weight_kg": round(abw_kg, 2),
        "ibw_formula_used": ibw_formula_used,
        "deviation_from_ibw_percent": round(deviation_from_ibw_percent, 2),
        "is_overweight_for_ibw": is_overweight_for_ibw,
        "calculation_details": calculation_details
    }