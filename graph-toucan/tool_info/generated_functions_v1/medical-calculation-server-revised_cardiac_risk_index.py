from typing import Dict, List, Any, Optional

def medical_calculation_server_revised_cardiac_risk_index(
    high_risk_surgery: Optional[bool] = False,
    ischemic_heart_disease: Optional[bool] = False,
    congestive_heart_failure: Optional[bool] = False,
    cerebrovascular_disease: Optional[bool] = False,
    insulin_treatment: Optional[bool] = False,
    creatinine_over_2mg: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Revised Cardiac Risk Index (RCRI) for Pre-Operative Risk Assessment.
    
    Estimates the risk of major cardiac complications (e.g., myocardial infarction, heart failure, 
    pulmonary edema, ventricular fibrillation, complete heart block) within 30 days after 
    noncardiac surgery.

    Parameters:
    -----------
    high_risk_surgery : bool, optional
        Intraperitoneal, intrathoracic, or suprainguinal vascular surgery
    ischemic_heart_disease : bool, optional
        History of MI, positive exercise test, current chest pain due to ischemia, 
        nitrate use, or ECG with pathological Q waves
    congestive_heart_failure : bool, optional
        Clinical signs like pulmonary edema, bilateral rales, S3 gallop, PND, or CXR findings
    cerebrovascular_disease : bool, optional
        History of TIA or stroke
    insulin_treatment : bool, optional
        Pre-operative insulin use for diabetes management
    creatinine_over_2mg : bool, optional
        Pre-operative serum creatinine > 2 mg/dL (176.8 µmol/L)

    Returns:
    --------
    dict
        - rcri_score (int): Number of present risk factors (0–6)
        - risk_factors (List[str]): Names of active risk factors
        - risk_percent (float): Estimated 30-day risk of major cardiac event
        - risk_category (str): Categorical risk level ("Low risk", "Intermediate risk", "High risk")
        - score_interpretation (str): Clinical summary combining score and risk

    References:
    -----------
    Lee TH, et al. Circulation. 1999;100(10):1043-1049.
    Canadian Cardiovascular Society (CCS) Guidelines, 2017.
    European Society of Cardiology (ESC) Guidelines, 2022.
    """
    # Default to False if None
    high_risk_surgery = high_risk_surgery if high_risk_surgery is not None else False
    ischemic_heart_disease = ischemic_heart_disease if ischemic_heart_disease is not None else False
    congestive_heart_failure = congestive_heart_failure if congestive_heart_failure is not None else False
    cerebrovascular_disease = cerebrovascular_disease if cerebrovascular_disease is not None else False
    insulin_treatment = insulin_treatment if insulin_treatment is not None else False
    creatinine_over_2mg = creatinine_over_2mg if creatinine_over_2mg is not None else False

    # Define risk factors
    risk_factors_map = {
        "high_risk_surgery": "High-risk surgery",
        "ischemic_heart_disease": "Ischemic heart disease",
        "congestive_heart_failure": "Congestive heart failure",
        "cerebrovascular_disease": "Cerebrovascular disease",
        "insulin_treatment": "Insulin treatment",
        "creatinine_over_2mg": "Serum creatinine >2 mg/dL"
    }

    # Evaluate active risk factors
    active_risk_factors = []
    score = 0

    if high_risk_surgery:
        score += 1
        active_risk_factors.append(risk_factors_map["high_risk_surgery"])
    if ischemic_heart_disease:
        score += 1
        active_risk_factors.append(risk_factors_map["ischemic_heart_disease"])
    if congestive_heart_failure:
        score += 1
        active_risk_factors.append(risk_factors_map["congestive_heart_failure"])
    if cerebrovascular_disease:
        score += 1
        active_risk_factors.append(risk_factors_map["cerebrovascular_disease"])
    if insulin_treatment:
        score += 1
        active_risk_factors.append(risk_factors_map["insulin_treatment"])
    if creatinine_over_2mg:
        score += 1
        active_risk_factors.append(risk_factors_map["creatinine_over_2mg"])

    # Map score to risk percentage and category based on literature
    risk_map = {
        0: {"percent": 0.4, "category": "Low risk"},
        1: {"percent": 0.9, "category": "Low risk"},
        2: {"percent": 6.6, "category": "Intermediate risk"},
        3: {"percent": 11.0, "category": "Intermediate risk"},
        4: {"percent": 14.4, "category": "High risk"},
        5: {"percent": 20.3, "category": "High risk"},
        6: {"percent": 20.3, "category": "High risk"}  # Max observed in studies
    }

    risk_info = risk_map.get(score, risk_map[6])  # Cap at 6
    risk_percent = risk_info["percent"]
    risk_category = risk_info["category"]

    # Generate interpretation
    if score == 0:
        interpretation = "No identified risk factors. Very low risk of major cardiac complications."
    else:
        factor_list = ", ".join(active_risk_factors)
        interpretation = (
            f"RCRI Score: {score}. Risk factors present: {factor_list}. "
            f"Estimated 30-day risk of major cardiac event: {risk_percent:.1f}% ({risk_category.lower()})."
        )

    return {
        "rcri_score": score,
        "risk_factors": active_risk_factors,
        "risk_percent": risk_percent,
        "risk_category": risk_category,
        "score_interpretation": interpretation
    }