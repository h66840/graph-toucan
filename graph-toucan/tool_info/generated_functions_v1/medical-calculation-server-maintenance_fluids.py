from typing import Dict, Any

def medical_calculation_server_maintenance_fluids(weight_kg: float) -> Dict[str, Any]:
    """
    Calculates maintenance IV fluid rate (mL/hr) using the 4-2-1 Rule.
    
    The 4-2-1 rule calculates hourly fluid maintenance as:
    - 4 mL/kg/hr for the first 10 kg
    - 2 mL/kg/hr for the next 10 kg (11-20 kg)
    - 1 mL/kg/hr for each additional kg above 20 kg
    
    Parameters:
    -----------
    weight_kg : float
        Patient's weight in kilograms. Must be positive.
    
    Returns:
    --------
    Dict[str, Any]
        A dictionary containing:
        - maintenance_rate_mlh (float): maintenance IV fluid rate in mL/hr
    
    Raises:
    -------
    ValueError
        If weight_kg is not a positive number.
    """
    # Input validation
    if weight_kg is None:
        raise ValueError("Weight must be provided.")
    if not isinstance(weight_kg, (int, float)):
        raise ValueError("Weight must be a number.")
    if weight_kg <= 0:
        raise ValueError("Weight must be a positive number.")
    
    # Apply 4-2-1 rule
    if weight_kg <= 10:
        maintenance_rate_mlh = weight_kg * 4
    elif weight_kg <= 20:
        maintenance_rate_mlh = (10 * 4) + ((weight_kg - 10) * 2)
    else:
        maintenance_rate_mlh = (10 * 4) + (10 * 2) + ((weight_kg - 20) * 1)
    
    return {
        "maintenance_rate_mlh": float(maintenance_rate_mlh)
    }