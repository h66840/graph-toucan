from typing import Dict, Any

def medical_calculation_server_calculate_mme(opioid: str, dose_per_administration: float, doses_per_day: int) -> Dict[str, Any]:
    """
    Calculates total daily Morphine Milligram Equivalents (MME) based on opioid type, dose, and frequency.
    
    Parameters:
    -----------
    opioid : str
        Name of the opioid (e.g., 'oxycodone', 'fentanyl_patch').
    dose_per_administration : float
        Amount of opioid per dose (mg for most, mcg/hr for fentanyl patch).
    doses_per_day : int
        Number of times the dose is taken per day.

    Returns:
    --------
    Dict[str, Any]
        A dictionary containing:
        - mme_per_day (float): Total Morphine Milligram Equivalents (MME) per day.
        - opioid_conversion_factor (float): Conversion factor used for morphine equivalence.
        - details (Dict): Additional information including validation status, assumptions, and special case notes.
    """
    # Define conversion factors (morphine mg equivalent per 1 mg of opioid)
    conversion_factors = {
        'morphine': 1.0,
        'oxycodone': 1.5,
        'hydrocodone': 1.0,
        'hydromorphone': 4.0,
        'oxymorphone': 3.0,
        'fentanyl_patch': 75.0,  # mcg/hr to mg/day morphine equivalent (approximate)
        'codeine': 0.15,
        'tramadol': 0.1,
        'tapentadol': 0.2,
        'methadone': 1.5  # Simplified; actual is dose-dependent
    }
    
    # Input validation
    errors = []
    if dose_per_administration < 0:
        errors.append("dose_per_administration must be non-negative")
    if doses_per_day < 0:
        errors.append("doses_per_day must be non-negative")
    if opioid.lower() not in conversion_factors:
        errors.append(f"Unknown opioid: {opioid}. Supported opioids: {list(conversion_factors.keys())}")
    
    # Default values in case of error
    mme_per_day = 0.0
    conversion_factor = 1.0
    details = {
        "input_valid": len(errors) == 0,
        "errors": errors,
        "assumptions": [],
        "notes": []
    }
    
    if not errors:
        opioid_key = opioid.lower()
        conversion_factor = conversion_factors[opioid_key]
        
        # Special handling for fentanyl patch (dose in mcg/hr, convert to daily MME)
        if opioid_key == 'fentanyl_patch':
            # Fentanyl patch: 1 mcg/hr ≈ 75 mg oral morphine/day (approximate conversion)
            mme_per_day = dose_per_administration * conversion_factor
            details["assumptions"].append("Transdermal fentanyl conversion assumes steady-state delivery and uses standard 1 mcg/hr ≈ 75 mg oral morphine/day equivalence.")
            details["notes"].append("Fentanyl patch conversion is approximate and may vary based on individual metabolism and patch formulation.")
        else:
            # Standard oral/parenteral opioids: dose * conversion factor * frequency
            mme_per_day = dose_per_administration * conversion_factor * doses_per_day
            details["assumptions"].append("Oral administration assumed for conversion factors.")
    
    return {
        "mme_per_day": float(mme_per_day),
        "opioid_conversion_factor": float(conversion_factor),
        "details": details
    }