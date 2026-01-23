from typing import Dict, Any

def medical_calculation_server_egfr_epi(age: int, male: bool, scr: float) -> Dict[str, Any]:
    """
    Calculate Estimated Glomerular Filtration Rate (eGFR) using the 2021 CKD-EPI creatinine equation.
    
    Parameters:
    -----------
    age : int
        Age in years
    male : bool
        True if the patient is male, False if female
    scr : float
        Serum creatinine level in mg/dL
    
    Returns:
    --------
    Dict[str, Any]
        A dictionary containing the calculated eGFR in mL/min/1.73m²:
        - egfr (float): estimated glomerular filtration rate

    Reference:
    ----------
    N Engl J Med. 2021 Nov 4;385(19):1737-1749
    """
    # Input validation
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive integer.")
    if not isinstance(scr, (float, int)) or scr <= 0:
        raise ValueError("Serum creatinine must be a positive number.")
    
    # CKD-EPI 2021 equation constants and logic
    if male:
        if scr <= 0.9:
            egfr = 142 * ((scr / 0.9) ** -0.293) * (0.993 ** age)
        else:
            egfr = 142 * ((scr / 0.9) ** -1.183) * (0.993 ** age)
    else:  # female
        if scr <= 0.7:
            egfr = 142 * ((scr / 0.7) ** -0.241) * (0.993 ** age) * 1.012
        else:
            egfr = 142 * ((scr / 0.7) ** -1.183) * (0.993 ** age) * 1.012
    
    # Round to 1 decimal place as per clinical convention
    egfr = round(egfr, 1)
    
    return {"egfr": egfr}