from typing import Dict, Any

def medical_calculation_server_chads2_vasc_score(
    age: int,
    chf: bool,
    diabetes: bool,
    female: bool,
    hypertension: bool,
    stroke_history: bool,
    vascular_disease: bool
) -> Dict[str, Any]:
    """
    Calculate CHA₂DS₂-VASc Score for Atrial Fibrillation Stroke Risk.
    
    The CHA₂DS₂-VASc score is used to estimate stroke risk in patients with atrial fibrillation.
    Points are assigned based on the presence of specific clinical risk factors.
    
    Parameters:
    -----------
    age : int
        Age in years
    chf : bool
        True if patient has history of congestive heart failure
    diabetes : bool
        True if patient has history of diabetes mellitus
    female : bool
        True if patient is female, False if male
    hypertension : bool
        True if patient has history of hypertension
    stroke_history : bool
        True if patient has history of stroke, TIA, or thromboembolism
    vascular_disease : bool
        True if patient has history of vascular disease (prior MI, peripheral artery disease, or aortic plaque)
    
    Returns:
    --------
    dict
        Dictionary containing:
        - score (int): Total CHA₂DS₂-VASc score
        - risk_category (str): Risk category based on score
        - annual_stroke_risk (str): Estimated annual stroke risk as percentage string
        - risk_factors (dict): Individual risk factors with values and assigned points
    """
    # Validate inputs
    if not isinstance(age, int) or age < 0:
        raise ValueError("Age must be a non-negative integer.")
    if not all(isinstance(x, bool) for x in [chf, diabetes, female, hypertension, stroke_history, vascular_disease]):
        raise ValueError("All boolean parameters must be True or False.")

    score = 0
    risk_factors = {}

    # Congestive Heart Failure (1 point)
    chf_points = 1 if chf else 0
    risk_factors["chf"] = {"value": chf, "points": chf_points}
    score += chf_points

    # Hypertension (1 point)
    hypertension_points = 1 if hypertension else 0
    risk_factors["hypertension"] = {"value": hypertension, "points": hypertension_points}
    score += hypertension_points

    # Age-related points
    age_points = 0
    if age >= 75:
        age_points = 2
    elif age >= 65:
        age_points = 1
    risk_factors["age"] = {"value": age, "points": age_points}
    score += age_points

    # Diabetes (1 point)
    diabetes_points = 1 if diabetes else 0
    risk_factors["diabetes"] = {"value": diabetes, "points": diabetes_points}
    score += diabetes_points

    # Stroke history (2 points)
    stroke_points = 2 if stroke_history else 0
    risk_factors["stroke_history"] = {"value": stroke_history, "points": stroke_points}
    score += stroke_points

    # Vascular disease (1 point)
    vascular_points = 1 if vascular_disease else 0
    risk_factors["vascular_disease"] = {"value": vascular_disease, "points": vascular_points}
    score += vascular_points

    # Sex (female) (1 point)
    sex_points = 1 if female else 0
    risk_factors["sex"] = {"value": "female" if female else "male", "points": sex_points}
    score += sex_points

    # Determine risk category and annual stroke risk
    if score >= 2:
        risk_category = "High"
        annual_stroke_risk = f"{1.3 + (score - 2) * 1.0:.1f}%"  # Approximate linear increase
    elif score == 1:
        risk_category = "Moderate-High"
        annual_stroke_risk = "1.3%"
    else:  # score == 0
        risk_category = "Low"
        annual_stroke_risk = "0.2%"

    return {
        "score": score,
        "risk_category": risk_category,
        "annual_stroke_risk": annual_stroke_risk,
        "risk_factors": risk_factors
    }