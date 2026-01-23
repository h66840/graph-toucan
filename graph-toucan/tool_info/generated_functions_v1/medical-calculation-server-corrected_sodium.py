from typing import Dict

def medical_calculation_server_corrected_sodium(measured_sodium: float, serum_glucose: float) -> Dict[str, float]:
    """
    Calculates corrected sodium level in the setting of hyperglycemia using Katz and Hillier formulas.
    
    Parameters:
    -----------
    measured_sodium : float
        Measured serum sodium in mEq/L.
    serum_glucose : float
        Serum glucose in mg/dL.
    
    Returns:
    --------
    dict
        Dictionary with corrected sodium values using Katz and Hillier formulas:
        - katz (float): Corrected sodium using Katz formula (mEq/L)
        - hillier (float): Corrected sodium using Hillier formula (mEq/L)
    
    Raises:
    -------
    ValueError
        If measured_sodium or serum_glucose are negative or non-numeric.
    """
    # Input validation
    if not isinstance(measured_sodium, (int, float)) or not isinstance(serum_glucose, (int, float)):
        raise ValueError("Both measured_sodium and serum_glucose must be numeric.")
    if measured_sodium < 0:
        raise ValueError("Measured sodium cannot be negative.")
    if serum_glucose < 0:
        raise ValueError("Serum glucose cannot be negative.")
    
    # Katz formula: Corrected Sodium = Measured Sodium + 0.016 * (Glucose - 100)
    katz_corrected = measured_sodium + 0.016 * (serum_glucose - 100)
    
    # Hillier formula: Corrected Sodium = Measured Sodium + 0.023 * (Glucose - 100)
    hillier_corrected = measured_sodium + 0.023 * (serum_glucose - 100)
    
    return {
        "katz": round(katz_corrected, 2),
        "hillier": round(hillier_corrected, 2)
    }