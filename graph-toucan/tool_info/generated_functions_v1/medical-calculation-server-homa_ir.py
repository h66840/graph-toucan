from typing import Dict, Any

def medical_calculation_server_homa_ir(fasting_glucose: float, fasting_insulin: float) -> Dict[str, Any]:
    """
    Calculates the HOMA-IR score for insulin resistance based on fasting insulin and glucose levels.
    
    Formula:
        HOMA-IR Score = (Fasting insulin (uIU/mL) * Fasting glucose (mg/dL)) / 405
    
    Parameters:
    -----------
    fasting_glucose : float
        Fasting glucose level in milligrams per deciliter (mg/dL).
    fasting_insulin : float
        Fasting insulin level in micro-units per milliliter (uIU/mL).
    
    Returns:
    --------
    Dict[str, Any]
        A dictionary containing the calculated HOMA-IR score.
        - homa_ir_score (float): HOMA-IR score calculated from fasting insulin and glucose levels.
    
    Raises:
    -------
    ValueError:
        If fasting_glucose or fasting_insulin is negative.
    TypeError:
        If inputs are not numeric.
    """
    # Input validation
    if not isinstance(fasting_glucose, (int, float)):
        raise TypeError("Fasting glucose must be a number.")
    if not isinstance(fasting_insulin, (int, float)):
        raise TypeError("Fasting insulin must be a number.")
    
    if fasting_glucose < 0:
        raise ValueError("Fasting glucose cannot be negative.")
    if fasting_insulin < 0:
        raise ValueError("Fasting insulin cannot be negative.")
    
    # Calculation
    homa_ir_score = (fasting_insulin * fasting_glucose) / 405.0
    
    return {
        "homa_ir_score": float(homa_ir_score)
    }