from typing import Dict, Any

def medical_calculation_server_map_calculator(sbp: int, dbp: int) -> Dict[str, Any]:
    """
    Calculate Mean Arterial Pressure (MAP) using systolic (SBP) and diastolic (DBP) blood pressure values.
    
    The MAP is calculated using the formula: MAP = DBP + 1/3 * (SBP - DBP)
    
    Parameters:
    -----------
    sbp : int
        Systolic Blood Pressure in mmHg
    dbp : int
        Diastolic Blood Pressure in mmHg
    
    Returns:
    --------
    dict
        Dictionary containing:
        - map (float): calculated Mean Arterial Pressure in mmHg
        - formula (str): mathematical formula used for calculation
        - inputs (dict): input values with keys 'sbp' and 'dbp'
    
    Raises:
    -------
    ValueError
        If sbp or dbp are not positive integers, or if sbp <= dbp
    """
    # Input validation
    if not isinstance(sbp, int):
        raise ValueError("Systolic Blood Pressure (sbp) must be an integer")
    if not isinstance(dbp, int):
        raise ValueError("Diastolic Blood Pressure (dbp) must be an integer")
    if sbp <= 0:
        raise ValueError("Systolic Blood Pressure (sbp) must be a positive integer")
    if dbp <= 0:
        raise ValueError("Diastolic Blood Pressure (dbp) must be a positive integer")
    if sbp <= dbp:
        raise ValueError("Systolic Blood Pressure (sbp) must be greater than Diastolic Blood Pressure (dbp)")

    # Calculate MAP using the standard formula
    map_value = round(dbp + (1/3) * (sbp - dbp), 2)
    
    # Create result dictionary
    result = {
        "map": map_value,
        "formula": "MAP = DBP + 1/3 * (SBP - DBP)",
        "inputs": {
            "sbp": sbp,
            "dbp": dbp
        }
    }
    
    return result