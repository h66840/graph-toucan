from typing import Dict, Any, Optional
import math

def medical_calculation_server_qtc_calculator(qt_interval: float, heart_rate: float, formula: Optional[str] = "bazett") -> Dict[str, Any]:
    """
    Corrected QT Interval (QTc) Calculator.
    
    Corrects the QT interval for heart rate extremes using various formulas.
    
    Parameters:
    -----------
    qt_interval : float
        Measured QT interval in milliseconds (ms)
    heart_rate : float
        Heart rate in beats per minute (bpm)
    formula : str, optional
        Formula to use for correction (default: "bazett")
        Options: "bazett", "fridericia", "framingham", "hodges", "rautaharju"
    
    Returns:
    --------
    dict
        Dictionary containing QTc value, interpretation, and calculation details
    """
    # Input validation
    if not isinstance(qt_interval, (int, float)) or qt_interval <= 0:
        raise ValueError("qt_interval must be a positive number")
    if not isinstance(heart_rate, (int, float)) or heart_rate <= 0:
        raise ValueError("heart_rate must be a positive number")
    if formula is None:
        formula = "bazett"
    if formula.lower() not in ["bazett", "fridericia", "framingham", "hodges", "rautaharju"]:
        raise ValueError("formula must be one of: bazett, fridericia, framingham, hodges, rautaharju")
    
    # Calculate RR interval in seconds
    rr_interval = 60.0 / heart_rate
    
    # Apply the selected formula
    formula_lower = formula.lower()
    if formula_lower == "bazett":
        qtc = qt_interval / math.sqrt(rr_interval)
        calculation = f"QTc = {qt_interval} / √({rr_interval:.3f}) = {qtc:.1f}"
        formula_used = "Bazett"
    elif formula_lower == "fridericia":
        qtc = qt_interval / (rr_interval ** (1/3))
        calculation = f"QTc = {qt_interval} / ({rr_interval:.3f})^(1/3) = {qtc:.1f}"
        formula_used = "Fridericia"
    elif formula_lower == "framingham":
        qtc = qt_interval + 154 * (1 - rr_interval)
        calculation = f"QTc = {qt_interval} + 154 × (1 - {rr_interval:.3f}) = {qtc:.1f}"
        formula_used = "Framingham"
    elif formula_lower == "hodges":
        qtc = qt_interval + 1.75 * (heart_rate - 60)
        calculation = f"QTc = {qt_interval} + 1.75 × ({heart_rate} - 60) = {qtc:.1f}"
        formula_used = "Hodges"
    elif formula_lower == "rautaharju":
        qtc = qt_interval * (120 + heart_rate) / 180
        calculation = f"QTc = {qt_interval} × (120 + {heart_rate}) / 180 = {qtc:.1f}"
        formula_used = "Rautaharju"
    else:
        raise ValueError(f"Unsupported formula: {formula}")
    
    # Round QTc to 1 decimal place
    qtc = round(qtc, 1)
    
    # Interpretation and risk assessment based on QTc value
    # General clinical guidelines (may vary by source and population)
    if qtc < 350:
        interpretation = "Short"
        risk_assessment = "Low"
    elif 350 <= qtc <= 440:
        interpretation = "Normal"
        risk_assessment = "Low"
    elif 441 <= qtc <= 470:
        interpretation = "Borderline"
        risk_assessment = "Intermediate"
    elif qtc > 470:
        interpretation = "Prolonged"
        risk_assessment = "High"
    else:
        interpretation = "Unknown"
        risk_assessment = "Unknown"
    
    # Add gender-specific note for prolonged QTc (general clinical note)
    note = (
        "Reference ranges: Normal QTc < 440 ms (men) or < 460 ms (women); "
        "Borderline: 440-470 ms (men) or 460-480 ms (women); "
        "Prolonged: > 470 ms (men) or > 480 ms (women). "
        "QTc > 500 ms is associated with increased arrhythmia risk. "
        "Clinical correlation recommended."
    )
    
    # Return the result dictionary
    return {
        "qtc": qtc,
        "qt_interval": float(qt_interval),
        "heart_rate": float(heart_rate),
        "rr_interval": round(rr_interval, 3),
        "formula_used": formula_used,
        "interpretation": interpretation,
        "risk_assessment": risk_assessment,
        "calculation": calculation,
        "note": note
    }