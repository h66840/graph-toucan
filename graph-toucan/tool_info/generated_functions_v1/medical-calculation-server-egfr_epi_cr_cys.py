from typing import Dict, Any

def medical_calculation_server_egfr_epi_cr_cys(age: int, male: bool, scr: float, scys: float) -> Dict[str, Any]:
    """
    Estimated Glomerular Filtration Rate (eGFR) using the 2021 CKD-EPI Creatinine-Cystatin C equation.
    
    Reference: N Engl J Med. 2021 Nov 4;385(19):1737-1749
    
    Parameters:
    -----------
    age : int
        Age in years
    male : bool
        True if patient is male, False if female
    scr : float
        Serum creatinine level in mg/dL
    scys : float
        Serum cystatin C level in mg/L
    
    Returns:
    --------
    dict
        Dictionary containing:
        - egfr (float): estimated glomerular filtration rate in mL/min/1.73m²
        - equation (str): name of the equation used
        - parameters (dict): intermediate calculation parameters including 'k_cr', 'k_cys', 'alpha', 'beta', and 'sex_factor'
    
    Raises:
    -------
    ValueError
        If age is not positive, scr or scys are non-positive, or scr/scys are unrealistic
    TypeError
        If inputs are of incorrect type
    """
    # Input validation
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if not isinstance(male, bool):
        raise TypeError("Male must be a boolean")
    if not isinstance(scr, (float, int)):
        raise TypeError("Serum creatinine (scr) must be a number")
    if not isinstance(scys, (float, int)):
        raise TypeError("Serum cystatin C (scys) must be a number")
    
    if age <= 0:
        raise ValueError("Age must be positive")
    if scr <= 0:
        raise ValueError("Serum creatinine must be positive")
    if scys <= 0:
        raise ValueError("Serum cystatin C must be positive")
    if scr > 15:
        raise ValueError("Unrealistic serum creatinine value (too high)")
    if scys > 8:
        raise ValueError("Unrealistic serum cystatin C value (too high)")

    # CKD-EPI Creatinine-Cystatin C equation constants
    # Reference: N Engl J Med. 2021 Nov 4;385(19):1737-1749
    
    # Creatinine and cystatin C parameters based on sex
    if male:
        k_cr = 0.7
        k_cys = 0.9
        sex_factor = 1.0
        alpha = -0.248
        beta = -0.375
    else:
        k_cr = 0.7
        k_cys = 0.9
        sex_factor = 1.073
        alpha = -0.248
        beta = -0.711

    # Min and max functions as used in the equation
    min_cr = min(scr / k_cr, 1.0)
    max_cr = max(scr / k_cr, 1.0)
    
    min_cys = min(scys / k_cys, 1.0)
    max_cys = max(scys / k_cys, 1.0)

    # Main equation
    egfr = 135 * (min_cr ** alpha) * (max_cr ** -0.601) * (min_cys ** beta) * (max_cys ** -0.375) * sex_factor
    
    # Adjust for age
    egfr *= (0.995 ** age)

    # Ensure eGFR is not negative
    egfr = max(egfr, 0)

    return {
        "egfr": round(egfr, 2),
        "equation": "CKD-EPI Creatinine-Cystatin C 2021",
        "parameters": {
            "k_cr": k_cr,
            "k_cys": k_cys,
            "alpha": alpha,
            "beta": beta,
            "sex_factor": sex_factor
        }
    }