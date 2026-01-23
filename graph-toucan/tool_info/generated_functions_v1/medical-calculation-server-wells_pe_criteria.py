from typing import Dict, Any, Optional

def medical_calculation_server_wells_pe_criteria(
    clinical_signs_dvt: Optional[bool] = None,
    alternative_diagnosis_less_likely: Optional[bool] = None,
    heart_rate_over_100: Optional[bool] = None,
    immobilization_or_surgery: Optional[bool] = None,
    previous_dvt_or_pe: Optional[bool] = None,
    hemoptysis: Optional[bool] = None,
    malignancy: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Calculate Wells' Criteria for Pulmonary Embolism (PE).
    
    This function computes the Wells' PE score based on clinical criteria,
    categorizes risk using both three-tier and two-tier models, and provides
    interpretation and recommendations.
    
    Parameters:
    -----------
    clinical_signs_dvt : bool, optional
        Clinical signs and symptoms of DVT (leg swelling, pain with palpation)
    alternative_diagnosis_less_likely : bool, optional
        Alternative diagnosis less likely than PE
    heart_rate_over_100 : bool, optional
        Heart rate > 100 beats per minute
    immobilization_or_surgery : bool, optional
        Immobilization or surgery in the previous four weeks
    previous_dvt_or_pe : bool, optional
        Previous DVT/PE
    hemoptysis : bool, optional
        Hemoptysis
    malignancy : bool, optional
        Malignancy (treatment ongoing, treated in last 6 months, or palliative)
    
    Returns:
    --------
    dict
        Dictionary containing:
        - score (float): numeric Wells' PE criteria score
        - three_tier_model (str): risk category (Low, Moderate, High Risk)
        - two_tier_model (str): risk category with recommendation
        - score_interpretation (str): combined human-readable interpretation
    """
    # Initialize score
    score = 0.0
    
    # Validate inputs and calculate score
    try:
        if clinical_signs_dvt is True:
            score += 3.0
        if alternative_diagnosis_less_likely is True:
            score += 3.0
        if heart_rate_over_100 is True:
            score += 1.5
        if immobilization_or_surgery is True:
            score += 1.5
        if previous_dvt_or_pe is True:
            score += 1.5
        if hemoptysis is True:
            score += 1.0
        if malignancy is True:
            score += 1.0
    except Exception as e:
        return {
            "error": f"Input validation error: {str(e)}"
        }
    
    # Three-tier model classification
    if score < 2:
        three_tier_risk = "Low Risk"
    elif score <= 6:
        three_tier_risk = "Moderate Risk"
    else:
        three_tier_risk = "High Risk"
    
    # Two-tier model classification with recommendation
    if score >= 4:
        two_tier_risk = "PE Likely (proceed to CTA)"
    else:
        two_tier_risk = "PE Unlikely (consider D-dimer)"
    
    # Combined interpretation
    interpretation = (
        f"Wells' PE score: {score}. "
        f"Three-tier model: {three_tier_risk}. "
        f"Two-tier model: {two_tier_risk}."
    )
    
    return {
        "score": score,
        "three_tier_model": three_tier_risk,
        "two_tier_model": two_tier_risk,
        "score_interpretation": interpretation
    }