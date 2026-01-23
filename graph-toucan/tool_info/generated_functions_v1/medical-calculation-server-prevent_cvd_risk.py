from typing import Dict, Any
import math

def medical_calculation_server_prevent_cvd_risk(
    age: int,
    current_smoker: bool,
    diabetes: bool,
    egfr: float,
    female: bool,
    hdl: float,
    sbp: int,
    tc: float,
    using_antihtn: bool,
    using_statins: bool
) -> Dict[str, Any]:
    """
    Predicts 10-year risk of cardiovascular disease (CVD) in patients aged 30-79 without known CVD.
    
    Parameters:
    -----------
    age : int
        Age in years (30-79)
    current_smoker : bool
        True if patient is a current smoker
    diabetes : bool
        True if patient has diabetes
    egfr : float
        Estimated glomerular filtration rate in mL/min/1.73m²
    female : bool
        True if patient is female, False if male
    hdl : float
        HDL cholesterol in mmol/L
    sbp : int
        Systolic blood pressure in mmHg
    tc : float
        Total cholesterol in mmol/L
    using_antihtn : bool
        True if patient is using antihypertensive drugs
    using_statins : bool
        True if patient is using statins

    Returns:
    --------
    dict
        Dictionary containing:
        - risk_10yr (float): 10-year CVD risk as percentage
        - risk_category (str): Risk category ("Low", "Intermediate", "High")
        - transformed_variables (dict): Normalized variables used in model
        - model_score (float): Linear predictor (logits) before transformation
    """
    # Input validation
    if not (30 <= age <= 79):
        raise ValueError("Age must be between 30 and 79 inclusive.")
    if tc <= 0:
        raise ValueError("Total cholesterol must be positive.")
    if hdl <= 0:
        raise ValueError("HDL cholesterol must be positive.")
    if sbp <= 0:
        raise ValueError("Systolic blood pressure must be positive.")
    if egfr <= 0:
        raise ValueError("eGFR must be positive.")

    # Transform variables (centered and scaled as per typical risk models)
    cage = age - 55.0
    cnhdl = (tc / hdl) - 4.5
    chdl = hdl - 1.2
    csbp = sbp - 120
    csbp2 = (sbp - 120) ** 2 / 1000.0
    cegfr = egfr - 95
    cegfr2 = (egfr - 95) ** 2 / 1000.0

    # Coefficients from a typical CVD risk model (simplified for simulation)
    # These are illustrative coefficients, not from actual PREVENT model
    coeffs = {
        'age': 0.07,
        'nhdl': 0.35,
        'hdl': -0.2,
        'sbp': 0.02,
        'sbp2': 0.1,
        'egfr': -0.01,
        'egfr2': -0.05,
        'smoker': 0.3,
        'diabetes': 0.4,
        'antihtn': 0.2,
        'statins': -0.15,
        'female': -0.3
    }

    # Calculate linear predictor (logits)
    model_score = (
        coeffs['age'] * cage +
        coeffs['nhdl'] * cnhdl +
        coeffs['hdl'] * chdl +
        coeffs['sbp'] * csbp +
        coeffs['sbp2'] * csbp2 +
        coeffs['egfr'] * cegfr +
        coeffs['egfr2'] * cegfr2 +
        coeffs['smoker'] * current_smoker +
        coeffs['diabetes'] * diabetes +
        coeffs['antihtn'] * using_antihtn +
        coeffs['statins'] * using_statins +
        coeffs['female'] * female
    )

    # Convert logits to 10-year risk using logistic transformation
    # S0(10) is baseline survival at 10 years (assumed ~0.90 for illustration)
    s0_10 = 0.90
    risk_10yr = (1 - s0_10 ** math.exp(model_score)) * 100  # percentage

    # Clamp risk to [0, 100]
    risk_10yr = max(0.0, min(100.0, risk_10yr))

    # Determine risk category
    if risk_10yr < 5.0:
        risk_category = "Low"
    elif risk_10yr < 20.0:
        risk_category = "Intermediate"
    else:
        risk_category = "High"

    # Prepare transformed variables dict
    transformed_variables = {
        'cage': round(cage, 3),
        'cnhdl': round(cnhdl, 3),
        'chdl': round(chdl, 3),
        'csbp': round(csbp, 3),
        'csbp2': round(csbp2, 3),
        'cegfr': round(cegfr, 3),
        'cegfr2': round(cegfr2, 3)
    }

    return {
        'risk_10yr': round(risk_10yr, 2),
        'risk_category': risk_category,
        'transformed_variables': transformed_variables,
        'model_score': round(model_score, 3)
    }