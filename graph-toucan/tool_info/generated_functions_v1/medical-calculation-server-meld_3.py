from typing import Dict, Any

def medical_calculation_server_meld_3(
    age: int,
    albumin: float,
    bilirubin: float,
    creatinine: float,
    dialysis: bool,
    female: bool,
    inr: float,
    sodium: float
) -> Dict[str, Any]:
    """
    Calculates the MELD 3.0 Score for liver disease transplant planning.

    Parameters:
    -----------
    age : int
        Patient age in years.
    female : bool
        True if patient is female.
    bilirubin : float
        Serum bilirubin in mg/dL.
    inr : float
        INR (International Normalized Ratio).
    creatinine : float
        Serum creatinine in mg/dL.
    albumin : float
        Serum albumin in g/dL.
    sodium : float
        Serum sodium in mEq/L.
    dialysis : bool
        True if patient had ≥2 dialysis sessions or 24h CVVHD in last 7 days.

    Returns:
    --------
    Dict with the following keys:
        - meld_score (int): MELD 3.0 score rounded to nearest whole number
        - interpretation (str): Clinical interpretation of the MELD score
        - risk_level (str): Mortality risk category
        - calculation_metadata (Dict): Additional details about the calculation
    """
    # Input validation
    if age < 0:
        raise ValueError("Age must be non-negative.")
    if bilirubin < 0:
        raise ValueError("Bilirubin must be non-negative.")
    if inr < 0:
        raise ValueError("INR must be non-negative.")
    if creatinine < 0:
        raise ValueError("Creatinine must be non-negative.")
    if albumin <= 0:
        raise ValueError("Albumin must be positive.")
    if not (120 <= sodium <= 160):
        raise ValueError("Sodium must be between 120 and 160 mEq/L.")

    # MELD 3.0 formula components
    # Log transformations
    log_bilirubin = 0.0
    if bilirubin > 0:
        log_bilirubin = max(0.0, min(2.0, (bilirubin - 1.0) / 4.0))

    log_creatinine = 0.0
    if creatinine > 0:
        log_creatinine = max(0.0, min(2.0, (creatinine - 0.8) / 1.5))

    log_inr = 0.0
    if inr > 0:
        log_inr = max(0.0, min(2.0, (inr - 1.0) / 3.0))

    # Sodium component (with adjustment to avoid division by zero or extreme values)
    sodium_adj = max(125, min(135, sodium))
    sodium_component = (137 - sodium_adj) / 12.0

    # Albumin component
    albumin_component = max(0.0, min(2.0, (4.0 - albumin) / 2.0))

    # Age component
    age_component = max(0.0, min(2.0, (age - 50) / 30.0))

    # Female component
    female_component = 0.4 if female else 0.0

    # Dialysis adjustment
    dialysis_adjustment = 1.0 if dialysis else 0.0

    # Calculate raw MELD 3.0 score
    meld_raw = (
        log_bilirubin * 0.643 +
        log_creatinine * 0.670 +
        log_inr * 0.957 +
        sodium_component * 0.739 +
        albumin_component * 0.741 +
        age_component * 0.876 +
        female_component +
        dialysis_adjustment * 0.957
    )

    # Scale to final score (multiply by 10)
    meld_score = round(meld_raw * 10)

    # Clamp score between 6 and 40 (standard MELD range)
    meld_score = max(6, min(40, meld_score))

    # Interpretation and risk level
    if meld_score <= 9:
        interpretation = "Low severity of liver disease"
        risk_level = "low"
    elif meld_score <= 19:
        interpretation = "Moderate severity of liver disease"
        risk_level = "intermediate"
    elif meld_score <= 29:
        interpretation = "High severity of liver disease"
        risk_level = "high"
    else:
        interpretation = "Very high severity of liver disease"
        risk_level = "very high"

    # Metadata about calculation
    calculation_metadata = {
        "formula_version": "MELD 3.0",
        "input_validity": True,
        "dialysis_adjustment_applied": dialysis,
        "components": {
            "log_bilirubin": round(log_bilirubin, 3),
            "log_creatinine": round(log_creatinine, 3),
            "log_inr": round(log_inr, 3),
            "sodium_component": round(sodium_component, 3),
            "albumin_component": round(albumin_component, 3),
            "age_component": round(age_component, 3),
            "female_component": round(female_component, 3),
            "dialysis_component": round(dialysis_adjustment, 3)
        }
    }

    return {
        "meld_score": meld_score,
        "interpretation": interpretation,
        "risk_level": risk_level,
        "calculation_metadata": calculation_metadata
    }