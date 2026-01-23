from typing import Dict, Any, Optional

def medical_calculation_server_corrected_calcium(serum_calcium: float, patient_albumin: float, normal_albumin: Optional[float] = 4.0) -> Dict[str, Any]:
    """
    Calcium Correction for Hypoalbuminemia and Hyperalbuminemia.
    Calculates a corrected calcium level for patients with abnormal albumin levels.

    Parameters:
    -----------
    serum_calcium : float
        Patient's measured serum calcium level in mg/dL
    patient_albumin : float
        Patient's serum albumin level in g/dL
    normal_albumin : float, optional
        Normal/reference albumin level in g/dL, default is 4.0 g/dL

    Returns:
    --------
    dict
        Dictionary containing:
        - measured_calcium (float): measured serum calcium level in mg/dL
        - corrected_calcium (float): calculated corrected calcium level in mg/dL
        - calcium_interpretation (str): clinical interpretation of corrected calcium
        - albumin_status (str): albumin status category
        - calculations (dict): formula, calculation steps, and reference note

    Formula:
    --------
    Corrected Calcium = (0.8 * (Normal Albumin - Patient's Albumin)) + Serum Calcium

    References:
    -----------
    Payne RB, et al. Br Med J. 1973;4(5893):643-646.
    """
    # Input validation
    if not isinstance(serum_calcium, (int, float)):
        raise TypeError("serum_calcium must be a number")
    if not isinstance(patient_albumin, (int, float)):
        raise TypeError("patient_albumin must be a number")
    if normal_albumin is not None and not isinstance(normal_albumin, (int, float)):
        raise TypeError("normal_albumin must be a number or None")
    
    if normal_albumin is None:
        normal_albumin = 4.0

    # Calculate corrected calcium
    correction_factor = 0.8 * (normal_albumin - patient_albumin)
    corrected_calcium = correction_factor + serum_calcium

    # Determine albumin status
    if patient_albumin < 3.5:
        albumin_status = "Hypoalbuminemia"
    elif patient_albumin > 5.0:
        albumin_status = "Hyperalbuminemia"
    else:
        albumin_status = "Normal"

    # Determine calcium interpretation
    if corrected_calcium < 8.5:
        calcium_interpretation = "Hypocalcemia"
    elif corrected_calcium > 10.5:
        calcium_interpretation = "Hypercalcemia"
    else:
        calcium_interpretation = "Normocalcemia"

    # Create calculation details
    formula = "Corrected Calcium = (0.8 * (Normal Albumin - Patient's Albumin)) + Serum Calcium"
    calculation = f"Corrected Calcium = (0.8 * ({normal_albumin} - {patient_albumin})) + {serum_calcium} = {corrected_calcium:.2f}"
    note = "Reference: Payne RB, et al. Br Med J. 1973;4(5893):643-646."

    return {
        "measured_calcium": float(serum_calcium),
        "corrected_calcium": round(corrected_calcium, 2),
        "calcium_interpretation": calcium_interpretation,
        "albumin_status": albumin_status,
        "calculations": {
            "formula": formula,
            "calculation": calculation,
            "note": note
        }
    }