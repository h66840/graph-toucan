from typing import Dict, Any

def medical_calculation_server_framingham_risk_score(
    age: int,
    gender: str,
    hdl_cholesterol: float,
    smoker: bool,
    systolic_bp: float,
    total_cholesterol: float,
    treated_for_bp: bool
) -> Dict[str, Any]:
    """
    Calculates the 10-year risk of heart attack (coronary heart disease) using the Framingham Risk Score.
    
    Parameters:
    -----------
    age : int
        Age of the patient (30-79 years).
    gender : str
        Gender of the patient ("male" or "female").
    hdl_cholesterol : float
        HDL cholesterol in mg/dL.
    smoker : bool
        Whether the patient is a current smoker (True if yes, False if no).
    systolic_bp : float
        Systolic blood pressure in mmHg.
    total_cholesterol : float
        Total cholesterol in mg/dL.
    treated_for_bp : bool
        Whether the patient is being treated for high blood pressure (True if yes, False if no).
    
    Returns:
    --------
    Dict[str, Any]
        A dictionary containing:
        - 'risk_score' (float): 10-year risk of heart attack as a percentage.
    
    Raises:
    -------
    ValueError
        If inputs are outside valid ranges or invalid.
    """
    # Input validation
    if not (30 <= age <= 79):
        raise ValueError("Age must be between 30 and 79 years.")
    if gender.lower() not in ["male", "female"]:
        raise ValueError("Gender must be 'male' or 'female'.")
    if total_cholesterol <= 0:
        raise ValueError("Total cholesterol must be greater than 0 mg/dL.")
    if hdl_cholesterol <= 0:
        raise ValueError("HDL cholesterol must be greater than 0 mg/dL.")
    if systolic_bp <= 0:
        raise ValueError("Systolic blood pressure must be greater than 0 mmHg.")

    # Coefficients for the Framingham equation (from Wilson et al., 1998)
    if gender.lower() == "male":
        # Coefficients for men
        age_coeff = 3.06117
        total_chol_coeff = 1.12370
        hdl_chol_coeff = -0.93263
        chol_age_coeff = 1.93303
        smoker_coeff = 0.65451
        smoker_age_coeff = 1.50150
        sbp_treated_coeff = 1.10927
        sbp_untreated_coeff = 0.93961

        # Calculate log of means for interaction terms
        log_age = age
        log_total_chol = total_cholesterol
        log_hdl_chol = hdl_cholesterol
        log_sbp = systolic_bp

        # Calculate points for each variable (continuous version)
        x = (
            age_coeff * log_age +
            total_chol_coeff * log_total_chol +
            hdl_chol_coeff * log_hdl_chol +
            chol_age_coeff * (log_age * log_total_chol / 100) +
            smoker_coeff * smoker +
            smoker_age_coeff * (smoker * log_age / 20) +
            (sbp_treated_coeff * treated_for_bp + sbp_untreated_coeff * (not treated_for_bp)) * log_sbp / 100
        )

        # Survival function for men at 10 years = 0.8825
        risk_score = (1 - 0.8825 ** (2.71828 ** (x - 23.9802))) * 100

    else:
        # Coefficients for women
        age_coeff = 2.32888
        total_chol_coeff = 1.20904
        hdl_chol_coeff = -0.70833
        chol_age_coeff = 0.69154
        smoker_coeff = 0.52873
        smoker_age_coeff = 1.91656
        sbp_treated_coeff = 1.80161
        sbp_untreated_coeff = 1.23317

        # Calculate log of means for interaction terms
        log_age = age
        log_total_chol = total_cholesterol
        log_hdl_chol = hdl_cholesterol
        log_sbp = systolic_bp

        # Calculate points for each variable (continuous version)
        x = (
            age_coeff * log_age +
            total_chol_coeff * log_total_chol +
            hdl_chol_coeff * log_hdl_chol +
            chol_age_coeff * (log_age * log_total_chol / 100) +
            smoker_coeff * smoker +
            smoker_age_coeff * (smoker * log_age / 60) +
            (sbp_treated_coeff * treated_for_bp + sbp_untreated_coeff * (not treated_for_bp)) * log_sbp / 100
        )

        # Survival function for women at 10 years = 0.9533
        risk_score = (1 - 0.9533 ** (2.71828 ** (x - 26.1931))) * 100

    # Clamp risk score between 0 and 100
    risk_score = max(0.0, min(100.0, risk_score))

    return {"risk_score": round(risk_score, 2)}